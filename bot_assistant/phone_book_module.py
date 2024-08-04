from functools import wraps
from bot_assistant.bot_classes import *
from bot_assistant.birthdays_module import *


def input_error(func):
    @wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return str(e)
        except KeyError as e:
            name = e.args[0]
            return f"{name} is not recorded in your phone book"
        except IndexError:
            return "Enter contact name please"
    return inner


def parse_input(user_input: str):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


@input_error
def add_contact(args, book: AddressBook):
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message


@input_error
def change_contact(args: list, book: AddressBook):
    if len(args) == 3:
        name, old_phone, new_phone = args
        record = book.find(name)
        if record:
            book.data[name].edit_phone(old_phone, new_phone)
            return f"Contact {name} updated"
        else:
            raise KeyError
    else:
        return "Please, enter name, old phone, new phone"


@input_error
def show_phone(args: list, book: AddressBook):
    try:
        name = args[0]
        if book.find(name):
            for key, record in book.data.items():
                if key == name:
                    return f"{", ".join(record.phones)}"
        else:
            raise KeyError

    except KeyError:
        raise KeyError(args[0])


def show_all(book: AddressBook):
    if not book:
        return "You dont have any contact's yet."
    else:
        result = ""
        for key, value in book.items():
            result += f"{key}: {value}\n"
        return result


@input_error
def add_birthday(args, book: AddressBook):
    name, birthday = args
    record = book.find(name)
    message = f"Added Birthday for contact {name}."
    if record is None and birthday:
        record = Record(name)
        book.add_record(record)
        message = f"Added Birthday for new contact {name}."
    if birthday:
        record.add_birthday(string_to_date(birthday))
    return message


@input_error
def show_birthday(args, book: AddressBook):
    name = args[0]
    if book.find(name):
        try:
            for key, record in book.data.items():
                if key == name:
                    return record.birthday
        except ValueError:
            raise ValueError(f"Not recorded birthday for contact {name}.")
    else:
        return f"Contact {name} is not exist"


@input_error
def birthdays(book: AddressBook):
    return get_upcoming_birthdays(book)
