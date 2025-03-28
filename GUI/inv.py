import qtawesome as qta
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel
from inventory import InventoryHandler


class InventoryWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout(self)
        self.inventory_handler = InventoryHandler()

        input_style = """
            padding: 15px;
            border: 2px solid #17a2b8;
            border-radius: 5px;
            font-size: 18px;
            background-color: #ffffff;
            color: #333;
        """

        self.barcode_input = QLineEdit(self)
        self.barcode_input.setPlaceholderText("Barcode")
        self.barcode_input.setStyleSheet(input_style)
        self.barcode_input.returnPressed.connect(
            self.prefill_inventory_item
        )  # Trigger prefill on Enter key
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
            "background-color: #008666; color: white; padding: 20px; font-size: 18px; border-radius: 5px; border: none;"
        )
        self.add_inventory_button.clicked.connect(self.add_inventory_item)
        self.layout.addWidget(self.add_inventory_button)

        # Success message label
        self.success_message_label = QLabel("", self)
        self.success_message_label.setStyleSheet("color: green; font-size: 14px;")
        self.layout.addWidget(self.success_message_label)

    def add_inventory_item(self):
        try:
            # Call the inventory handler to add or update the item
            self.inventory_handler.add_inventory_item(
                str(self.barcode_input.text()),  # Ensure barcode is passed as a string
                self.item_name_input.text(),
                self.original_price_input.text(),
                self.sale_price_input.text(),
                self.inventory_quantity_input.text(),
            )

            # Clear input fields
            self.clear_inputs()

            # Update button text and show success message
            self.add_inventory_button.setText("Add Item")
            self.success_message_label.setText("Item added/updated successfully!")
            self.success_message_label.setStyleSheet("color: green; font-size: 14px;")

        except Exception as e:
            # Handle errors (optional)
            self.success_message_label.setText(f"Error: {str(e)}")
            self.success_message_label.setStyleSheet("color: red; font-size: 14px;")

    def prefill_inventory_item(self):
        """Prefill input fields if the barcode exists in the inventory."""
        barcode = self.barcode_input.text()
        if barcode:
            item = self.inventory_handler.get_inventory_item(barcode)
            if item:
                self.item_name_input.setText(item.get("Item Name", ""))
                self.original_price_input.setText(str(item.get("Original Price", "")))
                self.sale_price_input.setText(str(item.get("Sale Price", "")))
                self.inventory_quantity_input.setText(
                    str(item.get("Inventory Quantity", ""))
                )
                self.success_message_label.setText(
                    "Item found. Fields prefilled for editing."
                )
                self.success_message_label.setStyleSheet(
                    "color: green; font-size: 14px;"
                )
            else:
                self.success_message_label.setText("Item not found in inventory.")
                self.success_message_label.setStyleSheet("color: red; font-size: 14px;")

    def focus_barcode_input(self):
        """Set focus on the barcode input field."""
        self.barcode_input.setFocus()

    def clear_inputs(self):
        """Clear all input fields."""
        self.barcode_input.clear()
        self.item_name_input.clear()
        self.original_price_input.clear()
        self.sale_price_input.clear()
        self.inventory_quantity_input.clear()
        self.success_message_label.clear()
