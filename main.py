import io
import os
import zipfile
import datetime
import re
from typing import List
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse, Response
# from PyPDF2 import PdfReader, PdfWriter
from pypdf import PdfReader, PdfWriter
from PIL import Image
import pytesseract
from pdf2image import convert_from_bytes

app = FastAPI()

@app.post('/list_reference/')
async def get_reference(image: UploadFile = File(...)):
    """
    Разделяет многостраничный pdf файл на отдельные файлы и упаковывает их в zip
    """
    if image.content_type != 'application/pdf':
        raise HTTPException(status_code=400, detail='Invalid file type. Only PDF files are allowed.')

    reader = PdfReader(image.file)
    zip_name = f'{os.path.splitext(image.filename)[0]}.zip'
    zip_buffer = io.BytesIO()
    start = datetime.datetime.now()
    for i in range(len(reader.pages)):
        buff = io.BytesIO()

        page = reader.pages[i]
        writer = PdfWriter()
        writer.add_page(page)
        writer.write(buff)

        buff.seek(0)
        image = convert_from_bytes(buff.getvalue())[0]
        text = pytesseract.image_to_string(image, lang='rus')
        pattern = "Настоящим подтверждаем, что\n+(?P<fio>.+)"
        match = re.search(pattern, text)
        file_name = match.group('fio').strip().split(' ')
        file_name = '_'.join([name for name in file_name if not re.search('[\(,.\)]', name)])
        # сохраняем файлы на диск
        with open(f'/home/egor/PDF/result/{file_name}.pdf', 'wb') as f:
            f.write(buff.getvalue())

        with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
            zip_file.writestr(f'{file_name}.pdf', buff.getvalue())

    print('Итого:', datetime.datetime.now() - start)
    response = Response(content=zip_buffer.getvalue(), media_type='application/zip')
    response.headers['Content-Disposition'] = f'attachment; filename=result_file_{datetime.date.today()}.zip'
    return response
