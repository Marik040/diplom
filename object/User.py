from datetime import datetime


class User:

    def __init__(self, id, name, sex, city, bdate, relation):
        self.id = id
        self.name = name
        self.sex = sex
        self.city = city
        self.bdate = bdate
        self.relation = relation

    def get_age(self):
        curent_year = datetime.now().year
        user_year = int(self.bdate.split('.')[2])
        age = curent_year - user_year
        age_from: int = age - 5
        age_to: int = age + 5
        result = {'age_from': age_from, 'age_to': age_to}
        return result
