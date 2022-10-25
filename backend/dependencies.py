import pandas as pd


async def get_flats_from_excel_file(file):
    new_file = await file.read()
    flats = pd.read_excel(new_file)
    return flats.values.tolist()

