import streamlit as st
from directory_tree import DirectoryTree
import html

st.set_page_config(page_title="File Directory Structure Simulator", page_icon="📁", layout="wide")
st.markdown("""
<style>
.stApp{background:#101418;color:#e8edf2}
[data-testid="stSidebar"]{background:#171d23}
h1,h2,h3,p,label{color:#e8edf2}
.hero{padding:1.2rem 1.5rem;border:1px solid #34434e;border-radius:16px;background:linear-gradient(120deg,#182630,#172027);margin-bottom:1rem}
.metric{padding:1rem;background:#192229;border:1px solid #34434e;border-radius:12px}
.treebox{background:#0b0e11;color:#b8f7d4;border:1px solid #35434d;border-radius:12px;padding:1rem;font-family:monospace;white-space:pre-wrap;overflow-x:auto}
</style>
""", unsafe_allow_html=True)

if "tree" not in st.session_state: st.session_state.tree = DirectoryTree()
if "path" not in st.session_state: st.session_state.path = []
if "notice" not in st.session_state: st.session_state.notice = None
tree = st.session_state.tree

def current_node():
    node = tree.root
    for part in st.session_state.path:
        child = tree.find_child(node, part)
        if child is None or not child.is_folder():
            st.session_state.path = []
            return tree.root
        node = child
    return node

def count_items(node):
    files = folders = 0
    for child in node.children:
        if child.is_folder(): folders += 1
        else: files += 1
        f, d = count_items(child)
        files += f
        folders += d
    return files, folders

def render_lines(node, prefix="", root=True, last=True):
    lines = [node.name + "/" if root else prefix + ("└── " if last else "├── ") + node.name + ("/" if node.is_folder() else "")]
    children = node.children
    child_prefix = "" if root else prefix + ("    " if last else "│   ")
    for i, child in enumerate(children):
        lines.extend(render_lines(child, child_prefix, False, i == len(children)-1))
    return lines

def notify(kind, message):
    st.session_state.notice = (kind, message)

st.markdown('<div class="hero"><small>PYTHON EXPERIENTIAL LEARNING PROJECT</small><h1>📁 File Directory Structure Simulator</h1><p>A tree-based virtual file system built with Python and Streamlit.</p></div>', unsafe_allow_html=True)
if st.session_state.notice:
    kind, message = st.session_state.notice
    {"success": st.success, "error": st.error, "info": st.info}.get(kind, st.info)(message)

with st.sidebar:
    st.header("🧭 Navigation")
    st.caption("Current directory")
    st.code("/" + "/".join(st.session_state.path) if st.session_state.path else "/ (Root)")
    if st.button("⬅️ Go Back", use_container_width=True, disabled=not st.session_state.path):
        st.session_state.path = st.session_state.path[:-1]; st.rerun()
    if st.button("🏠 Go to Root", use_container_width=True):
        st.session_state.path = []; st.rerun()
    if st.button("🔄 Reset Simulator", use_container_width=True):
        st.session_state.tree = DirectoryTree(); st.session_state.path = []
        st.session_state.notice = ("success", "Simulator reset."); st.rerun()
    st.caption("Use the JSON backup controls below to save your directory between sessions.")

current = current_node()
file_count, folder_count = count_items(tree.root)
a,b,c = st.columns(3)
a.metric("Folders", folder_count); b.metric("Files", file_count); c.metric("Items here", len(current.children))
left, right = st.columns([1,1.25], gap="large")

with left:
    st.subheader("⚙️ Directory Operations")
    create_tab, nav_tab, manage_tab = st.tabs(["Create", "Navigate", "Manage"])
    with create_tab:
        name = st.text_input("New item name", placeholder="Documents or notes.txt", key="newname")
        kind = st.radio("Item type", ["Folder", "File"], horizontal=True)
        if st.button("＋ Create item", use_container_width=True):
            name = name.strip()
            if not name or "/" in name or name in {".",".."}:
                notify("error", "Enter a valid name without slashes.")
            elif tree.find_child(current, name):
                notify("error", "An item with that name already exists here.")
            else:
                (tree.create_folder if kind == "Folder" else tree.create_file)(current, name)
                notify("success", f"{kind} '{name}' created.")
            st.rerun()
    with nav_tab:
        folders = [x.name for x in current.children if x.is_folder()]
        if folders:
            target = st.selectbox("Choose a folder", folders)
            if st.button("Open folder", use_container_width=True):
                st.session_state.path.append(target); st.rerun()
        else: st.info("No child folders in this directory.")
    with manage_tab:
        if current.children:
            labels = [x.name + ("/" if x.is_folder() else "") for x in current.children]
            label = st.selectbox("Select item to manage", labels)
            old = label[:-1] if label.endswith("/") else label
            node = tree.find_child(current, old)
            new_name = st.text_input("Rename to", key="rename")
            x,y = st.columns(2)
            with x:
                if st.button("✏️ Rename", use_container_width=True):
                    new_name = new_name.strip()
                    if not new_name or "/" in new_name or new_name in {".",".."}:
                        notify("error", "Enter a valid new name.")
                    elif new_name != old and tree.find_child(current, new_name):
                        notify("error", "That name already exists here.")
                    else:
                        node.name = new_name; notify("success", f"Renamed to '{new_name}'.")
                    st.rerun()
            with y:
                if st.button("🗑️ Delete", use_container_width=True):
                    tree.delete(current, old); notify("success", f"Deleted '{old}'."); st.rerun()
        else: st.info("Nothing to rename or delete yet.")

with right:
    st.subheader("🌳 Directory Tree")
    st.caption("Current path: " + current.get_path())
    tree_text = "\n".join(render_lines(tree.root))
    st.markdown(f'<div class="treebox">{html.escape(tree_text)}</div>', unsafe_allow_html=True)
    st.subheader("🔎 Search using DFS")
    query = st.text_input("Exact file or folder name", key="search")
    if st.button("Search entire tree", use_container_width=True):
        if not query.strip():
            notify("error", "Enter a name to search.")
        else:
            results = tree.search(query.strip())
            st.session_state.results = [x.get_path() for x in results]
            notify("success" if results else "info", f"Found {len(results)} match(es)." if results else "No matching item found.")
        st.rerun()
    for result in st.session_state.get("results", []): st.write("📍", result)

st.divider()
st.subheader("📊 Current Directory Information")
x,y,z,w = st.columns(4)
x.metric("Name", current.name); y.metric("Type", "Folder")
z.metric("Direct folders", sum(1 for n in current.children if n.is_folder()))
w.metric("Direct files", sum(1 for n in current.children if not n.is_folder()))

st.divider()
st.subheader("💾 Save / Load")
st.download_button("⬇️ Download JSON backup", tree.to_json(), "directory_backup.json", "application/json")
uploaded = st.file_uploader("Load a JSON backup", type=["json"])
if uploaded and st.button("Load backup"):
    try:
        st.session_state.tree = DirectoryTree.from_json(uploaded.getvalue().decode("utf-8"))
        st.session_state.path = []; st.session_state.results = []
        notify("success", "Backup loaded successfully."); st.rerun()
    except (ValueError, KeyError, TypeError) as e:
        notify("error", f"Could not load backup: {e}"); st.rerun()
st.caption("Python • Streamlit • Tree Data Structure • DFS • JSON")
