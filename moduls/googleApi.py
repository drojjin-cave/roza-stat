import requests
import json


class GoogleSheetsAPI:
    def __init__(self, script_url):
        self.script_url = script_url

    def get_data(self, params=None):
        """
        Получает данные из Google Таблицы через Apps Script
        """
        try:
            response = requests.get(self.script_url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            # Нормализуем структуру данных для единообразного отображения
            return self.normalize_data_structure(data)

        except requests.exceptions.RequestException as e:
            return {
                'status': 'error',
                'message': f'Ошибка при получении данных: {str(e)}'
            }
        except json.JSONDecodeError as e:
            return {
                'status': 'error',
                'message': f'Ошибка при разборе JSON: {str(e)}'
            }

    def normalize_data_structure(self, data):
        """
        Нормализует структуру данных для единообразного отображения в шаблонах
        """
        if data.get('status') == 'success' and 'data' in data:
            # Если данные уже в правильном формате
            if 'metadata' in data['data'] and 'records' in data['data']:
                return data

            # Если структура отличается, преобразуем к стандартной
            if 'records' in data['data']:
                records = data['data']['records']
                if records and len(records) > 0:
                    # Создаем метаданные на основе первого элемента
                    first_record = records[0]
                    columns = [{'name': key, 'index': i} for i, key in enumerate(first_record.keys())]

                    data['data']['metadata'] = {
                        'sheetName': data['data'].get('sheetName', 'Unknown'),
                        'totalRecords': len(records),
                        'returnedRecords': len(records),
                        'columns': columns
                    }

        return data