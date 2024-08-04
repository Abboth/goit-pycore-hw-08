from collections import UserDict
import re
from _datetime import datetime


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, value):
        super().__init__(value)


class Phone(Field):
    def __init__(self, value):
        if re.match(r"^\+?\d{0,2}\d{10}$", value):
            super().__init__(value)


class Birthday(Field):
    def __init__(self, value):
        pattern_birthday = r"(\d{2})\.(\d{2})\.(\d{4})"
        if re.match(pattern_birthday, value):
            try:
                datetime.strptime(value, "%d/%m/%y")
                super().__init__(value)
            except ValueError:
                raise ValueError(f"Date {value} is not exist")
        else:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = "has not yet been established"

    def add_phone(self, phone: str):
        self.phones.append(phone)

    def remove_phone(self, phone: str):
        try:
            for phone_number in self.phones:
                if phone_number == phone:
                    self.phones.remove(phone_number)
        except ValueError:
            print("Incorrect number")

    def edit_phone(self, old_phone: str, new_phone: str):
        if old_phone in self.phones:
            self.remove_phone(old_phone)
            self.add_phone(new_phone)

    def find_phone(self, phone: str) -> str:
        if phone in self.phones:
            for phone_number in self.phones:
                return phone_number
        else:
            print(f"phone number doesn't exist")

    def add_birthday(self, birthday):
        self.birthday = birthday

    def __str__(self):
        return f"Contact name: {self.name.value}, birthday {self.birthday}, phones: {'; '.join(p for p in self.phones)}"


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        if name in self.data:
            for key, record in self.data.items():
                if key == name:
                    return record

    def delete(self, name):
        if name in self.data:
            del self.data[name]
        else:
            print("contact is not exist")

    def __str__(self):
        result = []
        for name, record in self.data.items():
            result.append(str(record))
        return "\n".join(result)
