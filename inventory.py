from openpyxl import load_workbook
from excel import ExcelHandler


class InventoryHandler:
    def __init__(self):
        self.excel_handler = ExcelHandler()

    def add_inventory_item(
        self, barcode, item_name, original_price, sale_price, inventory_quantity
    ):
        wb = self.excel_handler.load_workbook()
        ws = wb.active

        columns = self.excel_handler.get_column_indexes(ws)

        # Validate and sanitize inputs
        barcode = str(barcode).strip()
        item_name = str(item_name).strip()
        try:
            original_price = float(original_price)
        except ValueError:
            raise ValueError("Original Price must be a valid number.")
        try:
            sale_price = float(sale_price)
        except ValueError:
            raise ValueError("Sale Price must be a valid number.")
        try:
            inventory_quantity = int(inventory_quantity)
        except ValueError:
            raise ValueError("Inventory Quantity must be a valid integer.")

        # Check if the barcode already exists
        existing_row = None
        for row in range(2, ws.max_row + 1):  # Start from row 2 (skip headers)
            if str(ws.cell(row=row, column=columns["Barcode"]).value) == barcode:
                existing_row = row
                break

        target_row = (
            existing_row
            if existing_row
            else self.excel_handler.find_first_empty_row(ws, columns["Barcode"])
        )

        data = {
            "Barcode": barcode,
            "Item Name": item_name,
            "Inventory Quantity": inventory_quantity,
            "Original Price": original_price,
            "Sale Price": sale_price,
        }

        for column_name, value in data.items():
            cell = ws.cell(row=target_row, column=columns[column_name], value=value)
            self.excel_handler.apply_formatting(cell, column_name)

        self.excel_handler.save_workbook(wb)

    def get_inventory_item(self, barcode):
        wb = self.excel_handler.load_workbook()
        ws = wb.active

        columns = self.excel_handler.get_column_indexes(ws)

        for row in range(2, ws.max_row + 1):
            if str(ws.cell(row=row, column=columns["Barcode"]).value) == str(barcode):
                return {
                    column_name: ws.cell(row=row, column=col_index).value
                    for column_name, col_index in columns.items()
                }

        return None
