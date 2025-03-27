import pandas as pd
import os
from datetime import datetime


class InventoryHandler:
    def __init__(self):
        self.file_path = self.get_excel_path()

    def get_excel_path(self):
        current_year = datetime.now().year
        current_month = datetime.now().month
        file_name = f"POS_{current_year}_{current_month:02d}.xlsx"
        return os.path.join("data", file_name)

    def add_inventory_item(
        self, item_name, original_price, sale_price, inventory_quantity
    ):
        df = pd.read_excel(self.file_path, engine="openpyxl")

        new_data = {
            "No": len(df) + 1,
            "Barcode": "",
            "Item Name": item_name,
            "Inventory Quantity": int(inventory_quantity),
            "Quantity Sold": 0,
            "Quantity Left": int(inventory_quantity),
            "Original Price": float(original_price),
            "Sale Price": float(sale_price),
            "Total Profit": 0,
            "Invested": float(original_price) * int(inventory_quantity),
            "Clean Profit": 0,
        }

        df = df.append(new_data, ignore_index=True)
        df.to_excel(self.file_path, index=False, engine="openpyxl")
