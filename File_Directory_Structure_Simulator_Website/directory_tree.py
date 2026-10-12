import json

class Node:
    def __init__(self, name, node_type, parent=None):
        self.name = name
        self.node_type = node_type
        self.parent = parent
        self.children = []

    def is_folder(self):
        return self.node_type == "folder"

    def get_path(self):
        parts, node = [], self
        while node:
            parts.append(node.name)
            node = node.parent
        return "/" + "/".join(reversed(parts))

    def add_child(self, child):
        if not self.is_folder():
            raise ValueError("Files cannot contain child items.")
        if any(item.name == child.name for item in self.children):
            raise ValueError(f"'{child.name}' already exists.")
        child.parent = self
        self.children.append(child)

class DirectoryTree:
    def __init__(self):
        self.root = Node("Root", "folder")

    def find_child(self, parent, name):
        return next((child for child in parent.children if child.name == name), None)

    def create_folder(self, parent, name):
        node = Node(name, "folder")
        parent.add_child(node)
        return node

    def create_file(self, parent, name):
        node = Node(name, "file")
        parent.add_child(node)
        return node

    def search(self, name):
        found = []
        def dfs(node):
            if node.name == name:
                found.append(node)
            for child in node.children:
                dfs(child)
        dfs(self.root)
        return found

    def delete(self, parent, name):
        node = self.find_child(parent, name)
        if node is None:
            raise ValueError(f"'{name}' not found.")
        parent.children.remove(node)
        node.parent = None
        return node

    def to_dict(self):
        def encode(node):
            return {"name": node.name, "node_type": node.node_type,
                    "children": [encode(child) for child in node.children]}
        return encode(self.root)

    def to_json(self):
        return json.dumps(self.to_dict(), indent=2)

    @classmethod
    def from_json(cls, raw):
        data = json.loads(raw)
        def build(item, parent=None):
            if not isinstance(item, dict):
                raise ValueError("Invalid node.")
            name, kind = item.get("name"), item.get("node_type")
            children = item.get("children", [])
            if not isinstance(name, str) or not name or "/" in name:
                raise ValueError("Invalid node name.")
            if kind not in ("folder", "file") or not isinstance(children, list):
                raise ValueError("Invalid node type or children.")
            if kind == "file" and children:
                raise ValueError("A file cannot contain children.")
            node = Node(name, kind, parent)
            for child_data in children:
                child = build(child_data, node)
                if any(existing.name == child.name for existing in node.children):
                    raise ValueError(f"Duplicate name: {child.name}")
                node.children.append(child)
            return node
        root = build(data)
        if root.node_type != "folder":
            raise ValueError("Root must be a folder.")
        root.name = "Root"
        tree = cls()
        tree.root = root
        return tree
