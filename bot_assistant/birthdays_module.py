from datetime import datetime, date, timedelta
from bot_assistant.bot_classes import AddressBook


def string_to_date(date_string):
    try:
        return datetime.strptime(date_string, "%d.%m.%Y").date()
    except ValueError:
        raise ValueError(f"Date {date_string} isn't exist")


def date_to_string(date_obj):
    return date_obj.strftime("%d.%m.%Y")


def prepare_user_list(user_data):
    prepared_list = []
    for user in user_data:
        prepared_list.append({"name": user["name"], "birthday": string_to_date(user["birthday"])})
    return prepared_list


def find_next_weekday(start_date, weekday):
    days_ahead = weekday - start_date.weekday()
    if days_ahead <= 0:
        days_ahead += 7
    return start_date + timedelta(days=days_ahead)


def adjust_for_weekend(birthday):
    if birthday.weekday() >= 5:
        return find_next_weekday(birthday, 0)
    return birthday


def get_upcoming_birthdays(book: AddressBook, days=7):
    upcoming_birthdays = []
    today = date.today()
    for name, record in book.data.items():
        birthday_this_year = record.birthday.replace(year=today.year)
        if birthday_this_year < today:
            birthday_this_year = birthday_this_year.replace(year=today.year + 1)

        if 0 <= (birthday_this_year - today).days <= days:
            birthday_this_year = adjust_for_weekend(birthday_this_year)

            congratulation_date_str = date_to_string(birthday_this_year)
            upcoming_birthdays.append({"name": record.name.value, "congratulation_date": congratulation_date_str})
    output = ""
    for record in upcoming_birthdays:
        output += f"{record['name']} birthday is {record['congratulation_date']}\n"
    return f"Upcoming birthdays:\n{output}"

