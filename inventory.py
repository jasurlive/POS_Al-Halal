import os
from datetime import datetime
from openpyxl import load_workbook


class InventoryHandler:
    def __init__(self):
        self.file_path = self.get_excel_path()

    def get_excel_path(self):
        current_year = datetime.now().year
        current_month = datetime.now().month
        file_name = f"POS_{current_year}_{current_month:02d}.xlsx"
        return os.path.join("data", file_name)

    def get_column_indexes(self, ws):
        """Find column indexes based on header names."""
        headers = {
            ws.cell(row=1, column=col).value: col for col in range(1, ws.max_column + 1)
        }
        required_columns = [
            "Barcode",
            "Item Name",
            "Inventory Quantity",
            "Original Price",
            "Sale Price",
        ]

        missing_columns = [col for col in required_columns if col not in headers]
        if missing_columns:
            raise ValueError(f"Missing required columns in Excel: {missing_columns}")

        return {col: headers[col] for col in required_columns}

    def find_first_empty_row(self, ws, barcode_col):
        """Find the first available empty row in the Barcode column."""
        for row in range(2, ws.max_row + 1):  # Start from row 2 (skip headers)
            if ws.cell(row=row, column=barcode_col).value is None:
                return row
        return ws.max_row + 1  # If no empty row found, append at the end

    def add_inventory_item(
        self, barcode, item_name, original_price, sale_price, inventory_quantity
    ):
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"Excel file not found: {self.file_path}")

        wb = load_workbook(self.file_path)
        ws = wb.active

        # Get column indexes dynamically
        columns = self.get_column_indexes(ws)

        # Find the first empty row in "Barcode" column
        empty_row = self.find_first_empty_row(ws, columns["Barcode"])

        # Insert data into the correct columns dynamically
        ws.cell(row=empty_row, column=columns["Barcode"], value=barcode)
        ws.cell(row=empty_row, column=columns["Item Name"], value=item_name)
        ws.cell(
            row=empty_row,
            column=columns["Inventory Quantity"],
            value=inventory_quantity,
        )
        ws.cell(row=empty_row, column=columns["Original Price"], value=original_price)
        ws.cell(row=empty_row, column=columns["Sale Price"], value=sale_price)

        # Save workbook
        wb.save(self.file_path)
