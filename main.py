from get_from_api import HHApi
from get_from_api import SJApi

from utils import read_file, vacancy_cycle

if __name__ == "__main__":
    open('log.csv', 'w').close()
    usr_inp = ''

    print('Какую профессию ищем?(Одно слово):')
    copies_api_req = []
    usr_inp = input()

    usr_inp_file = "log.csv"
    while True:
        choose_site = input('что парсим?\n1 - HH\n2 - SJ\n3 - все')
        if choose_site == '1':
            copies_api_req.append(HHApi(usr_inp_file, usr_inp))
            break
        elif choose_site == '2':
            copies_api_req.append(SJApi(usr_inp_file, usr_inp))
            break
        elif choose_site == '3':
            copies_api_req.append(HHApi(usr_inp_file, usr_inp))
            copies_api_req.append(SJApi(usr_inp_file, usr_inp))
            break
        else:
            print('ошибка')
            continue

    for copy in copies_api_req:
        copy.get_vacancies()
        copy.make_file()

    read_file(usr_inp_file)

    vacancy_cycle()
