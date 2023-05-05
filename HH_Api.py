import requests
import json


class HHApi:
    hh_api = 'https://api.hh.ru/vacancies'
    def __init__(self):
        self.text =''
    @staticmethod
    def get_vacancies(text):
        req = requests.get('https://api.hh.ru/vacancies', {'text': text})
        data = req.content.decode()  # Декодируем его ответ, чтобы Кириллица отображалась корректно
        req.close()
        return data
