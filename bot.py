from address_book import AddressBook, Record
from vievs import ConsoleView, UserInterface
import pickle

DATA_FILE = "addressbook.pkl"

COMMANDS = (
    "hello",
    "add [name] [phone]",
    "change [name] [old_phone] [new_phone]",
    "phone [name]",
    "add-birthday [name] [DD.MM.YYYY]",
    "show-birthday [name]",
    "birthdays",
    "all",
    "close / exit",
)

def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except AttributeError:
            return "Contact not found."
    return wrapper

# Parses user input by splitting it into command and arguments
def parse_input(user_input: str):
    cmd, *args = user_input.strip().split()
    cmd = cmd.lower()
    return cmd, args


# Adds a new contact or phone number to an existing contact
# Requires: name and phone number as arguments
def add_contact(args, book):
    if len(args) != 2:
        return "Please enter name and phone number."

    name, phone = args
    record = book.find(name)

    if record is None:
        record = Record(name)
        book.add_record(record)

    record.add_phone(phone)
    return "Contact added."


# Changes an existing phone number for a contact
# Requires: name, old phone number, and new phone number
@input_error
def change_contact(args, book):
    if len(args) != 3:
        return "Please enter name, old phone number and new phone number."

    name, old_phone, new_phone = args
    record = book.find(name)

    record.edit_phone(old_phone, new_phone)
    return "Contact updated."


# Displays all phone numbers for a specific contact
# Requires: contact name
@input_error
def show_phone(args, book):
    if len(args) != 1:
        return "Please enter a username."

    name = args[0]
    record = book.find(name)

    return "; ".join(phone.value for phone in record.phones)


# Adds a birthday to a contact
# Requires: name and birthday in DD.MM.YYYY format
@input_error
def add_birthday(args, book):
    if len(args) != 2:
        return "Please enter name and birthday."

    name, birthday = args
    record = book.find(name)

    record.add_birthday(birthday)
    return "Birthday added."


# Displays the birthday for a specific contact
# Requires: contact name
@input_error
def show_birthday(args, book):
    if len(args) != 1:
        return "Please enter a username."

    name = args[0]
    record = book.find(name)

    if record.birthday is None:
        return "Birthday not found."

    return record.birthday.value


# Shows all upcoming birthdays for the next 7 days
def show_birthdays(args, book):
    if args:
        return "The birthdays command does not accept arguments."

    birthdays = book.get_upcoming_birthdays()

    if not birthdays:
        return "No upcoming birthdays."

    return "\n".join(
        f"{item['name']}: {item['birthday']}" for item in birthdays
    )


# Displays all contacts in the address book
def show_all(book):
    if not book.data:
        return "No contacts saved."

    return str(book)

def save_data(book):
    with open(DATA_FILE, "wb") as f:
        pickle.dump(book, f)

def load_data():
    try:
        with open(DATA_FILE, "rb") as file:
            deserialized_data = pickle.load(file)

        if isinstance(deserialized_data, AddressBook):
            return deserialized_data

        print("Data file contains invalid data. Starting with an empty address book.")
        return AddressBook()

    except (FileNotFoundError, EOFError, pickle.UnpicklingError):
        print("No existing data file found. Starting with an empty address book.")
        return AddressBook()

# Main function that runs the interactive bot loop
def main():

    view = ConsoleView()
    # Initialize the address book
    book = load_data()

    # Display welcome message and available commands
    view.show_message("Welcome to the assistant bot!")
    view.show_commands(COMMANDS)

    # Main event loop for processing user commands
    while True:
        user_input = input("Enter a command: ")

        try:
            command, args = parse_input(user_input)
        except ValueError:
            view.show_message("Please enter a command.")
            continue

        # Handle exit commands
        if command in ("close", "exit"):
            save_data(book)
            view.show_message("Good bye!")
            break

        # Greet the user
        elif command == "hello":
            view.show_message("How can I help you?")

        # Add a new contact with phone number
        elif command == "add":
            try:
                view.show_message(add_contact(args, book))
            except ValueError as error:
                view.show_message(error)

        # Change existing phone number for a contact
        elif command == "change":
            try:
                view.show_message(change_contact(args, book))
            except ValueError as error:
                view.show_message(error)

        # Display phone numbers for a contact
        elif command == "phone":
            view.show_message(show_phone(args, book))

        # Add birthday to a contact
        elif command == "add-birthday":
            try:
                view.show_message(add_birthday(args, book))
            except (TypeError, ValueError) as error:
                view.show_message(error)

        # Show birthday for a specific contact
        elif command == "show-birthday":
            view.show_message(show_birthday(args, book))

        # Show upcoming birthdays for the next 7 days
        elif command == "birthdays":
            view.show_message(show_birthdays(args, book))

        # Display all contacts
        elif command == "all":
            view.show_contacts(book.data.values())

        # Handle invalid commands
        else:
            view.show_message("Invalid command.")


if __name__ == "__main__":
    main()
