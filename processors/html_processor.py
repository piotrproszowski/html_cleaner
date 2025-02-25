"""
HTML Processing Module
Handles the actual HTML modification using BeautifulSoup
"""

import os
from bs4 import BeautifulSoup, Comment

def process_html_file(input_path, output_path, tags_to_remove, tags_to_remove_with_content, clean_attrs_mode, attrs_exceptions=None):
    """
    Process HTML file by modifying specified tags using BeautifulSoup.
    
    Args:
        input_path: Path to the input file
        output_path: Path where processed file will be saved
        tags_to_remove: List of tags to remove (preserving content)
        tags_to_remove_with_content: List of tags to remove including their content
        clean_attrs_mode: Mode for cleaning attributes - 'all', 'selected', or 'all_except'
        attrs_exceptions: List of tags to exclude or include for attribute cleaning (depends on clean_attrs_mode)
    """
    try:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(input_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Parse the HTML content
        soup = BeautifulSoup(content, 'html.parser')
        
        # Remove comments if specified (special case)
        if 'comment' in tags_to_remove or 'comment' in tags_to_remove_with_content:
            for comment in soup.find_all(text=lambda text: isinstance(text, Comment)):
                comment.extract()
        
        # Process tags to remove while preserving content
        for tag in tags_to_remove:
            if tag and tag != 'comment':  # Skip empty tag names and 'comment'
                for element in soup.find_all(tag):
                    # Remove tag but keep its content
                    element.unwrap()
        
        # Process tags to remove with their content
        for tag in tags_to_remove_with_content:
            if tag and tag != 'comment':  # Skip empty tag names and 'comment'
                for element in soup.find_all(tag):
                    # Remove tag and its content
                    element.decompose()
        
        # Process tags for attribute cleaning based on mode
        if clean_attrs_mode == 'all':
            # Clean all tags
            for element in soup.find_all(True):  # Find all elements
                # Remove all attributes
                element.attrs = {}
                    
        elif clean_attrs_mode == 'selected':
            # Clean only selected tags
            for tag in attrs_exceptions or []:
                if tag:  # Skip empty tag names
                    for element in soup.find_all(tag):
                        # Remove all attributes
                        element.attrs = {}
                            
        elif clean_attrs_mode == 'all_except':
            # Clean all tags except those in tags_to_exclude
            for element in soup.find_all(True):
                if element.name not in (attrs_exceptions or []):
                    # Remove all attributes
                    element.attrs = {}
        
        # Convert back to string and write to output file
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(str(soup))
            
        return True
    except Exception as e:
        return str(e) 