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
                            QGroupBox, QScrollArea, QTabWidget, QRadioButton)
from PyQt5.QtCore import Qt, QMimeData
from PyQt5.QtGui import QDragEnterEvent, QDropEvent

def process_html_file(input_path, output_path, tags_to_remove, remove_with_content, clean_attrs_mode, attrs_exceptions=None):
    """
    Process HTML file by modifying specified tags using BeautifulSoup.
    
    Args:
        input_path: Path to the input file
        output_path: Path where processed file will be saved
        tags_to_remove: List of tags to remove
        remove_with_content: If True, removes tags with their content, otherwise preserves content
        clean_attrs_mode: Mode for cleaning attributes - 'all', 'selected', or 'all_except'
        attrs_exceptions: List of tags to exclude or include for attribute cleaning (depends on clean_attrs_mode)
    """
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
        
        # Process tags to remove
        for tag in tags_to_remove:
            if tag and tag != 'comment':  # Skip empty tag names and 'comment'
                for element in soup.find_all(tag):
                    if remove_with_content:
                        # Remove tag and its content
                        element.decompose()
                    else:
                        # Remove tag but keep its content
                        element.unwrap()
        
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
        self.setGeometry(100, 100, 800, 700)  # Optymalna wysokość dla zakładek
        
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

        # Utwórz główny widget
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)
        
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
        main_layout.addWidget(input_group)

        # Add recursive option
        self.recursive_checkbox = QCheckBox("Process subfolders recursively")
        self.recursive_checkbox.setChecked(True)
        input_layout.addWidget(self.recursive_checkbox)

        main_layout.addWidget(input_group)
        
        # Utwórz widget z zakładkami
        self.tabWidget = QTabWidget()
        main_layout.addWidget(self.tabWidget)
        
        # === PIERWSZA ZAKŁADKA: Tags to Remove ===
        remove_tab = QWidget()
        remove_layout = QVBoxLayout(remove_tab)
        
        # Add removal mode selection
        mode_layout = QHBoxLayout()
        mode_layout.addWidget(QLabel("Removal mode:"))
        self.removal_mode_combo = QComboBox()
        self.removal_mode_combo.addItems([
            "Remove tags only (preserve content)", 
            "Remove tags with content"
        ])
        mode_layout.addWidget(self.removal_mode_combo)
        remove_layout.addLayout(mode_layout)
        
        # Common HTML tags to remove
        common_tags_layout = QHBoxLayout()
        common_tags_layout.addWidget(QLabel("Common tags:"))
        
        self.removal_tag_checkboxes = {}
        common_tags = ["script", "style", "iframe", "comment", "header", "footer", "nav", "aside"]
        
        grid_layout = QGridLayout()
        row, col = 0, 0
        max_cols = 3
        
        for tag in common_tags:
            checkbox = QCheckBox(tag)
            self.removal_tag_checkboxes[tag] = checkbox
            grid_layout.addWidget(checkbox, row, col)
            col += 1
            if col >= max_cols:
                col = 0
                row += 1
        
        remove_layout.addLayout(grid_layout)
        
        # Custom tags to remove
        custom_tag_layout = QHBoxLayout()
        custom_tag_layout.addWidget(QLabel("Custom tag:"))
        self.removal_custom_input = QLineEdit()
        self.removal_custom_input.setPlaceholderText("Enter tag name(s) (e.g. 'div', 'span,p,a')...")
        self.removal_custom_input.returnPressed.connect(self.add_removal_tag)
        add_tag_button = QPushButton("Add")
        add_tag_button.clicked.connect(self.add_removal_tag)
        
        custom_tag_layout.addWidget(self.removal_custom_input)
        custom_tag_layout.addWidget(add_tag_button)
        remove_layout.addLayout(custom_tag_layout)
        
        # List of custom removal tags
        self.removal_tags_list = QListWidget()
        remove_tag_button = QPushButton("Remove Selected")
        remove_tag_button.clicked.connect(self.remove_removal_tag)
        remove_tag_button.setStyleSheet("background-color: #e74c3c; color: white;")
        
        remove_layout.addWidget(QLabel("Custom tags to remove:"))
        remove_layout.addWidget(self.removal_tags_list)
        remove_layout.addWidget(remove_tag_button)
        
        self.tabWidget.addTab(remove_tab, "Tags to Remove")
        
        # === DRUGA ZAKŁADKA: Tags to Clean Attributes ===
        clean_tab = QWidget()
        clean_layout = QVBoxLayout(clean_tab)
        
        # Mode selection for attribute cleaning
        mode_group = QGroupBox("Attribute Cleaning Mode")
        mode_layout = QVBoxLayout(mode_group)
        
        self.attr_mode_all = QRadioButton("Clean attributes from ALL tags")
        self.attr_mode_selected = QRadioButton("Clean attributes from SELECTED tags only")
        self.attr_mode_all_except = QRadioButton("Clean attributes from ALL tags EXCEPT selected")
        
        self.attr_mode_all.setChecked(True)  # Default option
        
        # Add modes to the layout
        mode_layout.addWidget(self.attr_mode_all)
        mode_layout.addWidget(self.attr_mode_selected)
        mode_layout.addWidget(self.attr_mode_all_except)
        
        # Connect signals
        self.attr_mode_all.toggled.connect(self.toggle_tag_selection)
        self.attr_mode_selected.toggled.connect(self.toggle_tag_selection)
        self.attr_mode_all_except.toggled.connect(self.toggle_tag_selection)
        
        clean_layout.addWidget(mode_group)
        
        # Tag selection container
        self.tag_selection_group = QGroupBox("Tag Selection")
        self.tag_selection_group.setEnabled(False)
        tag_selection_layout = QVBoxLayout(self.tag_selection_group)
        
        # Common tags for selection
        common_tags_layout = QGridLayout()
        common_tags = ["p", "div", "span", "a", "table", "tr", "td", "img", "h1", "h2", "h3", "ul", "ol", "li"]
        self.tag_selection_checkboxes = {}
        
        row, col = 0, 0
        max_cols = 5
        for tag in common_tags:
            checkbox = QCheckBox(tag)
            self.tag_selection_checkboxes[tag] = checkbox
            common_tags_layout.addWidget(checkbox, row, col)
            col += 1
            if col >= max_cols:
                col = 0
                row += 1
        
        tag_selection_layout.addLayout(common_tags_layout)
        
        # Custom tags input - similar to first tab
        custom_tag_layout = QHBoxLayout()
        custom_tag_layout.addWidget(QLabel("Custom tag:"))
        self.clean_custom_input = QLineEdit()
        self.clean_custom_input.setPlaceholderText("Enter tag name(s) (e.g. 'div', 'span,p,a')...")
        self.clean_custom_input.returnPressed.connect(self.add_clean_tag)
        add_clean_button = QPushButton("Add")
        add_clean_button.clicked.connect(self.add_clean_tag)
        
        custom_tag_layout.addWidget(self.clean_custom_input)
        custom_tag_layout.addWidget(add_clean_button)
        tag_selection_layout.addLayout(custom_tag_layout)
        
        # List of custom tags
        self.clean_tags_list = QListWidget()
        remove_clean_button = QPushButton("Remove Selected")
        remove_clean_button.clicked.connect(self.remove_clean_tag)
        remove_clean_button.setStyleSheet("background-color: #e74c3c; color: white;")
        
        tag_selection_layout.addWidget(QLabel("Custom tags:"))
        tag_selection_layout.addWidget(self.clean_tags_list)
        tag_selection_layout.addWidget(remove_clean_button)
        
        clean_layout.addWidget(self.tag_selection_group)
        
        self.tabWidget.addTab(clean_tab, "Tags to Clean Attributes")
        
        # Progress bar
        progress_group = QGroupBox("Progress")
        progress_layout = QVBoxLayout(progress_group)
        
        self.progress_bar = QProgressBar()
        progress_layout.addWidget(self.progress_bar)
        self.status_label = QLabel("Ready")
        progress_layout.addWidget(self.status_label)
        
        main_layout.addWidget(progress_group)
        
        # Start button
        start_button = QPushButton("Start Processing")
        start_button.clicked.connect(self.start_processing)
        main_layout.addWidget(start_button)
        
        # Add author label at the bottom
        main_layout.addWidget(self.author_label)

        self.adjustSize()  # Dostosuj rozmiar okna do zawartości

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

    def add_removal_tag(self):
        """Add custom tags to the removal list."""
        self._add_tags_to_list(self.removal_custom_input, self.removal_tags_list)
        
    def remove_removal_tag(self):
        """Remove selected tag from the removal list."""
        self._remove_selected_items(self.removal_tags_list)
        
    def add_clean_tag(self):
        """Add custom tags to the attribute cleaning list."""
        self._add_tags_to_list(self.clean_custom_input, self.clean_tags_list)
        
    def remove_clean_tag(self):
        """Remove selected tag from the attribute cleaning list."""
        self._remove_selected_items(self.clean_tags_list)
        
    def _add_tags_to_list(self, input_field, list_widget):
        """Helper method to add tags from input field to list widget."""
        tag_input = input_field.text().strip()
        if not tag_input:
            self.show_error("Please enter at least one tag name.")
            return
            
        # Split by comma and process each tag
        tag_list = [tag.strip() for tag in tag_input.split(',')]
        
        # Get existing tags to avoid duplicates
        existing_items = [list_widget.item(i).text() for i in range(list_widget.count())]
        
        added_count = 0
        duplicate_count = 0
        
        for tag in tag_list:
            if not tag:  # Skip empty tags
                continue
                
            if tag not in existing_items:
                list_widget.addItem(tag)
                added_count += 1
            else:
                duplicate_count += 1
                
        # Clear the input field
        input_field.clear()
        
        # Show summary message if needed
        if duplicate_count > 0:
            self.show_info(f"Added {added_count} tag(s). {duplicate_count} tag(s) were already in the list.")
        elif added_count > 0 and len(tag_list) > 1:
            self.status_label.setText(f"Added {added_count} tags")
            
    def _remove_selected_items(self, list_widget):
        """Helper method to remove selected items from a list widget."""
        selected_items = list_widget.selectedItems()
        for item in selected_items:
            list_widget.takeItem(list_widget.row(item))

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
        
        # Get tags to remove and clean
        tags_to_remove = []
        
        # Add checked common tags for removal
        for tag, checkbox in self.removal_tag_checkboxes.items():
            if checkbox.isChecked():
                tags_to_remove.append(tag)
                
        # Add custom tags for removal
        for i in range(self.removal_tags_list.count()):
            tags_to_remove.append(self.removal_tags_list.item(i).text())
            
        # Determine attribute cleaning mode and exceptions
        attr_clean_mode = 'all'  # Default
        attr_exceptions = []
        
        if self.attr_mode_selected.isChecked():
            attr_clean_mode = 'selected'
            attr_exceptions = self.get_selected_tags()
        elif self.attr_mode_all_except.isChecked():
            attr_clean_mode = 'all_except'
            attr_exceptions = self.get_selected_tags()
        
        # Validate selections...
        
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

        # Determine removal mode
        remove_with_content = self.removal_mode_combo.currentIndex() == 1  # 1 = "Remove tags with content"
        
        for input_path, rel_path in files:
            # Create output path preserving directory structure
            output_path = os.path.join(output_dir, rel_path)
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            result = process_html_file(input_path, output_path, tags_to_remove, 
                                      remove_with_content, attr_clean_mode, attr_exceptions)
            
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

    def toggle_tag_selection(self, checked):
        """Enable or disable tag selection based on selected mode."""
        if checked:
            # Enable tag selection only for 'selected' and 'all_except' modes
            self.tag_selection_group.setEnabled(
                self.attr_mode_selected.isChecked() or self.attr_mode_all_except.isChecked()
            )
            
            # Update label based on selected mode
            if self.attr_mode_selected.isChecked():
                self.tag_selection_group.setTitle("Tags TO Clean (select tags)")
            elif self.attr_mode_all_except.isChecked():
                self.tag_selection_group.setTitle("Tags to EXCLUDE from Cleaning (select tags to keep)")
        
    def get_selected_tags(self):
        """Get list of selected tags from checkboxes and list."""
        selected_tags = []
        
        # Get tags from checkboxes
        for tag, checkbox in self.tag_selection_checkboxes.items():
            if checkbox.isChecked():
                selected_tags.append(tag)
        
        # Get custom tags from list
        for i in range(self.clean_tags_list.count()):
            tag = self.clean_tags_list.item(i).text()
            if tag and tag not in selected_tags:
                selected_tags.append(tag)
                
        return selected_tags

def main():
    app = QApplication(sys.argv)
    window = FileProcessorWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
