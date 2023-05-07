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
        with open('result_log.csv','a',encoding='utf-8') as file:
            for point in result:
                file.write(point["name"])
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
while usr_inp != 'quit':
    print('введите профессию:\n')
    usr_inp = input()
    copy = HHApi("log.txt", usr_inp)
    print(copy.get_vacancies())
    copy.make_file()
