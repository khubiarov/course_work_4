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

    @abstractmethod
    def make_copy(self):
        pass
    @abstractmethod
    def read_file(self):
        pass


class CopyofVacancy(ABC):

    def __init__(self, number, profession, city, salary_from, salary_to):
        self.number = number
        self.profession = profession
        self.city = city
        self.salary_from = salary_from
        self.salary_to = salary_to
    ###@classmethod
    ###def get_copy(cls):
    ###    return cls(copy.make_copy())
class HHApi(ReqFromApi):
    def __init__(self, file_name, name_vacancies):
        self.i = 0
        super().__init__(file_name, name_vacancies)

    def make_copy(self):
        pass


    def make_file(self):
        result = self.get_vacancies()
        with open(f'{self.file_name}', 'w', encoding='utf-8') as file:
            file_writer = csv.writer(file, delimiter=",", lineterminator="\r")
            for point in result:
                if point.get('salary').get('from') is None:
                    point['salary']['from'] = '--'

                if point.get('salary').get('to') is None:
                    point['salary']['to'] = '--'
                file_writer.writerow([point.get('name'), point.get('area').get('name'), point.get('salary').get('from'),

                         point.get('salary').get('to'), point.get('apply_alternate_url')])

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

    def read_file(self):

        with open(f"{self.file_name}", 'rt', encoding='utf-8') as r_file:
            content = csv.reader(r_file, delimiter=",")
            for line in content:
                self.i += 1
                all_vacancies_copyes.append(CopyofVacancy(self.i, line[0], line[1], line[2], line[3]))
                print(f"{line[0]}; {line[1]};от {line[2]} до {line[3]} ")
                if self.i == 10:
                    input('Дальше? (press any key)')
class SJApi(ReqFromApi):
    pass
all_vacancies_copyes = []
usr_inp = ''
while True:
    print('Какую профессию ищем:\nquit - выйти')
    usr_inp = input()
    if usr_inp == 'quit'.lower():
        break
    copy = HHApi(f"{input('Имя файла лога')}.csv", usr_inp)
    copy.get_vacancies()
    copy.make_file()
    copy.read_file()
    print(all_vacancies_copyes)