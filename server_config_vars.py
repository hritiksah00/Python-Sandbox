# File: server_config_vars.py
# Purpose: Linux server deployment configuration and variable naming practice

# --- Part 1: Valid Variables (Using snake_case) ---
# These represent our Linux server deployment specs
cpu_core_count = 8
max_memory_gb = 32
primary_server_name = "ubuntu-web-01"

print("--- Initializing Server Specs ---")
print(f"Target Server: {primary_server_name}")
print(f"Allocated Cores: {cpu_core_count}")
print(f"Memory Limit: {max_memory_gb}GB\n")

# --- Part 2: Invalid Variables (Commented out to prevent crash) ---

# Invalid Variable 1: Starts with a number
# 1st_node_ip = "10.0.0.5"
# Reason: Python throws a SyntaxError because variable names cannot begin with a digit. 
# Fix: node_1_ip = "10.0.0.5"

# Invalid Variable 2: Contains spaces
# server location zone = "us-east-1"
# Reason: Spaces are strictly forbidden. Python thinks you are listing multiple separate commands.
# Fix: server_location_zone = "us-east-1"

# Invalid Variable 3: Contains special characters
# max-bandwidth@mbps = 1000
# Reason: Special characters like hyphens (-) or the @ symbol are illegal. Hyphens are read as a subtraction math symbol.
# Fix: max_bandwidth_mbps = 1000