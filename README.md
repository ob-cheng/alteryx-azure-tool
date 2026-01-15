# Azure Table Connector for Alteryx

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python: 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)

A professional-grade Python utility for Alteryx Designer and Gallery that allows users to fetch data from up to **five Azure Table Storage tables** simultaneously within a single tool.

## ⚠️ Security Warning
**Credential Safety First:** NEVER share your `AccountKey` or commit files containing credentials to version control. 
- The included `.gitignore` is configured to ignore `.csv` and `.xlsx` files.
- Always prefer encrypted Alteryx parameters or environment variables for production environments.

---

## 🚀 Key Features
- **Multi-Table Support**: Process up to 5 different Azure tables in one go.
- **No-Admin Workaround**: Install dependencies without Windows Administrator rights.
- **Smart Formatting**: Automatically handles PartitionKeys, RowKeys, and dynamic schemas.
- **Gallery Ready**: Optimized for Alteryx Server/Gallery environments.

---

## 🛠 Required Libraries
To run this tool, the following Python package is required:
- `azure-data-tables` (The modern, high-performance Azure SDK)

---

## 📂 Which Script Should I Use?

### 1. Local Designer (`azure_table_script.py`)
Use this if you are working on your personal machine or a company laptop.
- **The "No-Admin" Bypass**: This script detects if the library is missing and installs it into your `%APPDATA%` folder instead of the restricted system folder.
- **⚠️ Compliance Note**: While this allows you to bypass the need for an IT Administrator to install software, you **must confirm with your IT/Compliance Manager** that this alignment-of-libraries method follows your corporate security policies before use.

### 2. Alteryx Gallery/Server (`azure_table_script_gallery.py`)
Use this for workflows meant to be scheduled or shared on a Gallery.
- **Prerequisite**: This version assumes the Alteryx Server Administrator has already installed `azure-data-tables` on the worker nodes.
- **Support**: If you encounter a `ModuleNotFoundError` on the Gallery, contact your Server Admin and request they run `pip install azure-data-tables` on the Alteryx Server.

---

## ⚙️ Configuration

### 1. Prepare your Input
Connect a **Text Input** tool to the Python tool's **Input #1**. Use the following structure:

| StorageAccount | AccountKey | TableName | EndpointSuffix |
| :--- | :--- | :--- | :--- |
| `your_account` | `your_secret_key` | `YourTable1` | `core.windows.net` |
| `your_account` | `your_secret_key` | `YourTable2` | `core.windows.net` |
| ... | ... | ... | (Defaults to global Azure) |

*Note: You can include up to 5 rows to populate Output Anchors 1 through 5.*

### 2. Implementation
1. Copy the code from the appropriate `.py` file.
2. Paste it into the **Alteryx Python Tool** editor.
3. Run the workflow.

---

## 📝 License
Distributed under the **MIT License**. See `LICENSE` for more information.

---
**Developed by BitBridges**
