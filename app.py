import io
import os
import re
import zipfile
import datetime
import pytesseract

from pdf2image import convert_from_bytes, convert_from_path
from pypdf import PdfReader, PdfWriter
from flask import Flask, make_response, send_file, request, abort, Response

app = Flask(__name__)


@app.route('/list_reference', methods=('GET', 'POST'))
def get_reference() -> Response:
    """
    Разделяет многостраничный pdf файл на отдельные файлы ,упаковывает их в zip и отправляет по HTTP
    :return: zip
    """
    save_files = False
    write_zip = False

    file = request.files.get('image')
    if file.mimetype != 'application/pdf':
        return abort(404, 'формат файла не pdf')

    reader = PdfReader(file)
    zip_name = f'{os.path.splitext(file.filename)[0]}.zip'
    zip_buffer = io.BytesIO()
    start = datetime.datetime.now()
    how_match = 7
    how_match = how_match if how_match is not None else len(reader.pages)
    for i in range(how_match):
        buff = io.BytesIO()

        page = reader.pages[i]
        writer = PdfWriter()
        writer.add_page(page)
        writer.write(buff)

        buff.seek(0)
        pdf_to_image = convert_from_bytes(buff.getvalue())[0]
        text_from_image = pytesseract.image_to_string(pdf_to_image, lang='rus')
        # match = re.search('(?P<name>[А-ЯЁ][а-яё]+)\s(?P<lastname>[А-ЯЁ][а-яё]+)\s(?P<fatherland>[А-ЯЁ][а-яё]+)\s\((?P<birthdate>\d{2}.\d{2}.\d{4}).+\)',text)
        pattern = "Настоящим подтверждаем, что\n+(?P<fio>.+)"
        match = re.search(pattern, text_from_image)
        if match:
            file_name = match.group('fio').strip().split(' ')
            file_name = '_'.join([name for name in file_name if not re.search('[\(,.\)]', name)])
        else:
            file_name = 'Неопознан'
        if save_files:
            # сохраняем файлы на диск
            with open(f'/home/egor/PDF/result/{file_name}.pdf', 'wb') as f:
                f.write(buff.getvalue())
        # zip_buffer = io.BytesIO()

        with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
            zip_file.writestr(f'{file_name}.pdf', buff.getvalue())
        if write_zip:
            with open(f'/home/egor/PDF/result/{zip_name}', 'wb') as f:
                f.write(zip_buffer.getvalue())

    # return send_file(buff, mimetype='application/zip', as_attachment=True, download_name="1.pdf")
    # return send_file(zip_buffer, mimetype='application/zip', as_attachment=True, download_name="1.zip")
    print('Итого:', datetime.datetime.now() - start)
    response = make_response(zip_buffer.getvalue())
    response.headers['Content-Type'] = 'application/zip'
    response.headers['Content-Disposition'] = f'attachment; filename=result_file_{datetime.date.today()}.zip'
    return response


if __name__ == '__main__':
    app.run(debug=True, port=5050)
