import qtawesome as qta
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLineEdit
from inventory import InventoryHandler


class InventoryWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout(self)
        self.inventory_handler = InventoryHandler()

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
        self.layout.addWidget(self.barcode_input)

        self.item_name_input = QLineEdit(self)
        self.item_name_input.setPlaceholderText("Item Name")
        self.item_name_input.setStyleSheet(input_style)
        self.layout.addWidget(self.item_name_input)

        self.original_price_input = QLineEdit(self)
        self.original_price_input.setPlaceholderText("Original Price")
        self.original_price_input.setStyleSheet(input_style)
        self.layout.addWidget(self.original_price_input)

        self.sale_price_input = QLineEdit(self)
        self.sale_price_input.setPlaceholderText("Sale Price")
        self.sale_price_input.setStyleSheet(input_style)
        self.layout.addWidget(self.sale_price_input)

        self.inventory_quantity_input = QLineEdit(self)
        self.inventory_quantity_input.setPlaceholderText("Inventory Quantity")
        self.inventory_quantity_input.setStyleSheet(input_style)
        self.layout.addWidget(self.inventory_quantity_input)

        # Add Inventory Button
        self.add_inventory_button = QPushButton(" Add New Item", self)
        self.add_inventory_button.setIcon(qta.icon("fa5s.plus-circle"))
        self.add_inventory_button.setStyleSheet(
            "background-color: #ffc107; color: white; padding: 12px; font-size: 16px; border-radius: 5px; border: none;"
        )
        self.add_inventory_button.clicked.connect(self.add_inventory_item)
        self.layout.addWidget(self.add_inventory_button)

    def add_inventory_item(self):
        self.inventory_handler.add_inventory_item(
            self.item_name_input.text(),
            self.barcode_input.text(),
            self.original_price_input.text(),
            self.sale_price_input.text(),
            self.inventory_quantity_input.text(),
        )
