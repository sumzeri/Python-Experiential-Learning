# File Directory Structure Simulator

A Python-only browser application simulating a file system with a tree data structure.

## Features
- Create folders and files
- Display hierarchical directory tree
- Navigate into folders and go back
- Search using Depth First Search (DFS)
- Rename and delete items
- Directory information
- Download and load JSON backups
- Dark-themed interface

## Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy
1. Upload `app.py`, `directory_tree.py`, `requirements.txt`, and `README.md` to GitHub.
2. Open Streamlit Community Cloud and sign in with GitHub.
3. Create an app from your repository and select `app.py`.
4. Deploy.

The directory is held in the current app session. Download a JSON backup if you want to keep it between sessions.
