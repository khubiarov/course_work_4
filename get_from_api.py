from abc import ABC, abstractmethod
import requests
import csv
import json

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


class HHApi(ReqFromApi):
    def __init__(self, file_name, name_vacancies):

        super().__init__(file_name, name_vacancies)


    def make_file(self):
        result = self.get_vacancies()

        with open(f'{self.file_name}', 'w', encoding='utf-8') as file:
            file_writer = csv.writer(file, delimiter=",", lineterminator="\r")
            for point in result:
                if point.get('salary') is None:
                    salary_from = 0
                    salary_to = 0
                    salary_currency = 0
                else:
                    salary_from = point.get('salary').get('from')
                    salary_to = point.get('salary').get('to')
                    salary_currency = point.get('salary').get('currency')

                if point.get('address') is None:
                    address = '--'
                else:
                    address = point.get('address').get('raw')
                e_mail = '--'

                if point.get('snippet') == None:
                    description = '--'
                else:
                    description = point.get('snippet').get('requirement')
                file_writer.writerow([point.get('name'), point.get('area').get('name'), salary_from,

                                      salary_to, salary_currency, point.get('alternate_url'), address, e_mail]) #, description])



    def get_vacancies(self):
        req = requests.get('https://api.hh.ru/vacancies', {'text': self.name_vacancies})
        data = req.content.decode()  # спер из одного мануала

        req.close()

        json.dumps(data)
        data = json.loads(data)

        items_list = []
        with open('hh_log.txt', 'wt')as file:
            file.write(str(data))
        for item in data['items']:
            items_list.append(item)

        return items_list


class SJApi(ReqFromApi):
    def __init__(self, file_name, name_vacancies):
        super().__init__(file_name, name_vacancies)
        self.file_name = file_name
        self.name_vacancies = name_vacancies


    def make_file(self):
        result = self.get_vacancies()
        with open(f'{self.file_name}', 'a', encoding='utf-8') as file:
            file_writer = csv.writer(file, delimiter=",", lineterminator="\r")
            for point in result:
                file_writer.writerow(
                    [point.get('profession'), point.get('town').get('title'), point.get("payment_from"),

                     point.get('payment_to'), point.get('currency'), point.get('link'), point.get('address'),
                     point.get('email')]) #, point.get('candidat')][0:100])

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


