"""
File Utility Functions
Helpers for file operations
"""

import os

def is_supported_file(filename, extensions):
    """
    Check if a file has one of the supported extensions.
    
    Args:
        filename: The name of the file to check
        extensions: A set of supported extensions (e.g., {'.html', '.txt'})
        
    Returns:
        bool: True if the file has a supported extension, False otherwise
    """
    return os.path.splitext(filename)[1].lower() in extensions

def get_all_files(paths, recursive=False, supported_extensions=None):
    """
    Get all supported files from the given paths.
    
    Args:
        paths: List of file or directory paths
        recursive: Whether to search directories recursively
        supported_extensions: Set of file extensions to include
        
    Returns:
        list: List of tuples (full_path, relative_path)
    """
    if not supported_extensions:
        supported_extensions = set()
        
    files = []
    
    for path in paths:
        if os.path.isfile(path):
            if is_supported_file(path, supported_extensions):
                # For single file, use the filename as relative path
                filename = os.path.basename(path)
                files.append((path, filename))
        elif os.path.isdir(path):
            if recursive:
                # Walk through all directories and subdirectories
                for root, _, filenames in os.walk(path):
                    for filename in filenames:
                        if is_supported_file(filename, supported_extensions):
                            full_path = os.path.join(root, filename)
                            rel_path = os.path.relpath(full_path, path)
                            files.append((full_path, os.path.join(os.path.basename(path), rel_path)))
            else:
                # Just process the files in the top directory
                for filename in os.listdir(path):
                    full_path = os.path.join(path, filename)
                    if os.path.isfile(full_path) and is_supported_file(filename, supported_extensions):
                        files.append((full_path, os.path.join(os.path.basename(path), filename)))
                
    return files 