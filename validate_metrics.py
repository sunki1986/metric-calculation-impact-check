import sys
import importlib.util
import os

def load_processor_from_path(folder_path):
    """Dynamically loads the Processor class from a specific directory."""
    module_name = "main_module"
    # Ensure the folder is in the path for imports to work
    sys.path.insert(0, folder_path)
    
    # Path to your main.py file
    file_path = os.path.join(folder_path, "main.py")
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    
    # Remove from path to avoid naming collisions for the next load
    sys.path.pop(0)
    return module.Processor(multiplier=10)

if __name__ == "__main__":
    # In GitHub Actions, these paths are created by the 'checkout' step
    dev_path = "./base-branch" 
    pr_path = "./pr-branch"   

    try:
        dev_logic = load_processor_from_path(dev_path)
        pr_logic = load_processor_from_path(pr_path)

        test_input = 5
        dev_out = dev_logic.process_data(test_input)
        pr_out = pr_logic.process_data(test_input)

        if dev_out == pr_out:
            print(f"✅ Success: Both branches returned {pr_out}")
            sys.exit(0)
        else:
            print(f"❌ Failure: Dev branch returned {dev_out}, but PR returned {pr_out}")
            sys.exit(1)
            
    except Exception as e:
        print(f"⚠️ Error during validation: {e}")
        sys.exit(1)
