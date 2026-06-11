from collections import UserDict
from datetime import datetime, date, timedelta
# Base class for all contact field types
class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

# Field class for storing contact name
class Name(Field):
        def __init__(self, name):
            super().__init__(name)
            self.name = name

# Field class for storing and validating phone numbers
# Validates that phone is a 10-digit string
class Phone(Field):
    def __init__(self, phone: str):
        if not isinstance(phone, str) or len(phone) != 10 or not phone.isdigit():
            raise ValueError('Phone must be 10 digits')
        super().__init__(phone)

# Field class for storing and validating birthdays
# Converts string input to datetime object in DD.MM.YYYY format
class Birthday(Field):
    def __init__(self, value: str):
        try:
            if not isinstance(value, str):
                raise ValueError('Birthday must be a string')

            datetime.strptime(value, '%d.%m.%Y')  # Validate date format
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

        super().__init__(value)

# Represents a single contact record with name, phones, and birthday
class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    # Adds a phone number to the contact
    def add_phone(self, phone: str):
        self.phones.append(Phone(phone))

    # Edits an existing phone number by replacing old with new
    def edit_phone(self, old_phone, new_phone):
        if self.find_phone(old_phone) is not None:
            self.add_phone(new_phone)
            self.remove_phone(old_phone)
            return True
        raise ValueError(f"Phone {old_phone} not found in contact {self.name.value}")

    # Searches for a phone number in the contact's phone list
    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    # Removes a phone number from the contact
    def remove_phone(self, phone: str):
        found = self.find_phone(phone)
        if found is not None:
            self.phones.remove(found)
            return True
        return False

    # Adds a birthday to the contact
    def add_birthday(self, birthday: str):
        self.birthday = Birthday(birthday)

    # String representation of the contact record
    def __str__(self):
        birthday = self.birthday.value if self.birthday else "not set"
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, birthday: {birthday}"

# Address book class that manages a collection of contact records
# Inherits from UserDict for dictionary-like functionality
class AddressBook(UserDict):

    # Adds a new contact record to the address book
    def add_record(self, record: Record):
        self.data[record.name.value] = record

    # Searches for a contact by name
    def find(self, name):
        return self.data.get(name)

    # Deletes a contact by name
    def delete(self, name):
        if name in self.data:
            del self.data[name]
            return True
        return False

    # Finds the next occurrence of a specific weekday from a start date
    def find_next_weekday(self, start_date, weekday):
        days_ahead = weekday - start_date.weekday()

        if days_ahead <= 0:
            days_ahead += 7
        return start_date + timedelta(days=days_ahead)

    # Adjusts birthday date to the next Monday if it falls on a weekend
    def adjust_for_weekend(self, birthday: date):
        if birthday.weekday() >= 5:  # 5 = Saturday, 6 = Sunday
            return self.find_next_weekday(birthday, 0)  # 0 = Monday

        return birthday

    # Returns a list of upcoming birthdays within the specified number of days
    # Default is 7 days (next week)
    def get_upcoming_birthdays(self, days=7):
        upcoming_birthdays = []
        today = date.today()

        # Iterate through all contacts in the address book
        for record in self.data.values():
            if record.birthday is None:
                continue

            # Get the birthday date and adjust to current year
            birthday = datetime.strptime(record.birthday.value, "%d.%m.%Y").date()
            birthday_this_year = birthday.replace(year=today.year)

            # If birthday already passed this year, move to next year
            if birthday_this_year < today:
                birthday_this_year = birthday_this_year.replace(year=today.year + 1)

            # Check if birthday is within the specified date range
            if 0 <= (birthday_this_year - today).days <= days:
                # Adjust for weekend if necessary
                congratulation_date = self.adjust_for_weekend(birthday_this_year)

                upcoming_birthdays.append({
                    "name": record.name.value,
                    "birthday": congratulation_date.strftime("%d.%m.%Y")
                })

        return upcoming_birthdays

    # String representation of all contacts in the address book
    def __str__(self):
        return '\n'.join(str(record) for record in self.data.values())
