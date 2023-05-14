import csv
from vacancy import CopyofVacancy


def read_file(file_name):
    i = 0
    with open(f"{file_name}", 'rt', encoding='utf-8') as r_file:
        content = csv.reader(r_file, delimiter=";")
        for line in content:
            i += 1

            # создаем копии
            all_vacancies_copyes.append(CopyofVacancy(i, line[0], line[1], line[2], line[3], line[4], line[5], line[6],
                                                      line[7]))


def vacancy_cycle():
    if input('сортируем по за Y').lower() == 'y':
        all_vacancies_copyes.sort()
    i = 0

    for vac in all_vacancies_copyes:

        print(vac)
        i += 1

        if i % 10 == 0:
            numb_of_vacancy = input(
                '"N" - Дальше\n"Q" - Выход\n')
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
