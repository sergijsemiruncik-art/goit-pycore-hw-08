# goit-pycore-hw-08
Console assistant bot for managing an address book.

The bot stores contacts in an AddressBook object. Each contact is a Record with a name, one or more phone numbers, and an optional birthday.

Requirements

Python 3
Phone numbers must contain exactly 10 digits.
Birthdays must use the DD.MM.YYYY format.
How to Run

Run the bot from the project directory:

python3 bot.py
After startup, enter commands in the console.

Commands

hello

Get a greeting from the bot.

hello
add [name] [phone]

Add a new contact with a phone number. If the contact already exists, the phone number is added to the existing contact.

add Alice 1234567890
change [name] [old_phone] [new_phone]

Replace an existing phone number for a contact.

change Alice 1234567890 0987654321
phone [name]

Show all phone numbers for a contact.

phone Alice
all

Show all contacts in the address book.

all
add-birthday [name] [birthday]

Add a birthday to an existing contact. The birthday must be in DD.MM.YYYY format.

add-birthday Alice 31.12.2000
show-birthday [name]

Show the birthday for a contact.

show-birthday Alice
birthdays

Show contacts with birthdays in the next 7 days. If a birthday falls on a weekend, the congratulation date is moved to the next Monday.

birthdays
close or exit

Close the bot.

close
