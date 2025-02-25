"""
HTML and Text File Processor
Author: Piotr Proszowski
"""

from PIL import Image, UnidentifiedImageError
import os
import sys
from bs4 import BeautifulSoup, Comment
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QPushButton, QLabel, QLineEdit, 
                            QProgressBar, QCheckBox, QFileDialog, QMessageBox,
                            QComboBox, QListWidget, QListWidgetItem, QGridLayout,
                            QGroupBox)
from PyQt5.QtCore import Qt, QMimeData
from PyQt5.QtGui import QDragEnterEvent, QDropEvent

def process_html_file(input_path, output_path, tags_to_remove):
    """Process HTML file by removing specified tags using BeautifulSoup, preserving the text content."""
    try:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(input_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Parse the HTML content
        soup = BeautifulSoup(content, 'html.parser')
        
        # Remove comments if specified
        if 'comment' in tags_to_remove:
            for comment in soup.find_all(text=lambda text: isinstance(text, Comment)):
                comment.extract()
        
        # Process the content by removing specified tags but preserving their content
        for tag in tags_to_remove:
            if tag and tag != 'comment':  # Skip empty tag names and 'comment' which we handled separately
                # Use unwrap() to remove the tag but keep its contents
                for element in soup.find_all(tag):
                    element.unwrap()
        
        # Convert back to string and write to output file
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(str(soup))
            
        return True
    except Exception as e:
        return str(e)

def is_supported_file(filename, extensions):
    """Check if a file has one of the supported extensions."""
    return os.path.splitext(filename)[1].lower() in extensions

class DragDropLineEdit(QLineEdit):
    """Custom QLineEdit that accepts drag and drop of files and folders."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.paths = []
        
    def dragEnterEvent(self, event: QDragEnterEvent):
        """Handle drag enter events for the line edit."""
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        
    def dropEvent(self, event: QDropEvent):
        """Handle drop events for the line edit."""
        self.paths = []
        paths_text = []
        
        for url in event.mimeData().urls():
            path = url.toLocalFile()
            self.paths.append(path)
            paths_text.append(path)
            
        self.setText("; ".join(paths_text))
        event.acceptProposedAction()

    def get_paths(self):
        """Return the list of dropped paths."""
        return self.paths

class FileProcessorWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("HTML & Text File Processor")
        self.setGeometry(100, 100, 800, 600)
        
        # Add author info label
        self.author_label = QLabel("© 2024 Piotr Proszowski")
        self.author_label.setAlignment(Qt.AlignRight)
        self.author_label.setStyleSheet("color: #666666; padding: 5px;")
        
        # Detect system theme
        app = QApplication.instance()
        self.is_dark_mode = app.palette().window().color().lightness() < 128
        
        # Set theme-dependent styles
        if self.is_dark_mode:
            self.setStyleSheet("""
                QMainWindow {
                    background-color: #1e1e1e;
                }
                QPushButton {
                    background-color: #4CAF50;
                    color: white;
                    padding: 8px 15px;
                    border-radius: 4px;
                    min-width: 80px;
                    border: none;
                }
                QPushButton:hover {
                    background-color: #45a049;
                }
                QLineEdit {
                    padding: 8px;
                    border: 1px solid #333;
                    border-radius: 4px;
                    background-color: #2d2d2d;
                    color: #ffffff;
                }
                QLineEdit:focus {
                    border: 1px solid #4CAF50;
                    background-color: #363636;
                }
                QProgressBar {
                    border: 1px solid #333;
                    border-radius: 4px;
                    text-align: center;
                    background-color: #2d2d2d;
                    color: #ffffff;
                }
                QProgressBar::chunk {
                    background-color: #4CAF50;
                    border-radius: 3px;
                }
                QLabel {
                    color: #ffffff;
                }
                QCheckBox {
                    color: #ffffff;
                }
                QCheckBox::indicator {
                    width: 18px;
                    height: 18px;
                    background-color: #2d2d2d;
                    border: 1px solid #333;
                }
                QCheckBox::indicator:checked {
                    background-color: #4CAF50;
                    border-radius: 2px;
                }
                QListWidget {
                    background-color: #2d2d2d;
                    color: #ffffff;
                    border: 1px solid #333;
                    border-radius: 4px;
                }
                QGroupBox {
                    color: #ffffff;
                    border: 1px solid #333;
                    border-radius: 4px;
                    margin-top: 1ex;
                    padding-top: 1ex;
                }
                QGroupBox::title {
                    subcontrol-origin: margin;
                    padding: 0 5px;
                }
                QComboBox {
                    padding: 6px;
                    border: 1px solid #333;
                    border-radius: 4px;
                    background-color: #2d2d2d;
                    color: #ffffff;
                }
                QComboBox::drop-down {
                    subcontrol-origin: padding;
                    subcontrol-position: top right;
                    width: 15px;
                    border-left-width: 1px;
                    border-left-color: #333;
                }
            """)
        else:
            self.setStyleSheet("""
                QMainWindow {
                    background-color: #ffffff;
                }
                QPushButton {
                    background-color: #4CAF50;
                    color: white;
                    padding: 8px 15px;
                    border-radius: 4px;
                    min-width: 80px;
                    border: none;
                }
                QPushButton:hover {
                    background-color: #45a049;
                }
                QLineEdit {
                    padding: 8px;
                    border: 1px solid #ddd;
                    border-radius: 4px;
                    background-color: #fafafa;
                }
                QLineEdit:focus {
                    border: 1px solid #4CAF50;
                    background-color: white;
                }
                QProgressBar {
                    border: 1px solid #ddd;
                    border-radius: 4px;
                    text-align: center;
                    background-color: #fafafa;
                }
                QProgressBar::chunk {
                    background-color: #4CAF50;
                    border-radius: 3px;
                }
                QLabel {
                    color: #333333;
                }
                QCheckBox {
                    color: #333333;
                }
                QCheckBox::indicator {
                    width: 18px;
                    height: 18px;
                }
                QCheckBox::indicator:checked {
                    background-color: #4CAF50;
                    border-radius: 2px;
                }
                QListWidget {
                    background-color: #fafafa;
                    border: 1px solid #ddd;
                    border-radius: 4px;
                }
                QGroupBox {
                    border: 1px solid #ddd;
                    border-radius: 4px;
                    margin-top: 1ex;
                    padding-top: 1ex;
                }
                QGroupBox::title {
                    subcontrol-origin: margin;
                    padding: 0 5px;
                }
                QComboBox {
                    padding: 6px;
                    border: 1px solid #ddd;
                    border-radius: 4px;
                    background-color: #fafafa;
                }
                QComboBox::drop-down {
                    subcontrol-origin: padding;
                    subcontrol-position: top right;
                    width: 15px;
                    border-left-width: 1px;
                    border-left-color: #ddd;
                }
            """)

        # Create main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)

        # File/Folder selection with drag and drop support
        input_group = QGroupBox("Input Files and Folders")
        input_layout = QVBoxLayout(input_group)
        
        path_layout = QHBoxLayout()
        self.path_input = DragDropLineEdit()
        self.path_input.setPlaceholderText("Drag & drop files/folders here or click Browse...")
        browse_button = QPushButton("Browse")
        browse_button.clicked.connect(self.browse_paths)
        path_layout.addWidget(self.path_input)
        path_layout.addWidget(browse_button)
        input_layout.addLayout(path_layout)
        
        # File type selection
        file_type_layout = QHBoxLayout()
        file_type_layout.addWidget(QLabel("Process files with extension:"))
        
        self.html_checkbox = QCheckBox("HTML (.html)")
        self.html_checkbox.setChecked(True)
        file_type_layout.addWidget(self.html_checkbox)
        
        self.txt_checkbox = QCheckBox("Text (.txt)")
        file_type_layout.addWidget(self.txt_checkbox)
        
        input_layout.addLayout(file_type_layout)
        layout.addWidget(input_group)

        # Add recursive option
        self.recursive_checkbox = QCheckBox("Process subfolders recursively")
        self.recursive_checkbox.setChecked(True)
        input_layout.addWidget(self.recursive_checkbox)

        # Tag removal options
        tag_group = QGroupBox("HTML Tags to Remove")
        tag_layout = QVBoxLayout(tag_group)

        # Common HTML tags
        common_tags_layout = QHBoxLayout()
        common_tags_layout.addWidget(QLabel("Common tags:"))
        
        self.tag_checkboxes = {}
        common_tags = ["script", "style", "iframe", "comment", "header", "footer", "nav", "aside"]
        
        grid_layout = QGridLayout()
        row, col = 0, 0
        max_cols = 3
        
        for tag in common_tags:
            checkbox = QCheckBox(tag)
            self.tag_checkboxes[tag] = checkbox
            grid_layout.addWidget(checkbox, row, col)
            col += 1
            if col >= max_cols:
                col = 0
                row += 1
        
        tag_layout.addLayout(grid_layout)
        
        # Custom tag input
        custom_tag_layout = QHBoxLayout()
        custom_tag_layout.addWidget(QLabel("Custom tag:"))
        self.custom_tag_input = QLineEdit()
        self.custom_tag_input.setPlaceholderText("Enter tag name (e.g. 'div', 'span')...")
        add_tag_button = QPushButton("Add")
        add_tag_button.clicked.connect(self.add_custom_tag)
        
        custom_tag_layout.addWidget(self.custom_tag_input)
        custom_tag_layout.addWidget(add_tag_button)
        tag_layout.addLayout(custom_tag_layout)
        
        # List of custom tags
        self.custom_tags_list = QListWidget()
        remove_tag_button = QPushButton("Remove Selected")
        remove_tag_button.clicked.connect(self.remove_custom_tag)
        remove_tag_button.setStyleSheet("background-color: #e74c3c; color: white;")
        
        tag_layout.addWidget(QLabel("Custom tags to remove:"))
        tag_layout.addWidget(self.custom_tags_list)
        tag_layout.addWidget(remove_tag_button)
        
        layout.addWidget(tag_group)

        # Progress bar
        progress_group = QGroupBox("Progress")
        progress_layout = QVBoxLayout(progress_group)
        
        self.progress_bar = QProgressBar()
        progress_layout.addWidget(self.progress_bar)
        self.status_label = QLabel("Ready")
        progress_layout.addWidget(self.status_label)
        
        layout.addWidget(progress_group)

        # Start button
        start_button = QPushButton("Start Processing")
        start_button.clicked.connect(self.start_processing)
        layout.addWidget(start_button)

        # Add author label at the bottom
        layout.addWidget(self.author_label)

    def browse_paths(self):
        """Browse for files or folders."""
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.ExistingFiles)
        if dialog.exec_():
            paths = dialog.selectedFiles()
            self.path_input.setText("; ".join(paths))
            self.path_input.paths = paths

    def show_error(self, message):
        QMessageBox.critical(self, "Error", message)

    def show_info(self, message):
        QMessageBox.information(self, "Information", message)

    def add_custom_tag(self):
        """Add a custom tag to the list."""
        tag = self.custom_tag_input.text().strip()
        if tag:
            # Check if tag already exists in the list
            items = [self.custom_tags_list.item(i).text() for i in range(self.custom_tags_list.count())]
            if tag not in items:
                self.custom_tags_list.addItem(tag)
                self.custom_tag_input.clear()
            else:
                self.show_info(f"Tag '{tag}' already in the list.")
        else:
            self.show_error("Please enter a tag name.")

    def remove_custom_tag(self):
        """Remove selected custom tag from the list."""
        selected_items = self.custom_tags_list.selectedItems()
        for item in selected_items:
            self.custom_tags_list.takeItem(self.custom_tags_list.row(item))

    def get_all_files(self, paths, recursive=False):
        """Get all supported files from the given paths."""
        supported_extensions = set()
        if self.html_checkbox.isChecked():
            supported_extensions.add('.html')
        if self.txt_checkbox.isChecked():
            supported_extensions.add('.txt')
            
        if not supported_extensions:
            return []
            
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

    def start_processing(self):
        """Start processing the selected files."""
        paths = self.path_input.get_paths()
        if not paths:
            self.show_error("Please select at least one file or folder")
            return

        recursive = self.recursive_checkbox.isChecked()
        
        # Get tags to remove
        tags_to_remove = []
        
        # Add checked common tags
        for tag, checkbox in self.tag_checkboxes.items():
            if checkbox.isChecked():
                tags_to_remove.append(tag)
                
        # Add custom tags
        for i in range(self.custom_tags_list.count()):
            tags_to_remove.append(self.custom_tags_list.item(i).text())
            
        if not tags_to_remove:
            self.show_error("Please select at least one tag to remove")
            return
            
        # Handle special case for comments
        if "comment" in tags_to_remove:
            tags_to_remove.remove("comment")
            # We'll handle comments separately in the processing function
            
        # Get all files to process
        files = self.get_all_files(paths, recursive)
        
        total_files = len(files)
        
        if total_files == 0:
            self.show_info("No supported files found in selected paths")
            return

        # Create output directory
        output_dir = os.path.join(os.path.dirname(paths[0]), "processed")
        os.makedirs(output_dir, exist_ok=True)

        processed = 0
        errors = 0
        self.progress_bar.setMaximum(total_files)
        self.progress_bar.setValue(0)

        for input_path, rel_path in files:
            # Create output path preserving directory structure
            output_path = os.path.join(output_dir, rel_path)
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            result = process_html_file(input_path, output_path, tags_to_remove)
            
            if result is not True:
                self.show_error(f"Error processing {rel_path}: {result}")
                errors += 1
            
            processed += 1
            self.progress_bar.setValue(processed)
            self.status_label.setText(f"Processing: {processed}/{total_files}")
            QApplication.processEvents()

        success_count = processed - errors
        self.show_info(f"Processed {success_count} files successfully" + 
                      (f", {errors} errors" if errors > 0 else ""))
        self.status_label.setText("Ready")
        self.progress_bar.setValue(0)

def main():
    app = QApplication(sys.argv)
    window = FileProcessorWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
