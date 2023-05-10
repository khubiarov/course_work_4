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


class CopyofVacancy(ABC):

    def __init__(self, number, profession, city, salary_from, salary_to):
        self.number = number
        self.profession = profession
        self.city = city
        self.salary_from = salary_from
        self.salary_to = salary_to

    def __str__(self):
        return f'{self.number} {self.profession} {self.city} {self.salary_from} {self.salary_to}'
    ###@classmethod
    ###def get_copy(cls):
    ###    return cls(copy.make_copy())


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




class SJApi(ReqFromApi):
    def __init__(self, file_name, name_vacancies):
        super().__init__(file_name, name_vacancies)
        self.file_name = file_name
        self.name_vacancies = name_vacancies

    def make_copy(self):
        pass

    def make_file(self):
        result = self.get_vacancies()
        with open(f'{self.file_name}', 'a', encoding='utf-8') as file:
            file_writer = csv.writer(file, delimiter=",", lineterminator="\r")
            for point in result:
                file_writer.writerow(
                    [point.get('profession'), point.get('town').get('title'), point.get("payment_from"),

                     point.get('payment_to'), point.get('link')])

    def get_vacancies(self):

        sj_token = 'v3.r.137530181.b1f12ca1e0c7b4943c11c72d08c500e0e4864152.e3587859ac72dd5bf6e192e4b5cb9199ce2292bf'
        auth_data = {'X-Api-App-Id': sj_token}

        req = requests.get(f'https://api.superjob.ru/2.0/vacancies/?keyword="{self.name_vacancies}"/',
                           headers=auth_data)

        req = req.json()
        req = json.dumps(req, ensure_ascii=False)
        req = json.loads(req)
        items_list = []
        for item in req['objects']:
            items_list.append(item)
        return items_list

def read_file(file_name):
    i = 0
    with open(f"{file_name}", 'rt', encoding='utf-8') as r_file:
        content = csv.reader(r_file, delimiter=",")
        for line in content:
            i += 1
            all_vacancies_copyes.append(CopyofVacancy(i, line[0], line[1], line[2], line[3]))
            print(f"{i}) {line[0]}; {line[1]};от {line[2]} до {line[3]} ")

        numb_of_vacancy = int(input('Какую вакансию показать подробнее?\nДальше?"N"'))
        print(all_vacancies_copyes[numb_of_vacancy - 1])

name = 'сварщик'
copy = SJApi('abr', name)
copy.get_vacancies()
copy.make_file()

all_vacancies_copyes = []

usr_inp = ''

while True:
    print('q - выйти\nКакую профессию ищем?:')
    copies_api_req = []
    usr_inp = input()
    if usr_inp.lower() == 'q':
        break
    usr_inp_file = f"{input('Имя файла лога')}.csv"
    copies_api_req.append(HHApi(usr_inp_file, usr_inp))
    copies_api_req.append(SJApi(usr_inp_file, usr_inp))

    for copy in copies_api_req:
        copy.get_vacancies()
        copy.make_file()

    read_file(usr_inp_file)

