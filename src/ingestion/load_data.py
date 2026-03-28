import pandas as pd

def load_excel(path):
    try:
        xls = pd.ExcelFile(path)

        print("📄 Hojas encontradas:", xls.sheet_names)

        data = {}

        sheets_to_use = ["RAW_INPUT_METRICS", "RAW_ORDERS"]

        for sheet in sheets_to_use:
            if sheet in xls.sheet_names:
                df = pd.read_excel(xls, sheet_name=sheet)

                data[sheet] = df

                print(f"✅ Cargada hoja {sheet}: {df.shape}")
            else:
                print(f"⚠️ Hoja no encontrada: {sheet}")

        if not data:
            raise ValueError("❌ No se cargó ninguna hoja válida")

        return data

    except Exception as e:
        print("❌ Error cargando Excel:", e)
        raise