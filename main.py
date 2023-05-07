from abc import ABC, abstractmethod
import json
import csv
import requests


class ReqFromApi(ABC):
    @abstractmethod
    def __init__(self, file_name, name_vacancies):
        self.file_name = file_name
        self.name_vacancies = name_vacancies

    @abstractmethod
    def get_vacancies(self):
        pass

    @abstractmethod
    def make_file(self):
        pass

    def make_copy(self):
        pass


class HHApi(ReqFromApi):
    def __init__(self, file_name, name_vacancies):
        super().__init__(file_name, name_vacancies)

    def make_copy(self):
        pass

    def make_file(self):
        result = self.get_vacancies()
        with open(f'{self.file_name}', 'w', encoding='utf-8') as file:
            file_writer = csv.writer(file, delimiter=",", lineterminator="\r")
            for point in result:
                file_writer.writerow([point.get('name'), point.get('area').get('name'), point.get('salary'),

                                      point.get('apply_alternate_url')])

    def get_vacancies(self):
        req = requests.get('https://api.hh.ru/vacancies', {'text': self.name_vacancies})
        data = req.content.decode()  # спер из одного мануала
        req.close()

        json.dumps(data)
        data = json.loads(data)

        items_list = []

        for item in data['items']:
            items_list.append(item)
        return items_list


class SJApi(ReqFromApi):
    pass


usr_inp = ''
while True:
    print('Какую профессию ищем:\nquit - выйти')
    usr_inp = input()
    if usr_inp == 'quit'.lower():
        break
    copy = HHApi(f"{input('Имя файла лога')}.csv", usr_inp)
    copy.get_vacancies()
    copy.make_file()
    usr_inp = input('На экран выведем? Y/N').lower()
    if usr_inp == 'N':
        print('До свидания!')
        break
    elif usr_inp == 'Y':
        print(copy.get_vacancies())
