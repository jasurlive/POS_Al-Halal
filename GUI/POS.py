from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLineEdit,
    QLabel,
    QFrame,
    QScrollArea,
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt, QTimer
import qtawesome as qta
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

        # Scroll Area for Items
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("border: none;")
        self.list_container = QWidget()
        self.list_container.setStyleSheet("background-color: white;")
        self.scanned_items_list = QVBoxLayout(self.list_container)
        self.scanned_items_list.setContentsMargins(0, 0, 0, 0)

        self.scroll_area.setWidget(self.list_container)
        self.scroll_area.setFixedHeight(300)
        self.scroll_area.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOn
        )

        self.layout.addWidget(self.scroll_area)

        self.total_price_label = QLabel("Total: 0.00 KRW", self)
        self.total_price_label.setFont(QFont("Arial", 16))
        self.total_price_label.setStyleSheet(
            "color: #1a3a7f; font-weight: bold; background-color: #f5f8fa; border: 1px solid #ddd; border-radius: 8px; padding: 10px;"
        )
        self.total_price_label.setFixedHeight(50)
        self.total_price_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.total_price_label)

        self.sell_button = QPushButton(" Sell", self)
        self.sell_button.setObjectName("sellButton")
        self.sell_button.setIcon(qta.icon("fa5s.money-bill-wave"))
        self.sell_button.clicked.connect(self.process_sale)
        self.layout.addWidget(self.sell_button)

        self.scanned_items = {}

        self.setStyleSheet(
            """
            QPushButton#sellButton {
                background-color: #25a21c;
                color: white;
                padding: 12px;
                font-size: 25px;
                font-weight: bold;
                height: 50px;
                border-radius: 5px;
                border: none;
            }
            QPushButton#sellButton[success="true"] {
                background-color: #2564b6;
            }
            """
        )

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
                    f"{self.scanned_items[item_name]['quantity']}"
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
        item_frame.setFixedHeight(50)
        item_frame.setStyleSheet(
            """
            background-color: #f8f9fa;
            color: #333;
            border: 1px solid #ccc;
            border-radius: 5px;
            padding: 5px;
        """
        )

        item_layout = QHBoxLayout(item_frame)
        item_layout.setContentsMargins(5, 5, 5, 5)
        item_layout.setSpacing(10)

        name_label = QLabel(f"{item_name} - {sale_price:.2f} KRW", self)
        name_label.setFont(QFont("Arial", 12))

        decrease_button = QPushButton("-", self)
        decrease_button.setFixedSize(30, 30)
        decrease_button.setStyleSheet(
            "background-color: #dc3545; color: white; font-size: 14px; border-radius: 3px;"
        )
        decrease_button.clicked.connect(lambda: self.change_quantity(item_name, -1))

        quantity_label = QLabel("1", self, objectName=f"quantity_{item_name}")
        quantity_label.setFont(QFont("Arial", 12))
        quantity_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        quantity_label.setFixedWidth(30)

        increase_button = QPushButton("+", self)
        increase_button.setFixedSize(30, 30)
        increase_button.setStyleSheet(
            "background-color: #28a745; color: white; font-size: 14px; border-radius: 3px;"
        )
        increase_button.clicked.connect(lambda: self.change_quantity(item_name, 1))

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
        self.total_price_label.setText(f"Total: {self.total_price:.2f} KRW")

    def process_sale(self):
        if not self.scanned_items:
            error_label = QLabel("No items to sell. Add items first!", self)
            error_label.setStyleSheet("color: red; font-size: 14px;")
            self.scanned_items_list.addWidget(error_label)
            return

        for item_name, item_data in self.scanned_items.items():
            for _ in range(item_data["quantity"]):
                self.pos_handler.update_inventory(item_name)

        self.clear_inputs()

        self.sell_button.setText("Success!")
        self.sell_button.setIcon(qta.icon("fa5s.check-circle"))
        self.sell_button.setProperty("success", True)
        self.style().polish(self.sell_button)

        QTimer.singleShot(2000, self.reset_sell_button)
        self.focus_barcode_input()

    def reset_sell_button(self):
        self.sell_button.setText(" Sell")
        self.sell_button.setIcon(qta.icon("fa5s.money-bill-wave"))
        self.sell_button.setProperty("success", False)
        self.style().polish(self.sell_button)

    def clear_inputs(self):
        self.scanner_input.clear()
        while self.scanned_items_list.count():
            widget = self.scanned_items_list.takeAt(0).widget()
            if widget:
                widget.deleteLater()
        self.scanned_items.clear()
        self.total_price_label.setText("Total: 0.00 KRW")
