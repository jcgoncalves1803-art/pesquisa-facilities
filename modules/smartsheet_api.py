import smartsheet
import pandas as pd
from config import SMARTSHEET_TOKEN, SMARTSHEET_SHEET_ID


class SmartsheetManager:
    def __init__(self):
        self.client = smartsheet.Smartsheet(SMARTSHEET_TOKEN)
        self.client.errors_as_exceptions(True)
        self.sheet_id = int(SMARTSHEET_SHEET_ID)

    def get_column_map(self):
        sheet = self.client.Sheets.get_sheet(self.sheet_id)
        return {col.title: col.id for col in sheet.columns}

    def enviar_avaliacao(self, dados):
        try:
            col_map = self.get_column_map()
            new_row = smartsheet.models.Row()
            new_row.to_top = True

            for campo, valor in dados.items():
                if campo in col_map:
                    new_cell = smartsheet.models.Cell()
                    new_cell.column_id = col_map[campo]
                    new_cell.value = valor
                    new_row.cells.append(new_cell)

            response = self.client.Sheets.add_rows(self.sheet_id, [new_row])
            return response.result_code == 0
        except Exception as e:
            print(f"Erro ao enviar: {e}")
            return False

    def buscar_avaliacoes(self):
        try:
            sheet = self.client.Sheets.get_sheet(self.sheet_id)
            col_map = {col.id: col.title for col in sheet.columns}

            registros = []
            for row in sheet.rows:
                registro = {}
                for cell in row.cells:
                    col_name = col_map.get(cell.column_id, "")
                    registro[col_name] = cell.value
                registros.append(registro)

            return pd.DataFrame(registros)
        except Exception as e:
            print(f"Erro ao buscar: {e}")
            return pd.DataFrame()
