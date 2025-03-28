import pandas as pd
from openpyxl import load_workbook
from excel import ExcelHandler


class POSHandler:
    def __init__(self):
        self.excel_handler = ExcelHandler()

    def find_item_by_barcode(self, barcode):
        # Using pandas to search for the barcode in the Excel sheet
        df = pd.read_excel(
            self.excel_handler.file_path, dtype={"Barcode": str}, engine="openpyxl"
        )
        # Look for the item in the dataframe
        item = df[df["Barcode"] == barcode]
        if not item.empty:
            return item.iloc[0].to_dict()  # Return the first match
        else:
            return None

    def update_inventory(self, item_name):
        """Update the inventory by reducing the quantity of the sold item."""
        wb = self.excel_handler.load_workbook()
        ws = wb.active

        columns = self.excel_handler.get_column_indexes(ws)

        # Search for the item in the "Item Name" column
        for row in range(2, ws.max_row + 1):  # Start from row 2 (skip headers)
            if ws.cell(row=row, column=columns["Item Name"]).value == item_name:
                inventory_cell = ws.cell(row=row, column=columns["Inventory Quantity"])
                try:
                    current_quantity = int(inventory_cell.value)
                except (ValueError, TypeError):
                    current_quantity = 0
                inventory_cell.value = max(0, current_quantity - 1)
                break

        self.excel_handler.save_workbook(wb)
