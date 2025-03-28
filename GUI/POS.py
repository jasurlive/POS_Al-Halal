import qtawesome as qta
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLineEdit,
    QLabel,
    QListWidgetItem,
    QFrame,
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt, QTimer
from pos import POSHandler


class POSWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout(self)
        self.pos_handler = POSHandler()

        self.scanner_input = QLineEdit(self)
        self.scanner_input.setPlaceholderText("Scan Barcode Here...")
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

        self.scanned_items_list = QVBoxLayout()
        self.list_container = QWidget()
        self.list_container.setLayout(self.scanned_items_list)
        self.layout.addWidget(self.list_container)

        self.total_price_label = QLabel("Total Price: $0.00", self)
        self.total_price_label.setFont(QFont("Arial", 16))
        self.total_price_label.setStyleSheet("color: #28a745; font-weight: bold;")
        self.layout.addWidget(self.total_price_label)

        self.sell_button = QPushButton(" Sell", self)
        self.sell_button.setIcon(qta.icon("fa5s.money-bill-wave"))
        self.sell_button.setStyleSheet(
            "background-color: #2e9e26; color: white; padding: 12px; font-size: 16px; border-radius: 5px; border: none;"
        )
        self.sell_button.clicked.connect(self.process_sale)
        self.layout.addWidget(self.sell_button)

        self.scanned_items = {}

    def focus_barcode_input(self):
        self.scanner_input.setFocus()

    def scan_item(self):
        barcode = self.scanner_input.text().strip()
        if not barcode:
            return

        item = self.pos_handler.find_item_by_barcode(barcode)
        if item:
            item_name = item["Item Name"]
            sale_price = float(item["Sale Price"])

            if item_name in self.scanned_items:
                self.scanned_items[item_name]["quantity"] += 1
                self.scanned_items[item_name]["quantity_label"].setText(
                    f"x{self.scanned_items[item_name]['quantity']}"
                )
            else:
                item_widget = self.create_item_widget(item_name, sale_price)
                self.scanned_items_list.addWidget(item_widget)

                self.scanned_items[item_name] = {
                    "quantity": 1,
                    "price": sale_price,
                    "widget": item_widget,
                    "quantity_label": item_widget.findChild(
                        QLabel, f"quantity_{item_name}"
                    ),
                }

            self.update_total_price()
        else:
            error_label = QLabel("Product not found", self)
            error_label.setStyleSheet("color: red; font-size: 14px;")
            self.scanned_items_list.addWidget(error_label)

        self.scanner_input.clear()

    def create_item_widget(self, item_name, sale_price):
        item_frame = QFrame()
        item_frame.setStyleSheet(
            """
            background-color: #f8f9fa;
            color: #333;
            border: 1px solid #ccc;
            border-radius: 8px;
            padding: 10px;
        """
        )
        item_layout = QHBoxLayout(item_frame)

        name_label = QLabel(f"{item_name} - ${sale_price:.2f}", self)
        name_label.setFont(QFont("Arial", 14))

        quantity_label = QLabel("1", self, objectName=f"quantity_{item_name}")
        quantity_label.setFont(QFont("Arial", 14))
        quantity_label.setStyleSheet("color: #007bff; font-weight: bold;")

        increase_button = QPushButton("+", self)
        increase_button.setStyleSheet(
            "background-color: #28a745; color: white; font-size: 14px; padding: 10px;"
        )
        increase_button.clicked.connect(lambda: self.change_quantity(item_name, 1))

        decrease_button = QPushButton("-", self)
        decrease_button.setStyleSheet(
            "background-color: #dc3545; color: white; font-size: 14px; padding: 10px;"
        )
        decrease_button.clicked.connect(lambda: self.change_quantity(item_name, -1))

        item_layout.addWidget(name_label)
        item_layout.addStretch()
        item_layout.addWidget(decrease_button)
        item_layout.addWidget(quantity_label)
        item_layout.addWidget(increase_button)

        return item_frame

    def change_quantity(self, item_name, change):
        if item_name in self.scanned_items:
            self.scanned_items[item_name]["quantity"] += change
            if self.scanned_items[item_name]["quantity"] <= 0:
                self.remove_item(item_name)
            else:
                self.scanned_items[item_name]["quantity_label"].setText(
                    f"{self.scanned_items[item_name]['quantity']}"
                )
            self.update_total_price()

    def remove_item(self, item_name):
        item_widget = self.scanned_items[item_name]["widget"]
        self.scanned_items_list.removeWidget(item_widget)
        item_widget.deleteLater()
        del self.scanned_items[item_name]

    def update_total_price(self):
        self.total_price = sum(
            item["quantity"] * item["price"] for item in self.scanned_items.values()
        )
        self.total_price_label.setText(f"Total Price: ${self.total_price:.2f}")

    def set_button_style(self, text, icon_name, background_color):
        self.sell_button.setText(text)
        self.sell_button.setIcon(qta.icon(icon_name))
        self.sell_button.setStyleSheet(
            f"background-color: {background_color}; color: white; padding: 12px; font-size: 16px; border-radius: 5px; border: none;"
        )

    def process_sale(self):
        if not self.scanned_items:
            error_label = QLabel("No items to sell. Add items first!", self)
            error_label.setStyleSheet("color: red; font-size: 14px;")
            self.scanned_items_list.addWidget(error_label)
            return

        for item_name, item_data in self.scanned_items.items():
            for _ in range(item_data["quantity"]):
                self.pos_handler.update_inventory(item_name)

        while self.scanned_items_list.count():
            widget = self.scanned_items_list.takeAt(0).widget()
            if widget:
                widget.deleteLater()

        self.scanned_items.clear()
        self.total_price = 0.0
        self.total_price_label.setText("Total Price: $0.00")

        self.set_button_style("Success!", "fa5s.check-circle", "#2564b6")

        QTimer.singleShot(2000, self.reset_sell_button)
        self.focus_barcode_input()

    def reset_sell_button(self):
        self.set_button_style(" Sell", "fa5s.money-bill-wave", "#2e9e26")
