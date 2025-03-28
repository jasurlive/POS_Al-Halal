import sys
import qtawesome as qta
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTabWidget, QPushButton, QHBoxLayout
from PyQt6.QtGui import QPalette, QColor, QIcon, QCursor
from PyQt6.QtCore import Qt, QTimer
from GUI.POS import POSWidget
from GUI.inv import InventoryWidget


class MainApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("POS Al Halal")
        self.setGeometry(100, 100, 700, 500)

        # Set application-wide palette
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor("#fffdee"))
        self.setPalette(palette)

        # Set QtAwesome icon as window icon
        icon_pixmap = qta.icon("fa5s.shopping-cart").pixmap(64, 64)
        self.setWindowIcon(QIcon(icon_pixmap))

        # Main Layout
        self.main_layout = QVBoxLayout(self)

        # Create Tabs
        self.tabs = QTabWidget(self)
        self.tabs.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        # Add POS and Inventory tabs
        self.pos_widget = POSWidget()
        self.inventory_widget = InventoryWidget()

        self.tabs.addTab(
            self.pos_widget, qta.icon("fa5s.shopping-cart"), "Point of Sale"
        )
        self.tabs.addTab(self.inventory_widget, qta.icon("fa5s.box-open"), "Inventory")

        # Replace Clear Tab with a Button Styled as a Tab
        self.clear_button = QPushButton(" Clear")
        self.clear_button.setObjectName("clearButton")
        self.clear_button.setIcon(qta.icon("fa5s.paint-brush"))
        self.clear_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.clear_button.clicked.connect(self.handle_clear_click)

        # Add Clear Button as a Fake Tab
        self.tabs.setCornerWidget(self.clear_button, Qt.Corner.TopRightCorner)

        # Styling for Tabs and Clear Button
        self.tabs.setStyleSheet(
            """
            QTabWidget::pane {
                border: 1px solid #ccc;
                background-color: #e8ffec;
                padding: 10px;
                border-radius: 10px;
                alignment: center;
            }
             QTabBar {
                border: 1px solid #cccccc;
                border-radius: 8px;
    }
            QTabBar::tab, #clearButton {
                background: #007bff;
                color: white;
                height: 50px;
                font-size: 18px;
                border: 1px solid #007bff;
                margin: 5px;
                border-radius: 5px;
                width: 150px;
                margin: auto;
            }
            QTabBar::tab:selected {
                background: #00b365;
                border: 1px solid #ffffff;
            }
            QTabBar::tab:hover, #clearButton:hover {
                background: #0056b3;
                border: 1px solid #6effd3;
                color: #e9ecef;
            }
        """
        )

        # Add Tabs to Layout
        self.main_layout.addWidget(self.tabs)

        # Set default focus on POS tab's barcode input
        self.pos_widget.focus_barcode_input()

        self.previous_tab_index = 0  # Track the previously active tab index

    def handle_clear_click(self):
        """Change the button text and icon on click, then revert after a delay."""
        self.clear_button.setText(" Cleared!")
        self.clear_button.setIcon(qta.icon("fa5s.check-circle"))

        QTimer.singleShot(2000, self.reset_clear_button)  # Reset after 2 seconds

        # Track the currently active tab
        active_tab = self.tabs.currentIndex()

        # Perform clearing action
        self.clear_inputs()

        # Refocus the barcode input based on the active tab
        if active_tab == 0:  # POS tab
            self.pos_widget.focus_barcode_input()
        elif active_tab == 1:  # Inventory tab
            self.inventory_widget.focus_barcode_input()

    def reset_clear_button(self):
        """Reset the button back to original state."""
        self.clear_button.setText(" Clear")
        self.clear_button.setIcon(qta.icon("fa5s.paint-brush"))

    def clear_inputs(self):
        """Clear all input fields in POS and Inventory tabs."""
        self.pos_widget.clear_inputs()
        self.inventory_widget.clear_inputs()


if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec())
