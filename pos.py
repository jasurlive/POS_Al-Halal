import pandas as pd
import os
from datetime import datetime
import openpyxl
from openpyxl.utils.dataframe import dataframe_to_rows


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

        # Read data into pandas dataframe
        df = pd.read_excel(self.file_path, engine="openpyxl")

        # Find the index of the item to update
        index = df[df["Item Name"] == item_name].index
        if not index.empty:
            df.at[index[0], "Inventory Quantity"] = max(
                0, df.at[index[0], "Inventory Quantity"] - 1
            )

            # Preserve the original column widths
            original_column_widths = {}
            for col in sheet.columns:
                column = col[0].column_letter  # Get the column name
                max_length = 0
                for cell in col:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(cell.value)
                    except:
                        pass
                adjusted_width = max_length + 2
                original_column_widths[column] = adjusted_width

            # Clear all existing rows except for the header
            for row in sheet.iter_rows(min_row=2, max_row=sheet.max_row):
                for cell in row:
                    cell.value = None  # Clear the cell value

            # Write the updated dataframe back to the sheet
            for r_idx, row in enumerate(
                dataframe_to_rows(df, index=False, header=True), 2
            ):
                for c_idx, value in enumerate(row, 1):
                    sheet.cell(row=r_idx, column=c_idx, value=value)

            # Restore column widths
            for col_letter, width in original_column_widths.items():
                sheet.column_dimensions[col_letter].width = width

            wb.save(self.file_path)
