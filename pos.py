import pandas as pd
import os
from datetime import datetime
import openpyxl


class POSHandler:
    def __init__(self):
        self.file_path = self.get_excel_path()

    def get_excel_path(self):
        current_year = datetime.now().year
        current_month = datetime.now().month
        file_name = f"POS_{current_year}_{current_month:02d}.xlsx"
        return os.path.join("data", file_name)

    def find_item_by_barcode(self, barcode):
        df = pd.read_excel(self.file_path, dtype={"Barcode": str}, engine="openpyxl")
        item = df[df["Barcode"] == barcode]
        return item.iloc[0].to_dict() if not item.empty else None

    def update_inventory(self, item_name):
        # Load the workbook with openpyxl to keep the formatting
        wb = openpyxl.load_workbook(self.file_path)
        sheet = wb.active

        # Extract the header row and map column names to indexes
        header = [cell.value for cell in sheet[1]]
        item_name_col = header.index(
            "Item Name"
        )  # Find the column index for "Item Name"
        inventory_col = header.index(
            "Inventory Quantity"
        )  # Find the column index for "Inventory Quantity"

        # Iterate over the rows to find the item by its name
        for row in sheet.iter_rows(min_row=2, max_row=sheet.max_row):
            if row[item_name_col].value == item_name:  # Match the item name
                inventory_cell = row[
                    inventory_col
                ]  # Reference the "Inventory Quantity" cell
                if inventory_cell.value is not None:
                    inventory_cell.value = max(
                        0, inventory_cell.value - 1
                    )  # Decrease inventory
                break

        # Save the workbook with the updated inventory
        wb.save(self.file_path)
