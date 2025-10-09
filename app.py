from flask import Flask, render_template, request, jsonify
import random
import string

app = Flask(__name__)

def generate_password(length=12, use_uppercase=True, use_numbers=True, use_special=True):

    # Базовый набор символов (строчные буквы)
    characters = string.ascii_lowercase

    # Добавляем дополнительные наборы символов
    if use_uppercase:
        characters += string.ascii_uppercase
    if use_numbers:
        characters += string.digits
    if use_special:
        characters += "!@#$%^&*()_+-=[]{}|;:,.<>?"

    # Проверяем, что есть хотя бы один набор символов
    if not characters:
        characters = string.ascii_letters + string.digits

    # Генерируем пароль
    password = ''.join(random.choice(characters) for _ in range(length))

    return password

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    try:
        # Получаем параметры из формы
        length = int(request.form.get('length', 12))
        use_uppercase = 'uppercase' in request.form
        use_numbers = 'numbers' in request.form
        use_special = 'special' in request.form

        # Валидация длины
        if length < 4:
            length = 4
        elif length > 50:
            length = 50

        # Генерируем пароль
        password = generate_password(length, use_uppercase, use_numbers, use_special)

        return jsonify({
            'success': True,
            'password': password,
            'length': len(password)
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

if __name__ == '__main__':
    app.run(debug=True)