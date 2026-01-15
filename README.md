## Two Versions of the Script

| File | Environment | Dependency Handling |
| :--- | :--- | :--- |
| `azure_table_script.py` | **Local Designer** | Installs libraries to `%APPDATA%` (No Admin needed). |
| `azure_table_script_gallery.py`| **Alteryx Gallery** | Assumes libraries are pre-installed by Admin. |

## 1. Configure Input
Add a **Text Input** tool to your workflow. The script supports up to **5 rows**, where each row connects to a different table and outputs to a separate anchor (1-5).

**Required Columns:**
- `StorageAccount`
- `AccountKey`
- `TableName`
- `EndpointSuffix` (Optional)

### Example Input Table

| StorageAccount | AccountKey | TableName | EndpointSuffix |
| :--- | :--- | :--- | :--- |
| YOUR_ACCOUNT_NAME | YOUR_ACCOUNT_KEY | Table1 | core.windows.net |
| YOUR_ACCOUNT_NAME | YOUR_ACCOUNT_KEY | Table2 | core.windows.net |

## 2. Configure Python Tool
1. Drag a **Python** tool onto the canvas.
2. Connect the **Text Input** tool to the **Input #1** anchor of the Python tool.
3. Paste the code from `azure_table_script.py` (Local) or `azure_table_script_gallery.py` (Server) into the Python tool's code editor.

## 3. Run Workflow
Run the workflow. The script will:
1. Iterate through your input rows (up to 5).
2. Connect to each Azure Table.
3. Output each table's data to the corresponding anchor number (Input Row 1 → Anchor 1, etc.).

## Troubleshooting

### "ModuleNotFoundError" or "CalledProcessError" (Local)
If you don't have Administrator rights, the standard Alteryx package installer will fail. 

**Solution:** Use `azure_table_script.py`. It creates a private library folder in your `%APPDATA%` folder and installs the libraries there.
1.  **Just Run the Workflow**: The script will automatically try to install the libraries to your user folder.
2.  **Wait**: The first run might take 30-60 seconds.
