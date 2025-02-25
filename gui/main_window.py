"""
Main Application Window
Defines the UI components and application logic
"""

import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QPushButton, QLabel, QProgressBar, 
                            QCheckBox, QFileDialog, QMessageBox, QComboBox, 
                            QListWidget, QGroupBox, QTabWidget, QRadioButton, 
                            QGridLayout, QLineEdit, QListWidgetItem)
from PyQt5.QtCore import Qt

from gui.drag_drop import DragDropLineEdit
from processors.html_processor import process_html_file
from utils.file_utils import get_all_files

class FileProcessorWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("HTML & Text File Processor")
        self.setGeometry(100, 100, 800, 700)
        
        # Add author info label
        self.author_label = QLabel("© 2024 Piotr Proszowski")
        self.author_label.setAlignment(Qt.AlignRight)
        self.author_label.setStyleSheet("color: #666666; padding: 5px;")
        
        # Detect system theme
        app = QApplication.instance()
        self.is_dark_mode = app.palette().window().color().lightness() < 128
        
        # Set theme-dependent styles
        self._setup_styles()
        
        # Create UI components
        self._create_ui()
        
        self.adjustSize()  # Dostosuj rozmiar okna do zawartości

    def _setup_styles(self):
        """Set up application styles based on theme."""
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
                    color: #ddd;
                }
                QCheckBox, QRadioButton, QLabel {
                    color: #ddd;
                }
                QGroupBox {
                    border: 1px solid #444;
                    border-radius: 4px;
                    margin-top: 1em;
                    padding-top: 10px;
                    color: #ddd;
                }
                QGroupBox::title {
                    subcontrol-origin: margin;
                    left: 10px;
                    padding: 0 3px 0 3px;
                }
                QListWidget {
                    background-color: #2d2d2d;
                    border: 1px solid #333;
                    color: #ddd;
                }
                QTabWidget::pane {
                    border: 1px solid #444;
                    background-color: #1e1e1e;
                }
                QTabBar::tab {
                    background-color: #333;
                    color: #ddd;
                    padding: 8px 12px;
                    margin-right: 2px;
                }
                QTabBar::tab:selected {
                    background-color: #4CAF50;
                }
                QComboBox {
                    background-color: #2d2d2d;
                    color: #ddd;
                    padding: 5px;
                    border: 1px solid #333;
                    border-radius: 4px;
                }
                QProgressBar {
                    border: 1px solid #333;
                    border-radius: 4px;
                    text-align: center;
                    background-color: #2d2d2d;
                }
                QProgressBar::chunk {
                    background-color: #4CAF50;
                    width: 1px;
                }
            """)
        else:
            self.setStyleSheet("""
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
                }
                QGroupBox {
                    border: 1px solid #ddd;
                    border-radius: 4px;
                    margin-top: 1em;
                    padding-top: 10px;
                }
                QGroupBox::title {
                    subcontrol-origin: margin;
                    left: 10px;
                    padding: 0 3px 0 3px;
                }
                QListWidget {
                    border: 1px solid #ddd;
                }
                QTabWidget::pane {
                    border: 1px solid #ddd;
                }
                QTabBar::tab {
                    background-color: #eee;
                    padding: 8px 12px;
                    margin-right: 2px;
                }
                QTabBar::tab:selected {
                    background-color: #4CAF50;
                    color: white;
                }
                QProgressBar {
                    border: 1px solid #ddd;
                    border-radius: 4px;
                    text-align: center;
                }
                QProgressBar::chunk {
                    background-color: #4CAF50;
                    width: 1px;
                }
            """)

    def _create_ui(self):
        """Create the user interface components."""
        # Utwórz główny widget
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)
        
        # File/Folder selection with drag and drop support
        self._create_input_section(main_layout)
        
        # Create tab widget for tag operations
        self.tabWidget = QTabWidget()
        main_layout.addWidget(self.tabWidget)
        
        # Create tabs for tag removal and attribute cleaning
        self._create_tag_removal_tab()
        self._create_attribute_cleaning_tab()
        
        # Progress bar
        self._create_progress_section(main_layout)
        
        # Start button
        start_button = QPushButton("Start Processing")
        start_button.clicked.connect(self.start_processing)
        main_layout.addWidget(start_button)
        
        # Add author label at the bottom
        main_layout.addWidget(self.author_label)

    def _create_input_section(self, main_layout):
        """Create the input files/folders selection section."""
        input_group = QGroupBox("Input Files and Folders")
        input_layout = QVBoxLayout(input_group)
        
        # Path input with drag and drop
        path_layout = QHBoxLayout()
        self.path_input = DragDropLineEdit()
        self.path_input.setPlaceholderText("Drag and drop files/folders here or use Browse button...")
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
        self.txt_checkbox = QCheckBox("Text (.txt)")
        
        file_type_layout.addWidget(self.html_checkbox)
        file_type_layout.addWidget(self.txt_checkbox)
        file_type_layout.addStretch()
        
        input_layout.addLayout(file_type_layout)
        
        # Add recursive option
        self.recursive_checkbox = QCheckBox("Process subfolders recursively")
        input_layout.addWidget(self.recursive_checkbox)
        
        main_layout.addWidget(input_group)

    def _create_tag_removal_tab(self):
        """Create tab for tag removal options."""
        remove_tab = QWidget()
        remove_layout = QVBoxLayout(remove_tab)
        
        # Remove general mode selection (będziemy mieć per-tag)
        # Instead add explanation text
        remove_layout.addWidget(QLabel("Select which tags to remove and how:"))
        
        # Common HTML tags to remove
        common_tags_layout = QGridLayout()
        
        self.removal_tag_checkboxes = {}
        self.removal_mode_checkboxes = {}  # Nowy słownik dla trybu usuwania
        common_tags = ["script", "style", "iframe", "comment", "header", "footer", "nav", "aside"]
        
        # Create column headers
        common_tags_layout.addWidget(QLabel("Tag"), 0, 0)
        common_tags_layout.addWidget(QLabel("Remove"), 0, 1)
        common_tags_layout.addWidget(QLabel("With content"), 0, 2)
        
        for i, tag in enumerate(common_tags):
            row = i + 1  # Start from row 1 (after headers)
            
            # Tag name label
            tag_label = QLabel(tag)
            common_tags_layout.addWidget(tag_label, row, 0)
            
            # Checkbox to select tag for removal
            checkbox = QCheckBox()
            self.removal_tag_checkboxes[tag] = checkbox
            common_tags_layout.addWidget(checkbox, row, 1)
            
            # Checkbox to select removal mode (with content)
            mode_checkbox = QCheckBox()
            mode_checkbox.setEnabled(False)  # Initially disabled
            self.removal_mode_checkboxes[tag] = mode_checkbox
            common_tags_layout.addWidget(mode_checkbox, row, 2)
            
            # Connect checkbox to enable/disable mode selection
            checkbox.stateChanged.connect(lambda state, tag=tag: self.toggle_removal_mode(tag, state))
        
        remove_layout.addLayout(common_tags_layout)
        
        # Custom tags section stays mostly the same, but add mode selection
        custom_tag_section = QGroupBox("Custom Tags")
        custom_tag_layout = QVBoxLayout(custom_tag_section)
        
        input_row = QHBoxLayout()
        input_row.addWidget(QLabel("Custom tag:"))
        self.removal_custom_input = QLineEdit()
        self.removal_custom_input.setPlaceholderText("Enter tag name (e.g. 'div')")
        self.removal_custom_input.returnPressed.connect(self.add_removal_tag)
        input_row.addWidget(self.removal_custom_input)
        
        # Mode selection for custom tag
        self.custom_tag_with_content = QCheckBox("Remove with content")
        input_row.addWidget(self.custom_tag_with_content)
        
        add_tag_button = QPushButton("Add")
        add_tag_button.clicked.connect(self.add_removal_tag)
        input_row.addWidget(add_tag_button)
        
        custom_tag_layout.addLayout(input_row)
        
        # List of custom removal tags (now with two columns: tag name and removal mode)
        self.removal_tags_list = QListWidget()
        remove_tag_button = QPushButton("Remove Selected")
        remove_tag_button.clicked.connect(self.remove_removal_tag)
        remove_tag_button.setStyleSheet("background-color: #e74c3c; color: white;")
        
        custom_tag_layout.addWidget(QLabel("Custom tags to remove:"))
        custom_tag_layout.addWidget(self.removal_tags_list)
        custom_tag_layout.addWidget(remove_tag_button)
        
        remove_layout.addWidget(custom_tag_section)
        
        self.tabWidget.addTab(remove_tab, "Tags to Remove")

    def _create_attribute_cleaning_tab(self):
        """Create the tab for attribute cleaning options."""
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

    def _create_progress_section(self, main_layout):
        """Create the progress bar section."""
        progress_group = QGroupBox("Progress")
        progress_layout = QVBoxLayout(progress_group)
        
        self.progress_bar = QProgressBar()
        progress_layout.addWidget(self.progress_bar)
        self.status_label = QLabel("Ready")
        progress_layout.addWidget(self.status_label)
        
        main_layout.addWidget(progress_group)

    # Event handlers and utility methods
    def browse_paths(self):
        """Browse for files or folders."""
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.ExistingFiles)
        if dialog.exec_():
            paths = dialog.selectedFiles()
            self.path_input.setText("; ".join(paths))
            self.path_input.paths = paths

    def show_error(self, message):
        """Show an error message dialog."""
        QMessageBox.critical(self, "Error", message)

    def show_info(self, message):
        """Show an information message dialog."""
        QMessageBox.information(self, "Information", message)

    def add_removal_tag(self):
        """Add custom tag to the removal list."""
        tag_input = self.removal_custom_input.text().strip()
        if not tag_input:
            self.show_error("Please enter at least one tag name.")
            return
        
        # Add with indicator of removal mode
        with_content = self.custom_tag_with_content.isChecked()
        display_text = f"{tag_input} {'(with content)' if with_content else ''}"
        
        # Store actual data as tag_name|mode where mode is 1 for with_content, 0 for without
        item_data = f"{tag_input}|{1 if with_content else 0}"
        
        # Get existing tags to avoid duplicates
        existing_items = [self.removal_tags_list.item(i).text().split()[0] for i in range(self.removal_tags_list.count())]
        
        if tag_input not in existing_items:
            item = QListWidgetItem(display_text)
            item.setData(Qt.UserRole, item_data)  # Store the actual data
            self.removal_tags_list.addItem(item)
            self.removal_custom_input.clear()
            self.custom_tag_with_content.setChecked(False)
        else:
            self.show_info(f"Tag '{tag_input}' is already in the list.")
        
    def remove_removal_tag(self):
        """Remove selected tag from the removal list."""
        selected_items = self.removal_tags_list.selectedItems()
        for item in selected_items:
            self.removal_tags_list.takeItem(self.removal_tags_list.row(item))

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

    def toggle_removal_mode(self, tag, state):
        """Enable or disable removal mode checkbox based on tag checkbox state."""
        self.removal_mode_checkboxes[tag].setEnabled(state == Qt.Checked)
        if state != Qt.Checked:
            self.removal_mode_checkboxes[tag].setChecked(False)

    def start_processing(self):
        """Start processing the selected files."""
        # Validate input
        paths = self.path_input.get_paths()
        if not paths:
            self.show_error("Please select at least one file or folder")
            return

        recursive = self.recursive_checkbox.isChecked()
        
        # Get supported file extensions
        supported_extensions = set()
        if self.html_checkbox.isChecked():
            supported_extensions.add('.html')
        if self.txt_checkbox.isChecked():
            supported_extensions.add('.txt')
            
        if not supported_extensions:
            self.show_error("Please select at least one file type to process")
            return
        
        # Get tags to remove (split into two lists)
        tags_to_remove = []
        tags_to_remove_with_content = []
        
        # Add checked common tags for removal
        for tag, checkbox in self.removal_tag_checkboxes.items():
            if checkbox.isChecked():
                if self.removal_mode_checkboxes[tag].isChecked():
                    tags_to_remove_with_content.append(tag)
                else:
                    tags_to_remove.append(tag)
                
        # Add custom tags for removal
        for i in range(self.removal_tags_list.count()):
            item = self.removal_tags_list.item(i)
            item_data = item.data(Qt.UserRole).split('|')
            tag = item_data[0]
            with_content = item_data[1] == '1'
            
            if with_content:
                tags_to_remove_with_content.append(tag)
            else:
                tags_to_remove.append(tag)
            
        # Determine attribute cleaning mode and exceptions
        attr_clean_mode = 'all'  # Default
        attr_exceptions = []
        
        if self.attr_mode_selected.isChecked():
            attr_clean_mode = 'selected'
            attr_exceptions = self.get_selected_tags()
        elif self.attr_mode_all_except.isChecked():
            attr_clean_mode = 'all_except'
            attr_exceptions = self.get_selected_tags()
        
        # Validate selections based on current tab
        current_tab_index = self.tabWidget.currentIndex()
        
        if current_tab_index == 0 and not tags_to_remove and not tags_to_remove_with_content:
            self.show_error("Please select at least one tag to remove")
            return
        elif current_tab_index == 1:
            # On attribute cleaning tab
            if attr_clean_mode == 'all':
                # In "Clean all tags" mode, no need to select tags
                pass
            elif not attr_exceptions:
                # In "selected" or "all_except" modes, we need selected tags
                if attr_clean_mode == 'selected':
                    self.show_error("Please select at least one tag to clean attributes from")
                else:  # attr_clean_mode == 'all_except'
                    self.show_error("Please select at least one tag to exclude from cleaning")
                return
        
        # Get all files to process
        files = get_all_files(paths, recursive, supported_extensions)
        
        total_files = len(files)
        
        if total_files == 0:
            self.show_info("No supported files found in selected paths")
            return

        # Create output directory
        output_dir = os.path.join(os.path.dirname(paths[0]), "processed")
        os.makedirs(output_dir, exist_ok=True)

        # Initialize progress tracking
        processed = 0
        errors = 0
        self.progress_bar.setMaximum(total_files)
        self.progress_bar.setValue(0)

        # Process each file
        for input_path, rel_path in files:
            # Create output path preserving directory structure
            output_path = os.path.join(output_dir, rel_path)
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            result = process_html_file(input_path, output_path, 
                                      tags_to_remove, tags_to_remove_with_content,
                                      attr_clean_mode, attr_exceptions)
            
            if result is not True:
                self.show_error(f"Error processing {rel_path}: {result}")
                errors += 1
            
            processed += 1
            self.progress_bar.setValue(processed)
            self.status_label.setText(f"Processing: {processed}/{total_files}")
            QApplication.processEvents()

        # Show completion message
        success_count = processed - errors
        self.show_info(f"Processed {success_count} files successfully" + 
                      (f", {errors} errors" if errors > 0 else ""))
        self.status_label.setText("Ready")
        self.progress_bar.setValue(0) 