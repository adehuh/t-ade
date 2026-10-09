"use strict";

// Appendix A
const folders = [
  {
    "type": "folder",
    "name": "Episode123",
    "children": [
      {
        "type": "folder",
        "name": "Shot045",
        "children": [
          {
            "type": "folder",
            "name": "Scenes",
            "children": [
              {
                "type": "file",
                "name": "Episode123_Shot045_V001.mov"
              },
              {
                "type": "file",
                "name": "Episode123_Shot045_V002.mov"
              },
              {
                "type": "file",
                "name": "Episode123_Shot045_V003.mov"
              }
            ]
          },
          {
            "type": "file",
            "name": "Readme.md"
          }
        ]
      }
    ]
  },
  {
    "type": "folder",
    "name": "Episode678",
    "children": [
      {
        "type": "folder",
        "name": "Shot009",
        "children": [
          {
            "type": "folder",
            "name": "Scenes",
            "children": [
              {
                "type": "file",
                "name": "Episode678_Shot009_V001.mov"
              }
            ]
          },
          {
            "type": "file",
            "name": "Readme.md"
          }
        ]
      }
    ]
  },
  {
    "type": "folder",
    "name": "Episode456",
    "children": [
      {
        "type": "folder",
        "name": "Shot101",
        "children": [
          {
            "type": "folder",
            "name": "Scenes",
            "children": [
              {
                "type": "file",
                "name": "Episode456_Shot101_V001.mov"
              }
            ]
          },
          {
            "type": "file",
            "name": "Readme.md"
          }
        ]
      }
    ]
  }
];

function renderTraversal(target, entries) {
  const fragment = document.createDocumentFragment();

  for (const { node, path, depth } of entries) {
    const item = document.createElement("tr");
    const depthCell = document.createElement("td");
    depthCell.className = "depth";
    depthCell.textContent = String(depth);
    const nameCell = document.createElement("td");
    const label = document.createElement("code");
    const suffix = node.type === "folder" ? "/" : "";
    label.textContent = node.name + suffix;
    label.title = path + suffix;
    label.style.paddingInlineStart = `${depth * 4}ch`;
    if (node.type === "folder") label.className = "folder";
    nameCell.append(label);
    item.append(depthCell, nameCell);
    fragment.append(item);
  }

  target.replaceChildren(fragment);
}

renderTraversal(document.getElementById("dfs"), depthFirst(folders));
renderTraversal(document.getElementById("bfs"), breadthFirst(folders));
