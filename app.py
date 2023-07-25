import io
import re

import numpy as np
import pytesseract
from PIL import Image
from pdf2image import convert_from_bytes, convert_from_path
from pypdf import PdfReader
from pypdf import PdfWriter

from flask import Flask, redirect, make_response, send_file, request, abort

app = Flask(__name__)


@app.route('/list_reference', methods=('GET', 'POST'))
def get_reference():
    param = 'save'
    file = request.files.get('image')
    if file.mimetype != 'application/pdf':
        return abort(404, 'формат файла не pdf')

    reader = PdfReader(file)

    for i in range(len(reader.pages)):
        page = reader.pages[i]
        buff = io.BytesIO()
        writer = PdfWriter()
        writer.add_page(page)
        writer.write(buff)
        buff.seek(0)
        image = convert_from_bytes(buff.getvalue())[0]
        text = pytesseract.image_to_string(image, lang='rus')
        # match = re.search('(?P<name>[А-ЯЁ][а-яё]+)\s(?P<lastname>[А-ЯЁ][а-яё]+)\s(?P<fatherland>[А-ЯЁ][а-яё]+)\s\((?P<birthdate>\d{2}.\d{2}.\d{4}).+\)',text)
        pattern = "Настоящим подтверждаем, что\n+(?P<fio>.+)"
        match = re.search(pattern, text)
        file_name = match.group('fio').strip().split(' ')
        file_name = '_'.join([name for name in file_name if not re.search('[\(,.\)]', name)])
        if param == 'save':
            # сохраняем файлы на диск
            with open(f'/home/egor/PDF/result/{file_name}.pdf', 'wb') as f:
                f.write(buff.getvalue())
        # print(buff.getvalue())
            # (f'home/egor/PDF/result/{file_name}.pdf')
        # buff.save(f'~/PDF/result/{file_name}.pdf')
    return "send_file(buff, as_attachment=True, download_name=f'{file_name}.pdf')"
    # return response


if __name__ == '__main__':
    app.run(debug=True)
