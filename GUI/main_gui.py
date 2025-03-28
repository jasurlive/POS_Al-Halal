import sys
import qtawesome as qta
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTabWidget
from PyQt6.QtGui import QPalette, QColor, QIcon
from PyQt6.QtCore import Qt
from GUI.POS import POSWidget
from GUI.inv import InventoryWidget


class MainApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("POS Al Halal")
        self.setGeometry(100, 100, 700, 500)

        # Set application-wide palette
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor("#f8f9fa"))
        self.setPalette(palette)

        # Set QtAwesome icon as window icon
        icon_pixmap = qta.icon("fa5s.shopping-cart").pixmap(64, 64)
        self.setWindowIcon(QIcon(icon_pixmap))

        # Main Layout
        self.main_layout = QVBoxLayout(self)

        # Create Tabs
        self.tabs = QTabWidget(self)

        # Add POS and Inventory tabs
        self.pos_widget = POSWidget()
        self.inventory_widget = InventoryWidget()

        self.tabs.addTab(
            self.pos_widget, qta.icon("fa5s.shopping-cart"), " Point of Sale"
        )
        self.tabs.addTab(self.inventory_widget, qta.icon("fa5s.box-open"), " Inventory")

        # Add Refresh Tab (Dummy Empty Widget)
        self.refresh_tab = QWidget()  # Empty widget since we just need the tab itself
        self.tabs.addTab(self.refresh_tab, qta.icon("fa5s.sync-alt"), " Refresh")

        # Styling for Tabs
        self.tabs.setStyleSheet(
            """
            QTabWidget::pane {
                border: 1px solid #ccc;
                background-color: #ffffff;
            }
            QTabBar::tab {
                background: #007bff;
                color: white;
                padding: 10px;
                border-radius: 5px;
            }
            QTabBar::tab:selected {
                background: #0056b3;
            }
            QTabBar::tab:hover {
                background: #0056b3;
                color: #e9ecef;
            }
        """
        )

        # Add Tabs to Layout
        self.main_layout.addWidget(self.tabs)

        # Set default focus on POS tab's barcode input
        self.pos_widget.focus_barcode_input()

        # Connect tab change event to override refresh tab behavior
        self.tabs.currentChanged.connect(self.handle_tab_change)

        self.previous_tab_index = 0  # Track the previously active tab index

    def handle_tab_change(self, index):
        """Handle tab change. If Refresh tab is clicked, refresh inputs and stay on the current tab."""
        if index == 2:  # Refresh tab
            self.clear_inputs()
            self.tabs.setCurrentIndex(
                self.previous_tab_index
            )  # Return to the previous tab
        else:
            self.previous_tab_index = index  # Update the previous tab index
            if index == 0:  # POS tab
                self.pos_widget.focus_barcode_input()
            elif index == 1:  # Inventory tab
                self.inventory_widget.focus_barcode_input()

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
