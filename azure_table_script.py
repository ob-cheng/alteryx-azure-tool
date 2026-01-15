from ayx import Alteryx
import pandas as pd
import sys

# -----------------------------------------------------------------------------
# 1. Install Dependencies (No-Admin Workaround)
# -----------------------------------------------------------------------------
import os
import sys
import subprocess

# Define a local folder to store libraries (No Admin rights needed)
# We will use the user's AppData folder which is always writable
local_lib = os.path.join(os.environ['APPDATA'], 'Alteryx', 'PythonPackages')
if not os.path.exists(local_lib):
    os.makedirs(local_lib)

# Add this folder to the Python Path so Alteryx can see the libraries
if local_lib not in sys.path:
    sys.path.insert(0, local_lib)

try:
    import azure.data.tables
except ImportError:
    print(f"Installing 'azure-data-tables' to {local_lib}...")
    try:
        # Use subprocess to install directly to our local folder
        subprocess.check_call([sys.executable, "-m", "pip", "install", "azure-data-tables", "--target", local_lib])
        import azure.data.tables
        print("Installation successful!")
    except Exception as e:
        print(f"Installation failed: {str(e)}")
        raise RuntimeError("Could not install Azure libraries. Please contact IT or try 'pip install --user azure-data-tables' in a terminal.")

from azure.data.tables import TableClient

# -----------------------------------------------------------------------------
# 2. Read Credentials from Input #1
# -----------------------------------------------------------------------------
df_input = Alteryx.read("#1")

if df_input.empty:
    raise ValueError("Input #1 is empty. Please provide StorageAccount, AccountKey, and TableName columns.")

# -----------------------------------------------------------------------------
# 3. Process each row and output to separate anchors
# -----------------------------------------------------------------------------
# Limit to 5 output anchors (Alteryx Python tool standard limit)
max_anchors = 5
rows_to_process = min(len(df_input), max_anchors)

if len(df_input) > max_anchors:
    print(f"Warning: Input contains {len(df_input)} rows, but script is limited to {max_anchors} output anchors. Only the first {max_anchors} will be processed.")

for index in range(rows_to_process):
    row = df_input.iloc[index]
    
    # 1-based anchor number (1, 2, 3, 4, 5)
    output_anchor = index + 1
    
    storage_account = row['StorageAccount']
    account_key = row['AccountKey']
    table_name = row['TableName']
    
    endpoint_suffix = "core.windows.net"
    if 'EndpointSuffix' in df_input.columns and not pd.isna(row['EndpointSuffix']):
        endpoint_suffix = row['EndpointSuffix']

    connection_string = f"DefaultEndpointsProtocol=https;AccountName={storage_account};AccountKey={account_key};EndpointSuffix={endpoint_suffix}"

    print(f"Processing Row {index}: Connecting to table '{table_name}' for Output #{output_anchor}...")

    try:
        table_client = TableClient.from_connection_string(conn_str=connection_string, table_name=table_name)
        
        # Fetch Data
        entities = table_client.list_entities()
        data = list(entities)
        
        if not data:
            print(f"  -> Table '{table_name}' is empty.")
            df_output = pd.DataFrame()
        else:
            df_output = pd.DataFrame(data)
            
            # Reorder standard columns
            cols = df_output.columns.tolist()
            if 'PartitionKey' in cols:
                cols.insert(0, cols.pop(cols.index('PartitionKey')))
            if 'RowKey' in cols:
                cols.insert(1, cols.pop(cols.index('RowKey')))
            df_output = df_output[cols]
            
            print(f"  -> Retrieved {len(df_output)} rows.")

        # Output to specific anchor
        Alteryx.write(df_output, output_anchor)

    except Exception as e:
        error_msg = f"Error reading table '{table_name}': {str(e)}"
        print(f"  -> {error_msg}")
        df_error = pd.DataFrame({'Error': [error_msg], 'TableName': [table_name]})
        Alteryx.write(df_error, output_anchor)

print("Batch processing complete.")
