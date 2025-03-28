import qtawesome as qta
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel
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

        # Success message label
        self.success_message_label = QLabel("", self)
        self.success_message_label.setStyleSheet("color: green; font-size: 14px;")
        self.layout.addWidget(self.success_message_label)

    def add_inventory_item(self):
        try:
            # Call the inventory handler to add the item
            self.inventory_handler.add_inventory_item(
                str(self.barcode_input.text()),  # Ensure barcode is passed as a string
                self.item_name_input.text(),
                self.original_price_input.text(),
                self.sale_price_input.text(),
                self.inventory_quantity_input.text(),
            )

            # Clear input fields
            self.barcode_input.clear()
            self.item_name_input.clear()
            self.original_price_input.clear()
            self.sale_price_input.clear()
            self.inventory_quantity_input.clear()

            # Update button text and show success message
            self.add_inventory_button.setText("Add Item")
            self.success_message_label.setText("Item added successfully!")

        except Exception as e:
            # Handle errors (optional)
            self.success_message_label.setText(f"Error: {str(e)}")
            self.success_message_label.setStyleSheet("color: red; font-size: 14px;")

    def focus_barcode_input(self):
        """Set focus on the barcode input field."""
        self.barcode_input.setFocus()
