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
        path = []
        current = self
        while current:
            path.append(current.name)
            current = current.parent
        return "/".join(reversed(path))
    def add_child(self, child):
        if not self.is_folder():
            raise ValueError("A file cannot contain children.")
        if any(x.name.lower() == child.name.lower() for x in self.children):
            raise ValueError("An item with this name already exists.")
        child.parent = self
        self.children.append(child)
class DirectoryTree:
    def __init__(self):
        self.root = Node("Root", "folder")
    def find_child(self, parent, name):
        for child in parent.children:
            if child.name.lower() == name.lower():
                return child
        return None
    def create_folder(self, parent, name):
        folder = Node(name, "folder")
        parent.add_child(folder)
        return folder
    def create_file(self, parent, name):
        file = Node(name, "file")
        parent.add_child(file)
        return file
    def search(self, name):
        results = []
        def dfs(node):
            if node.name.lower() == name.lower():
                results.append(node)
            for child in node.children:
                dfs(child)
        dfs(self.root)
        return results
    def delete(self, node):
        if node == self.root:
            raise ValueError("Root cannot be deleted.")
        node.parent.children.remove(node)
    def rename(self, node, new_name):
        if node == self.root:
            raise ValueError("Root cannot be renamed.")
        if self.find_child(node.parent, new_name):
            raise ValueError("An item with this name already exists.")
        node.name = new_name
    def display(self):
        print("\nDirectory Tree:")
        print("Root/")
        def show(node, prefix=""):
            for i, child in enumerate(node.children):
                last = i == len(node.children) - 1
                connector = "└── " if last else "├── "
                suffix = "/" if child.is_folder() else ""
                print(prefix + connector + child.name + suffix)
                if child.is_folder():
                    show(child, prefix + ("    " if last else "│   "))
        show(self.root)
    def info(self, node):
        files = folders = 0
        def count(current):
            nonlocal files, folders
            for child in current.children:
                if child.is_folder():
                    folders += 1
                    count(child)
                else:
                    files += 1
        count(node)
        print("\nDirectory Information")
        print("---------------------")
        print("Path         :", node.get_path())
        print("Folders      :", folders)
        print("Files        :", files)
        print("Total Items  :", files + folders)
    def save(self, filename="directory.json"):
        def convert(node):
            return {
                "name": node.name,
                "type": node.node_type,
                "children": [convert(x) for x in node.children]
            }
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(convert(self.root), file, indent=4)
    def load(self, filename="directory.json"):
        def convert(data, parent=None):
            node = Node(data["name"], data["type"], parent)
            for child in data.get("children", []):
                node.children.append(convert(child, node))
            return node
        with open(filename, "r", encoding="utf-8") as file:
            self.root = convert(json.load(file))
def menu(current):
    print("\n" + "=" * 55)
    print("       FILE DIRECTORY STRUCTURE SIMULATOR")
    print("=" * 55)
    print("Current Directory:", current.get_path())
    print("\n1. Create Folder")
    print("2. Create File")
    print("3. Display Directory Tree")
    print("4. Navigate to Folder")
    print("5. Go Back")
    print("6. Search")
    print("7. Rename")
    print("8. Delete")
    print("9. Directory Information")
    print("10. Save Directory")
    print("11. Load Directory")
    print("12. Exit")
def main():
    tree = DirectoryTree()
    current = tree.root
    while True:
        menu(current)
        choice = input("\nEnter your choice: ").strip()
        try:
            if choice == "1":
                name = input("Enter folder name: ").strip()
                if name:
                    tree.create_folder(current, name)
                    print(f"Folder '{name}' created successfully.")
            elif choice == "2":
                name = input("Enter file name: ").strip()
                if name:
                    tree.create_file(current, name)
                    print(f"File '{name}' created successfully.")
            elif choice == "3":
                tree.display()
            elif choice == "4":
                name = input("Enter folder name: ").strip()
                folder = tree.find_child(current, name)
                if folder and folder.is_folder():
                    current = folder
                    print("Moved to:", current.get_path())
                else:
                    print("Folder not found.")
            elif choice == "5":
                if current.parent:
                    current = current.parent
                else:
                    print("Already at Root.")
                print("Current Directory:", current.get_path())
            elif choice == "6":
                name = input("Enter file/folder name to search: ").strip()
                results = tree.search(name)
                if results:
                    print("\nSearch Results:")
                    for item in results:
                        kind = "Folder" if item.is_folder() else "File"
                        print(f"{kind}: {item.get_path()}")
                else:
                    print("No matching item found.")
            elif choice == "7":
                old = input("Enter current name: ").strip()
                node = tree.find_child(current, old)
                if node:
                    new = input("Enter new name: ").strip()
                    tree.rename(node, new)
                    print("Renamed successfully.")
                else:
                    print("File/folder not found.")
            elif choice == "8":
                name = input("Enter file/folder name to delete: ").strip()
                node = tree.find_child(current, name)
                if node:
                    tree.delete(node)
                    print(f"'{name}' deleted successfully.")
                else:
                    print("File/folder not found.")
            elif choice == "9":
                tree.info(current)
            elif choice == "10":
                filename = input("Enter file name [directory.json]: ").strip()
                tree.save(filename or "directory.json")
                print("Directory saved successfully.")
            elif choice == "11":
                filename = input("Enter file name [directory.json]: ").strip()
                tree.load(filename or "directory.json")
                current = tree.root
                print("Directory loaded successfully.")
            elif choice == "12":
                print("\nProject ended.")
                print("Thank you for using the simulator.")
                break
            else:
                print("Invalid choice. Please select 1-12.")
        except (ValueError, OSError, KeyError, TypeError, json.JSONDecodeError) as error:
            print("Error:", error)
        if choice != "12":
            input("\nPress Enter to continue...")
if __name__ == "__main__":
    main()
    
