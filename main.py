from flask import Flask, render_template, request, jsonify, redirect, send_file
import re
app = Flask(__name__)
import xlwt


tables = []




@app.route('/')
def index():
    return render_template('index.html')


@app.route('/translate', methods=['POST'])
def translate():
    if request.method == 'POST':
        russian_text = request.form['russian_text']
        function_choice = request.form['function_choice']

        if function_choice == 'to_english':
            translated_text = translate_to_english(russian_text)
        elif function_choice == 'to_russian':
            translated_text = translate_to_russian(russian_text)
        elif function_choice == 'format_sentence':
            translated_text = format_sentence(russian_text)
        else:
            translated_text = "Выберите функцию"

        return render_template('translate.html', original_text=russian_text, translated_text=translated_text)


def translate_to_english(russian_text):
    translation_table = {
        'й': 'q', 'ц': 'w', 'у': 'e', 'к': 'r', 'е': 't', 'н': 'y', 'г': 'u', 'ш': 'i', 'щ': 'o', 'з': 'p',
        'ф': 'a', 'ы': 's', 'в': 'd', 'а': 'f', 'п': 'g', 'р': 'h', 'о': 'j', 'л': 'k', 'д': 'l', 'ж': ';',
        'э': "'", 'я': 'z', 'ч': 'x', 'с': 'c', 'м': 'v', 'и': 'b', 'т': 'n', 'ь': 'm', 'б': ',', 'ю': '.',
        'ё': '`', 'Й': 'Q', 'Ц': 'W', 'У': 'E', 'К': 'R', 'Е': 'T', 'Н': 'Y', 'Г': 'U', 'Ш': 'I', 'Щ': 'O',
        'З': 'P', 'Ф': 'A', 'Ы': 'S', 'В': 'D', 'А': 'F', 'П': 'G', 'Р': 'H', 'О': 'J', 'Л': 'K', 'Д': 'L',
        'Ж': ':', 'Э': '"', 'Я': 'Z', 'Ч': 'X', 'С': 'C', 'М': 'V', 'И': 'B', 'Т': 'N', 'Ь': 'M', 'Б': '<',
        'Ю': '>', 'Ё': '~'
    }
    translated_text = ''.join([translation_table.get(c, c) for c in russian_text])
    return translated_text


def translate_to_russian(english_text):
    translation_table2 = {
        'q': 'й', 'w': 'ц', 'e': 'у', 'r': 'к', 't': 'е', 'y': 'н', 'u': 'г', 'i': 'ш', 'o': 'щ', 'p': 'з',
        'a': 'ф', 's': 'ы', 'd': 'в', 'f': 'а', 'g': 'п', 'h': 'р', 'j': 'о', 'k': 'л', 'l': 'д', ';': 'ж',
        "'": 'э', 'z': 'я', 'x': 'ч', 'c': 'с', 'v': 'м', 'b': 'и', 'n': 'т', 'm': 'ь', ',': 'б', '.': 'ю',
        '`': 'ё', 'Q': 'Й', 'W': 'Ц', 'E': 'У', 'R': 'К', 'T': 'Е', 'Y': 'Н', 'U': 'Г', 'I': 'Ш', 'O': 'Щ',
        'P': 'З', 'A': 'Ф', 'S': 'Ы', 'D': 'В', 'F': 'А', 'G': 'П', 'H': 'Р', 'J': 'О', 'K': 'Л', 'L': 'Д',
        ':': 'Ж', '"': 'Э', 'Z': 'Я', 'X': 'Ч', 'C': 'С', 'V': 'М', 'B': 'И', 'N': 'Т', 'M': 'Ь', '<': 'Б',
        '>': 'Ю', '~': 'Ё'
    }
    translated_text = ''.join([translation_table2.get(c, c) for c in english_text])
    return translated_text


def format_sentence(sentence):
    sentence = sentence.strip()
    sentence = sentence.capitalize()
    if not sentence.endswith(('.', '!', '?')):
        sentence += '.'
    sentence = re.sub(r'([\'"])', r'\1', sentence)
    sentence = re.sub(r'\s*,', ',', sentence)
    sentence = re.sub(r',', ', ', sentence)

    return sentence

@app.route('/table')
def table():
    return render_template('table.html', tables=tables)

@app.route('/add_table', methods=['POST'])
def add_table():
    # Получаем данные из формы
    table_name = request.form['table_name']
    rows = int(request.form['rows'])
    cols = int(request.form['cols'])

    # Создаем таблицу в виде списка списков
    table = [[f'Row {i+1}, Col {j+1}' for j in range(cols)] for i in range(rows)]

    # Добавляем таблицу в список
    tables.append({'name': table_name, 'data': table})

    return render_template('table.html', tables=tables)

@app.route('/update_cell', methods=['POST'])
def update_cell():
    data = request.json
    table_id = int(data['table_id'])
    row_index = int(data['row_index'])
    col_index = int(data['col_index'])
    new_value = data['new_value']

    tables[table_id]['data'][row_index][col_index] = new_value

    return jsonify({'message': 'Cell updated successfully'})
@app.route('/add_row', methods=['POST'])
def add_row():
    table_id = int(request.form['table_id'])
    tables[table_id]['data'].append(['' for _ in range(len(tables[table_id]['data'][0]))])
    return render_template('table.html', tables=tables)
@app.route('/add_column', methods=['POST'])
def add_column():
    table_id = int(request.form['table_id'])
    for row in tables[table_id]['data']:
        row.append('')
    return redirect('/table')


@app.route('/download_table/<int:table_id>', methods=['GET'])
def download_table(table_id):
    table = tables[table_id]

    workbook = xlwt.Workbook()
    sheet = workbook.add_sheet('Table Data')

    for row_index, row in enumerate(table['data']):
        for col_index, cell in enumerate(row):
            sheet.write(row_index, col_index, cell)

    file_path = f'table_{table_id}.xls'
    workbook.save(file_path)
    return send_file(file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
