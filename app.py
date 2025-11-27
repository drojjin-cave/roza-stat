from flask import Flask, render_template, request, jsonify
from datetime import datetime
from moduls.googleApi import GoogleSheetsAPI
from moduls.script_url import SCRIPT_URL
app = Flask(__name__)

# Инициализация API
sheets_api = GoogleSheetsAPI(SCRIPT_URL)


@app.route('/')
def index():
    """
    Главная страница с таблицей
    """
    # Параметры из GET запроса
    sheet_name = request.args.get('sheet', '')
    limit = request.args.get('limit', '')
    offset = request.args.get('offset', '')

    # Формируем параметры для API
    params = {}
    if sheet_name:
        params['sheet'] = sheet_name
    if limit:
        params['limit'] = limit
    if offset:
        params['offset'] = offset

    # Получаем данные
    data = sheets_api.get_data(params)

    return render_template('index.html',
                           data=data,
                           params=params,
                           current_time=datetime.now())


@app.route('/api/data')
def api_data():
    """
    API endpoint для получения данных в JSON формате
    """
    params = request.args.to_dict()
    data = sheets_api.get_data(params)
    return jsonify(data)


@app.route('/sheets')
def sheets_list():
    """
    Страница для управления разными листами
    """
    available_sheets = ['Sheet1', 'Data', 'Users', 'Products']  # Замените на реальные имена листов

    sheet_name = request.args.get('sheet', 'Sheet1')
    params = {'sheet': sheet_name}

    data = sheets_api.get_data(params)

    return render_template('sheets.html',
                           data=data,
                           available_sheets=available_sheets,
                           selected_sheet=sheet_name,
                           current_time=datetime.now())


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)