import sys
import qtawesome as qta
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLineEdit,
    QLabel,
    QTabWidget,
    QListWidget,
)
from PyQt6.QtGui import QFont, QPalette, QColor, QIcon
from PyQt6.QtCore import QTimer
from pos import POSHandler
from inventory import InventoryHandler


class POSApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("POS Al Halal")
        self.setGeometry(100, 100, 700, 500)

        # Set application-wide palette
        palette = self.palette()
        palette.setColor(
            QPalette.ColorRole.Window, QColor("#f8f9fa")
        )  # Light background
        self.setPalette(palette)

        self.layout = QVBoxLayout()
        self.tabs = QTabWidget(self)
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
        self.layout.addWidget(self.tabs)

        # Point of Sale Tab (with Icon)
        self.pos_tab = QWidget()
        self.tabs.addTab(self.pos_tab, qta.icon("fa5s.shopping-cart"), " Point of Sale")
        self.pos_layout = QVBoxLayout()
        self.pos_tab.setLayout(self.pos_layout)

        # Inventory Tab (with Icon)
        self.inventory_tab = QWidget()
        self.tabs.addTab(self.inventory_tab, qta.icon("fa5s.box-open"), " Inventory")
        self.inventory_layout = QVBoxLayout()
        self.inventory_tab.setLayout(self.inventory_layout)

        # Scanner Input
        self.scanner_input = QLineEdit(self)
        self.scanner_input.setPlaceholderText("Scan Item ID Here...")
        self.scanner_input.setStyleSheet(
            """
            font-size: 18px;
            padding: 12px;
            border: 2px solid #007bff;
            border-radius: 5px;
            background-color: #ffffff;
            color: #333;
        """
        )
        self.scanner_input.setFocus()
        self.scanner_input.returnPressed.connect(self.scan_item)
        self.pos_layout.addWidget(self.scanner_input)

        # Scanned Items List
        self.scanned_items_list = QListWidget(self)
        self.scanned_items_list.setStyleSheet(
            """
            font-size: 14px;
            padding: 10px;
            background-color: #ffffff;
            color: #333;
            border: 1px solid #ccc;
            border-radius: 5px;
        """
        )
        self.pos_layout.addWidget(self.scanned_items_list)

        # Total Price Label
        self.total_price_label = QLabel("Total Price: $0.00", self)
        self.total_price_label.setFont(QFont("Arial", 16))
        self.total_price_label.setStyleSheet(
            """
            color: #28a745;
            font-weight: bold;
        """
        )
        self.pos_layout.addWidget(self.total_price_label)

        # Sell Button (with Icon)
        self.sell_button = QPushButton(self)
        self.sell_button.setText(" Sell")
        self.sell_button.setIcon(qta.icon("fa5s.money-bill-wave"))
        self.sell_button.setStyleSheet(
            """
            background-color: #2e9e26;
            color: white;
            padding: 12px;
            font-size: 16px;
            border-radius: 5px;
            border: none;
        """
        )
        self.sell_button.clicked.connect(self.process_sale)
        self.pos_layout.addWidget(self.sell_button)

        # Inventory Inputs
        input_style = """
            padding: 10px;
            border: 2px solid #17a2b8;
            border-radius: 5px;
            background-color: #ffffff;
            color: #333;
        """
        self.barcode_input = QLineEdit(self)
        self.barcode_input.setPlaceholderText("Barcode")
        self.barcode_input.setStyleSheet(input_style)
        self.inventory_layout.addWidget(self.barcode_input)

        self.item_name_input = QLineEdit(self)
        self.item_name_input.setPlaceholderText("Item Name")
        self.item_name_input.setStyleSheet(input_style)
        self.inventory_layout.addWidget(self.item_name_input)

        self.original_price_input = QLineEdit(self)
        self.original_price_input.setPlaceholderText("Original Price")
        self.original_price_input.setStyleSheet(input_style)
        self.inventory_layout.addWidget(self.original_price_input)

        self.sale_price_input = QLineEdit(self)
        self.sale_price_input.setPlaceholderText("Sale Price")
        self.sale_price_input.setStyleSheet(input_style)
        self.inventory_layout.addWidget(self.sale_price_input)

        self.inventory_quantity_input = QLineEdit(self)
        self.inventory_quantity_input.setPlaceholderText("Inventory Quantity")
        self.inventory_quantity_input.setStyleSheet(input_style)
        self.inventory_layout.addWidget(self.inventory_quantity_input)

        # Add Inventory Button (with Icon)
        self.add_inventory_button = QPushButton(self)
        self.add_inventory_button.setText(" Add New Item")
        self.add_inventory_button.setIcon(qta.icon("fa5s.plus-circle"))
        self.add_inventory_button.setStyleSheet(
            """
            background-color: #ffc107;
            color: white;
            padding: 12px;
            font-size: 16px;
            border-radius: 5px;
            border: none;
        """
        )
        self.add_inventory_button.clicked.connect(self.add_inventory_item)
        self.inventory_layout.addWidget(self.add_inventory_button)

        self.setLayout(self.layout)

        self.pos_handler = POSHandler()
        self.inventory_handler = InventoryHandler()

        self.scanned_items = []
        self.total_price = 0.0

        self.focus_timer = QTimer(self)
        self.focus_timer.timeout.connect(self.manage_focus)
        self.focus_timer.start(500)
        self.barcode_focused_once = False  # Track if barcode input has been focused

    def manage_focus(self):
        if self.tabs.currentWidget() == self.pos_tab:
            self.scanner_input.setFocus()
        elif (
            self.tabs.currentWidget() == self.inventory_tab
            and not self.barcode_focused_once
        ):
            self.barcode_input.setFocus()
            if self.barcode_input.text():  # Stop focusing if barcode input is filled
                self.barcode_focused_once = True

    def scan_item(self):
        barcode = self.scanner_input.text()
        if barcode:
            item = self.pos_handler.find_item_by_barcode(barcode)
            if item:
                item_name = item["Item Name"]
                sale_price = float(item["Sale Price"])
                self.scanned_items.append((item_name, sale_price))
                self.scanned_items_list.addItem(f"{item_name} - ${sale_price:.2f}")
                self.total_price += sale_price
                self.total_price_label.setText(f"Total Price: ${self.total_price:.2f}")
            else:
                self.scanned_items_list.addItem("Product not found")
            self.scanner_input.clear()
            QTimer.singleShot(100, lambda: self.scanner_input.setFocus())

    def process_sale(self):
        for item_name, _ in self.scanned_items:
            self.pos_handler.update_inventory(item_name)
        self.scanned_items_list.clear()
        self.scanned_items = []
        self.total_price = 0.0
        self.total_price_label.setText("Total Price: $0.00")

    def add_inventory_item(self):
        self.inventory_handler.add_inventory_item(
            self.item_name_input.text(),
            self.barcode_input.text(),
            self.original_price_input.text(),
            self.sale_price_input.text(),
            self.inventory_quantity_input.text(),
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = POSApp()
    window.show()
    sys.exit(app.exec())
