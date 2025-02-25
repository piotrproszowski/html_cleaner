"""
Drag and Drop Components
Custom widgets that support file drag and drop
"""

from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QDragEnterEvent, QDropEvent

class DragDropLineEdit(QLineEdit):
    """Custom QLineEdit that accepts drag and drop of files and folders."""
    
    def __init__(self, parent=None):
        """Initialize the drag and drop line edit."""
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