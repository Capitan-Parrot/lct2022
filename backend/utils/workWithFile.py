import aiofiles
import pandas as pd


async def get_flats_from_excel_file(file):
    new_file = await file.read()
    flats = pd.read_excel(new_file)
    return flats.values.tolist()


async def save_file(file, out_file_path):
    async with aiofiles.open(out_file_path, 'wb') as out_file:
        while content := await file.read(1024):  # async read chunk
            await out_file.write(content)


async def update_file(flats, filename):
    pass


async def get_file(filename):
    pass