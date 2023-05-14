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

    def make_file(self):
        result = self.get_vacancies()
        with open(f'{self.file_name}', 'a', encoding='utf-8') as file:
            file_writer = csv.writer(file, delimiter=";", lineterminator="\r")
            for point in result:
                file_writer.writerow(
                    [point[0], point[1], point[2],

                     point[3], point[4], point[5], point[6],
                     point[7]])



class HHApi(ReqFromApi):
    def __init__(self, file_name, name_vacancies):

        super().__init__(file_name, name_vacancies)


    def get_vacancies(self):
        req = requests.get('https://api.hh.ru/vacancies', {'text': self.name_vacancies})
        data = req.content.decode()  # спер из одного мануала

        req.close()

        json.dumps(data)
        data = json.loads(data)

        items_list = []

        for item in data['items']:
            if item.get('salary') is None:
                item['salary'] = {}
                item["salary"]['to'] = 0
                item['salary']['currency'] = '--'
                item['salary']['from'] = 0

            if item.get('address') is None:
                item['address'] = {}
                item['address']['raw'] = '--'

            e_mail = ''
            item_lst = [item['name'], item['area']['name'], item['salary']['from'], item['salary']['to'],
                        item['salary']['currency'], item['apply_alternate_url'], item['address']['raw'], e_mail]
            items_list.append(item_lst)

        return items_list


class SJApi(ReqFromApi):
    def __init__(self, file_name, name_vacancies):
        super().__init__(file_name, name_vacancies)
        self.file_name = file_name
        self.name_vacancies = name_vacancies

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
            item_lst = [item.get('profession'), item.get('town').get('title'), item.get("payment_from"),

                        item.get('payment_to'), item.get('currency'), item.get('link'), item.get('address'),
                        item.get('email')]
            items_list.append(item_lst)

        return items_list
