class CopyofVacancy:

    def __init__(self, number, profession, city, salary_from, salary_to, currency, link, address,
                 email):  # description):
        if salary_from.isdigit():
            self.salary_from = salary_from
        else:
            self.salary_from = 0
        self.number = number
        self.profession = profession
        self.city = city

        self.salary_to = salary_to
        self.currency = currency
        self.link = link
        self.address = address
        self.email = email
        # self.description = description
        print(self.__str__())

    def __str__(self):

        return f'{self.number} {self.profession} {self.city} от {self.salary_from} до {self.salary_to} {self.currency}' \
               f' Ссылка на вакансию: {self.link} ' \
               f' Адрес: {self.address} E-mail:{self.email}'
        # f'\nОписание вакансии: {self.description}'

    def __lt__(self, other):
        return int(self.salary_from) < int(other.salary_from)

    # def __repr__(self):
    #   return self.salary_from
    # f'\nАдрес: {self.address}'
    ###@classmethod
    ###def get_copy(cls):
    ###    return cls(copy.make_copy())
