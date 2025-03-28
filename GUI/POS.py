import qtawesome as qta
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLineEdit,
    QLabel,
    QListWidget,
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import QTimer
from pos import POSHandler


class POSWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout(self)
        self.pos_handler = POSHandler()

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
        self.layout.addWidget(self.scanner_input)

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
        self.layout.addWidget(self.scanned_items_list)

        # Total Price Label
        self.total_price_label = QLabel("Total Price: $0.00", self)
        self.total_price_label.setFont(QFont("Arial", 16))
        self.total_price_label.setStyleSheet("color: #28a745; font-weight: bold;")
        self.layout.addWidget(self.total_price_label)

        # Sell Button
        self.sell_button = QPushButton(" Sell", self)
        self.sell_button.setIcon(qta.icon("fa5s.money-bill-wave"))
        self.sell_button.setStyleSheet(
            "background-color: #2e9e26; color: white; padding: 12px; font-size: 16px; border-radius: 5px; border: none;"
        )
        self.sell_button.clicked.connect(self.process_sale)
        self.layout.addWidget(self.sell_button)

        self.scanned_items = []
        self.total_price = 0.0

        # Auto-focus
        self.focus_timer = QTimer(self)
        self.focus_timer.timeout.connect(lambda: self.scanner_input.setFocus())
        self.focus_timer.start(500)

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

    def process_sale(self):
        for item_name, _ in self.scanned_items:
            self.pos_handler.update_inventory(item_name)
        self.scanned_items_list.clear()
        self.scanned_items = []
        self.total_price = 0.0
        self.total_price_label.setText("Total Price: $0.00")
