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

    def __init__(self, number, profession, city, salary_from, salary_to, currency, link, address): #description):
        self.number = number
        self.profession = profession
        self.city = city
        self.salary_from = salary_from
        self.salary_to = salary_to
        self.currency = currency
        self.link = link
        self.address = address
        #self.description = description
    def __str__(self):
        return f'{self.number} {self.profession} {self.city} {self.salary_from} {self.salary_to} {self.currency}' \
               f'\nСсылка на вакансию: {self.link} ' \
               f'\nАдрес: {self.address}'
               #f'Описание вакансии: {self.description}'
               #f'\nАдрес: {self.address}'
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
                if point.get('salary') is None:
                    salary_from = '--'
                    salary_to = '--'
                    salary_currency = '--'
                else:
                    salary_from = point.get('salary').get('from')
                    salary_to = point.get('salary').get('to')
                    salary_currency = point.get('salary').get('currency')


                file_writer.writerow([point.get('name'), point.get('area').get('name'), salary_from,

                                      salary_to, salary_currency, point.get('url'), point.get('address')])

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

    def make_copy(self):
        pass

    def make_file(self):
        result = self.get_vacancies()
        with open(f'{self.file_name}', 'a', encoding='utf-8') as file:
            file_writer = csv.writer(file, delimiter=",", lineterminator="\r")
            for point in result:
                file_writer.writerow(
                    [point.get('profession'), point.get('town').get('title'), point.get("payment_from"),

                     point.get('payment_to'), point.get('currency'), point.get('link'), point.get('address')])

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
    while True:
        i = 0
        with open(f"{file_name}", 'rt', encoding='utf-8') as r_file:
            content = csv.reader(r_file, delimiter=",")
            for line in content:
                i += 1

                if line[4] is None:
                    line_4 = '--'
                else:
                    line_4 = line[4]

                #создаем копии
                all_vacancies_copyes.append(CopyofVacancy(i, line[0], line[1], line[2], line[3], line_4, line[5], line[6]))
                print(f"{i}) {line[0]}; {line[1]};от {line[2]} до {line[3]} {line[4]} ")

                if i % 10 == 0:
                    numb_of_vacancy = input('Какую вакансию показать подробнее?\n"N" - Дальше\n"Q" - Выход\n')
                    if numb_of_vacancy.isdigit():
                        if int(numb_of_vacancy) > i:
                            print('Ошибка , нет такой вакансии')
                            break
                        else:
                            print(all_vacancies_copyes[int(numb_of_vacancy) - 1])
                            input('нажмите enter')
                            break
                    elif numb_of_vacancy == 'N'.lower():
                        continue
                    elif numb_of_vacancy == 'Q'.lower():
                        exit()


                    else:
                        print('Ошибка,нет такой команды')
                        break

all_vacancies_copyes = []

usr_inp = ''


print('q - выйти\nКакую профессию ищем?:')
copies_api_req = []
usr_inp = input()

usr_inp_file = "log.csv"
# это для полиморфизма
copies_api_req.append(HHApi(usr_inp_file, usr_inp))
copies_api_req.append(SJApi(usr_inp_file, usr_inp))

for copy in copies_api_req:
    copy.get_vacancies()
    copy.make_file()

while True:
    read_file(usr_inp_file)

