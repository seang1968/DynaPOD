import os

# Base directory where the structure will be created
#base_dir = "I:/cygwin64/home/sg22321/0NewCode"
base_dir = "."
# Directory structure and files to be created
structure = {
    "config": ["config.xml"],
    "data": [],
    "database": ["db_helpers.py", "sqlite_manager.py", "__init__.py"],
    "helper": [
        "constants_singleton.py", "gvar_singleton.py", "logging_singleton.py",
        "timer_singleton.py", "configuration.py", "__init__.py"
    ],
    "logs": ["etl.log"],
    "processing": ["data_cleaner.py", "data_transformer.py", "etl_manager.py", "__init__.py"],
    "scripts": ["run_etl.py", "__init__.py"],
    "tests": [
        "test_data_cleaner.py", "test_logging_singleton.py", 
        "test_timer_singleton.py", "__init__.py"
    ]
}

# Function to create directories and files
def create_structure(base_dir, structure):
    for folder, files in structure.items():
        folder_path = os.path.join(base_dir, folder)
        os.makedirs(folder_path, exist_ok=True)
        for file in files:
            file_path = os.path.join(folder_path, file)
            # Create an empty file
            with open(file_path, 'w') as f:
                pass
            print(f"Created {file_path}")

# Run the function to create the structure
create_structure(base_dir, structure)
