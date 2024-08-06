import pickle
from bot_assistant.bot_classes import AddressBook
from bot_assistant.phone_book_module import input_error


def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)

@input_error
def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        raise FileNotFoundError
