import qtawesome as qta
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTabWidget
from GUI.POS import POSWidget
from GUI.inv import InventoryWidget

from PyQt6.QtGui import QFont, QPalette, QColor, QIcon, QPixmap


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

        self.layout = QVBoxLayout(self)
        self.tabs = QTabWidget(self)

        # Apply styling
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

        # Add POS and Inventory tabs
        self.pos_widget = POSWidget()
        self.inventory_widget = InventoryWidget()

        self.tabs.addTab(
            self.pos_widget, qta.icon("fa5s.shopping-cart"), " Point of Sale"
        )
        self.tabs.addTab(self.inventory_widget, qta.icon("fa5s.box-open"), " Inventory")

        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)
