def provision_server(os_type, memory_gb):
    if memory_gb < 2:
        return "Deployment failed: Insufficient memory"
    else: 
        return f"Server provisioned with {memory_gb}GB memory on {os_type} OS"
    
# Un-indented! These now run in the main script.
status = provision_server("Linux", 12)
print(status)