import qtawesome as qta
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLineEdit,
    QLabel,
    QApplication,
)
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
            lambda: self.handle_key_press(self.item_name_input, None, is_barcode=True)
        )
        self.layout.addWidget(self.barcode_input)

        self.item_name_input = QLineEdit(self)
        self.item_name_input.setPlaceholderText("Item Name")
        self.item_name_input.setStyleSheet(input_style)
        self.item_name_input.returnPressed.connect(
            lambda: self.handle_key_press(self.original_price_input, self.barcode_input)
        )
        self.layout.addWidget(self.item_name_input)

        self.original_price_input = QLineEdit(self)
        self.original_price_input.setPlaceholderText("Original Price")
        self.original_price_input.setStyleSheet(input_style)
        self.original_price_input.returnPressed.connect(
            lambda: self.handle_key_press(self.sale_price_input, self.item_name_input)
        )
        self.layout.addWidget(self.original_price_input)

        self.sale_price_input = QLineEdit(self)
        self.sale_price_input.setPlaceholderText("Sale Price")
        self.sale_price_input.setStyleSheet(input_style)
        self.sale_price_input.returnPressed.connect(
            lambda: self.handle_key_press(
                self.inventory_quantity_input, self.original_price_input
            )
        )
        self.layout.addWidget(self.sale_price_input)

        self.inventory_quantity_input = QLineEdit(self)
        self.inventory_quantity_input.setPlaceholderText("Inventory Quantity")
        self.inventory_quantity_input.setStyleSheet(input_style)
        self.inventory_quantity_input.returnPressed.connect(
            lambda: self.handle_key_press(None, self.sale_price_input, is_last=True)
        )
        self.layout.addWidget(self.inventory_quantity_input)

        # Add Inventory Button with dynamic text
        self.add_inventory_button = QPushButton("Add New Item", self)
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

    def handle_key_press(
        self, next_input, previous_input, is_last=False, is_barcode=False
    ):
        """Handle the key press for Enter and Shift+Enter."""
        if self.has_shift_key_pressed():
            if previous_input:  # If Shift + Enter, go to previous input
                previous_input.setFocus()
                previous_input.selectAll()
        else:
            if is_barcode:
                self.prefill_inventory_item()  # Search and prefill item
            if is_last:
                self.add_inventory_item()  # Trigger add item if it's the last field
            elif next_input:  # Otherwise, move to the next input field
                next_input.setFocus()

    def has_shift_key_pressed(self):
        """Check if Shift key is pressed along with Enter."""
        return QApplication.keyboardModifiers() == Qt.KeyboardModifier.ShiftModifier

    def add_inventory_item(self):
        try:
            # Call the inventory handler to add or update the item
            self.inventory_handler.add_inventory_item(
                str(self.barcode_input.text()),
                self.item_name_input.text(),
                self.original_price_input.text(),
                self.sale_price_input.text(),
                self.inventory_quantity_input.text(),
            )

            # Show success message
            self.success_message_label.setText("Item added/updated successfully!")
            self.success_message_label.setStyleSheet("color: green; font-size: 14px;")

            # Change button text to "Added"
            self.add_inventory_button.setText("Added")

            # Set a timer to revert button text after 2 seconds
            QTimer.singleShot(2000, self.reset_add_button)

            # Clear input fields and focus barcode input for next scan
            self.clear_inputs()
            self.focus_barcode_input()

        except Exception as e:
            self.success_message_label.setText(f"Error: {str(e)}")
            self.success_message_label.setStyleSheet("color: red; font-size: 14px;")

    def reset_add_button(self):
        """Revert button text to 'Add New Item'."""
        self.add_inventory_button.setText("Add New Item")

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
