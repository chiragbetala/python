from importlib import import_module
from pathlib import Path
from fastapi import APIRouter

def get_all_routers():
    """Automatically discover and return all routers in the routers directory"""
    routers = []
    current_dir = Path(__file__).parent
    
    # Get all .py files in the routers directory
    for file_path in current_dir.glob("*.py"):
        if file_path.stem == "__init__":
            continue
            
        # Convert file path to module path (e.g., routers.users)
        module_name = f"routers.{file_path.stem}"
        
        try:
            # Import the module dynamically
            module = import_module(module_name)
            
            # If module has a router attribute, add it to our list
            if hasattr(module, "router"):
                routers.append(module.router)
        except Exception as e:
            print(f"Error loading router from {module_name}: {e}")
            
    return routers