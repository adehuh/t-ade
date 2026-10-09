"use strict";

function* depthFirst(nodes) {
  const stack = [];

  for (let i = nodes.length - 1; i >= 0; i--) {
    stack.push({ node: nodes[i], parent: "", depth: 0 });
  }

  while (stack.length > 0) {
    const { node, parent, depth } = stack.pop();
    const path = parent + node.name;
    yield { node, path, depth };

    if (node.children) {
      for (let i = node.children.length - 1; i >= 0; i--) {
        stack.push({ node: node.children[i], parent: path + "/", depth: depth + 1 });
      }
    }
  }
}

function* breadthFirst(nodes) {
  let level = nodes.map(node => ({ node, path: node.name, depth: 0 }));

  while (level.length > 0) {
    const nextLevel = [];

    for (const entry of level) {
      yield entry;

      if (entry.node.children) {
        for (const child of entry.node.children) {
          nextLevel.push({
            node: child,
            path: entry.path + "/" + child.name,
            depth: entry.depth + 1,
          });
        }
      }
    }

    level = nextLevel;
  }
}
