import datetime
import json


class Student:
    def __init__(self, id_, name, surname, birthday, grade=None, parent_name=None, parent_patronymic=None, parent_surname=None,
                 parent_birthday=None, parent_passport_number=None, parent_passport_date=None,
                 parent_passport_certifying_organization=None, parent_email=None, parent_phone=None):
        self.id = id_
        self.name = name
        self.surname = surname
        # self.birthday = datetime.datetime.strptime(birthday, '%Y-%m-%d')
        self.birthday = birthday
        self.grade = grade  # класс

        self.parent_name = parent_name
        self.parent_surname = parent_surname
        self.parent_patronymic = parent_patronymic
        self.parent_birthday = parent_birthday

        self.parent_email = parent_email
        self.parent_phone = parent_phone

        self.parent_passport_number = parent_passport_number
        self.parent_passport_date = parent_passport_date
        self.parent_passport_certifying_organization = parent_passport_certifying_organization

    def __repr__(self):
        return f'{self.name} {self.surname}'


    def resp_json(self):
        resp = {'id': self.id, 'name': self.name, 'surname': self.surname, 'birthday': self.birthday, 'grade': self.grade, 'parent_name': self.parent_name, 'parent_surname': self.parent_surname, 'parent_patronymic': self.parent_patronymic, 'parent_birthday': self.parent_birthday, 'parent_email': self.parent_email, 'parent_phone': self.parent_phone, 'parent_passport_number': self.parent_passport_number, 'parent_passport_date': self.parent_passport_date, 'parent_passport_certifying_organization': self.parent_passport_certifying_organization}
        resp = {key: val for key, val in resp.items() if val}
        return json.dumps(resp, indent=4, sort_keys=True, default=str)

    @property
    def age(self):
        """Возвращает возраст студента"""
        return round((datetime.datetime.now() - self.birthday).days / 365)


class StudentJunior(Student):
    def __init__(self, id_, name, surname, birthday, birth_certificate_series=None, birth_certificate_number=None,
                 birth_certificate_date=None, birth_certificate_organization=None):
        super().__init__(id_, name, surname, birthday)
        self.birth_certificate_series = birth_certificate_series
        self.birth_certificate_number = birth_certificate_number
        self.birth_certificate_date = birth_certificate_date
        self.birth_certificate_organization = birth_certificate_organization


class StudentMiddle(StudentJunior):
    def __init__(self, id_, name, surname, birthday, student_passport_series=None, student_passport_number=None,
                 student_passport_date=None, student_passport_certifying_organization=None):
        super().__init__(id_, name, surname, birthday, )
        self.student_passport_series = student_passport_series
        self.student_passport_number = student_passport_number
        self.student_passport_date = student_passport_date
        self.student_passport_certifying_organization = student_passport_certifying_organization

