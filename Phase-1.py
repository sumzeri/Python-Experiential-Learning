class Node:
    def __init__(self, name, type):
        self.name = name
        self.type = type
        self.children = []
    def add(self, node):
        self.children.append(node)
    def display(self, level=0):
        print("  " * level + self.name)
        for child in self.children:
            child.display(level + 1)
class DirectoryTree:
    def __init__(self):
        self.root = Node("Root", "folder")
    def create_folder(self, parent, name):
        folder = Node(name, "folder")
        parent.add(folder)
        return folder
    def create_file(self, parent, name):
        file = Node(name, "file")
        parent.add(file)
        return file
tree = DirectoryTree()
documents = tree.create_folder(tree.root, "Documents")
tree.create_file(documents, "Assignment.pdf")
pictures = tree.create_folder(tree.root, "Pictures")
tree.create_file(pictures, "Photo.jpg")
tree.root.display()