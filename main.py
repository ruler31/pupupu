import os

from flask import Flask, render_template, request, jsonify, redirect, send_file, session, url_for
import re
app = Flask(__name__)
import xlwt
import hashlib
app.secret_key = 'nhneg82indcwfea244532tgdgw32214sagfew'


tables = []




@app.route('/')
def index():
    if 'username' in session:
        logged_in = True
        username = session['username']
    else:
        logged_in = False
        username = None
    return render_template('index.html', logged_in=logged_in, username=username)
@app.route('/trans')
def trans():
    return render_template('trans.html')

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
    table_name = request.form['table_name']
    rows = int(request.form['rows'])
    cols = int(request.form['cols'])

    table = [[f'Row {i+1}, Col {j+1}' for j in range(cols)] for i in range(rows)]

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

@app.route('/word')
def word():
    return render_template('word.html')

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








@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        with open("users.txt", "r") as f:
            userse = f.readlines()
            users = []
            for user in userse:
                users.append(user.split(":")[0])
        if username in users:
            return "Пользователь уже существует!"
        with open('users.txt', 'a') as file:
            file.write(f'{username}:{password}\n')
        return "Регистрация завершена успешно!"


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if check_credentials(username, password):
            session['username'] = username
            return redirect('/')
        else:
            return render_template('login.html', error='Неправильное имя пользователя или пароль')




def check_credentials(username, password):
    with open('users.txt', 'r') as file:
        for line in file:
            stored_username, *stored_password = line.strip().split(':')
            stored_password = ':'.join(stored_password)  # Объединяем оставшуюся часть строки как пароль
            if stored_username == username and stored_password == password:
                return True
    return False




def process_registration(form_data):

    return "Регистрация завершена успешно!"

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))


@app.route('/save', methods=['POST'])
def save_text():
    if 'username' not in session:
        return redirect(url_for('login'))

    text = request.form['text']

    username = session['username']


    user_folder = os.path.join("user_data", username)
    os.makedirs(user_folder, exist_ok=True)


    file_path = os.path.join(user_folder, "saved_text.txt")


    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(text)

    return redirect(url_for('index'))



@app.route('/load')
def load_text():
    if 'username' not in session:
        return redirect(url_for('login'))

    # Получаем имя пользователя из сессии
    username = session['username']

    # Путь к файлу пользователя
    file_path = os.path.join("user_data", username, "saved_text.txt")

    # Загружаем текст из файла, если файл существует
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
    else:
        text = ""  # Если файл не существует, возвращаем пустую строку

    return render_template('index.html', loaded_text=text)

if __name__ == '__main__':
    app.run(debug=True)
