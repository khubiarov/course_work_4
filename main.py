from get_from_api import HHApi
from get_from_api import SJApi
from vacancy import CopyofVacancy
import csv


def read_file(file_name):
    i = 0
    with open(f"{file_name}", 'rt', encoding='utf-8') as r_file:
        content = csv.reader(r_file, delimiter=",")
        for line in content:

            i += 1

            if line[4] is None:
                line_4 = 0
            else:
                line_4 = line[4]

            # создаем копии
            all_vacancies_copyes.append(CopyofVacancy(i, line[0], line[1], line[2], line[3], line_4, line[5], line[6],
                                                      line[7]))


def vacancy_cycle():
    i = 0




    for vac in all_vacancies_copyes:

        print(vac)
        i += 1

        if i % 10 == 0:
            numb_of_vacancy = input(
                'Какую вакансию показать подробнее?\nЦифра - номер позиции\n"N" - Дальше\n"Q" - Выход\n')
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


if __name__ == "__main__":
    all_vacancies_copyes = []

    usr_inp = ''

    print('q - выйти\nКакую профессию ищем?(Одно слово):')
    copies_api_req = []
    usr_inp = input()

    usr_inp_file = "log.csv"
    # это для полиморфизма
    copies_api_req.append(HHApi(usr_inp_file, usr_inp))
    copies_api_req.append(SJApi(usr_inp_file, usr_inp))

    for copy in copies_api_req:
        copy.get_vacancies()
        copy.make_file()

    #while True:
    read_file(usr_inp_file)


    if input('сортируем по за Y').lower() == 'y':
        all_vacancies_copyes.sort()

        vacancy_cycle()