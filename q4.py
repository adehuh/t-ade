import json
import sqlite3
from contextlib import closing
from pathlib import Path


def iter_rows(nodes):
    if not isinstance(nodes, list):
        raise ValueError("The JSON root must be a list")

    stack = [(node, None, position) for position, node in reversed(list(enumerate(nodes)))]
    node_id = 0

    while stack:
        node, parent_id, position = stack.pop()
        if not isinstance(node, dict):
            raise ValueError("Each node must be an object")

        kind = node.get("type")
        name = node.get("name")
        children = node.get("children", [])

        if kind not in ("folder", "file"):
            raise ValueError("Node type must be 'folder' or 'file'")
        if not isinstance(name, str) or not name:
            raise ValueError("Node name must be a non-empty string")
        if not isinstance(children, list):
            raise ValueError("Children must be a list")
        if kind == "file" and children:
            raise ValueError("Files cannot have children")

        node_id += 1
        yield node_id, parent_id, kind, name, position

        for index in range(len(children) - 1, -1, -1):
            stack.append((children[index], node_id, index))


def create_database(json_path: Path, database_path: Path) -> int:
    """Refresh the nodes table from JSON, rolling back if the import fails."""
    with open(json_path, encoding="utf-8") as source:
        data = json.load(source)

    with closing(sqlite3.connect(database_path)) as connection:
        connection.execute("PRAGMA foreign_keys = ON")
        with connection:
            connection.execute("BEGIN")
            connection.execute("""
                CREATE TABLE IF NOT EXISTS nodes (
                    id INTEGER PRIMARY KEY,
                    parent_id INTEGER REFERENCES nodes(id),
                    type TEXT NOT NULL CHECK (type IN ('folder', 'file')),
                    name TEXT NOT NULL CHECK (length(name) > 0),
                    position INTEGER NOT NULL CHECK (position >= 0)
                )
            """)
            connection.execute("DELETE FROM nodes")
            connection.executemany(
                "INSERT INTO nodes (id, parent_id, type, name, position) VALUES (?, ?, ?, ?, ?)",
                iter_rows(data),
            )
            connection.execute("CREATE INDEX IF NOT EXISTS nodes_parent_position ON nodes(parent_id, position)")
            count = connection.execute("SELECT COUNT(*) FROM nodes").fetchone()[0]

    return count


def main() -> None:
    directory = Path(__file__).resolve().parent
    json_path = directory / "appendix_a.json"
    database_path = directory / "appendix_a.db"

    print(f"Reading {json_path.name}...", flush=True)
    count = create_database(json_path, database_path)
    print(f"Imported {count} entries into {database_path.name}.\n")

    with closing(sqlite3.connect(database_path)) as connection:
        rows = connection.execute("""
            WITH RECURSIVE tree (id, parent_id, type, name, path) AS (
                SELECT id, parent_id, type, name, '/' || name
                FROM nodes WHERE parent_id IS NULL
                UNION ALL
                SELECT n.id, n.parent_id, n.type, n.name, tree.path || '/' || n.name
                FROM nodes AS n JOIN tree ON n.parent_id = tree.id
            )
            SELECT id, parent_id, type, name, path FROM tree ORDER BY id
        """).fetchall()
        name_width = max([len("Name")] + [len(row[3]) for row in rows])
        print(f"{'ID':>3}  {'Parent':>6}  {'Type':<6}  {'Name':<{name_width}}  Path")
        for node_id, parent_id, kind, name, path in rows:
            parent = "-" if parent_id is None else str(parent_id)
            print(f"{node_id:>3}  {parent:>6}  {kind:<6}  {name:<{name_width}}  {path}")


if __name__ == "__main__":
    main()
