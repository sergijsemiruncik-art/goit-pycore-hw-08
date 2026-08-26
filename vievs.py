from abc import ABC, abstractmethod
from collections.abc import Iterable
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from address_book import Record

class UserInterface(ABC):

    @abstractmethod
    def show_messsage(self, message: str) -> None:
        pass

    @abstractmethod
    def show_contacts(self, contacts: list) -> None:
        pass

    @abstractmethod
    def show_commands(self, commands: list) -> None:
        pass

class ContactCardFormater:

    @staticmethod
    def format_contact(record: Record) -> str:
        phones ="; ".join(phone.value for phone in record.phones) or "not set"
        birthday = record.birthday.value if record.birthday else "not set"

        return (
            "-------------------------\n"
            f"Name: {record.name.value}\n"
            f"Phones: {phones}\n"
            f"Birthday: {birthday}\n"
            "-------------------------"
        )

class ConsoleView(UserInterface):

    def __init__(self, formatter: ContactCardFormater | None = None) -> None:
        self._formatter = formatter or ContactCardFormater()

    @staticmethod
    def show_message(message: str) -> None:
        print(message)

    def show_contacts(self, contacts: Iterable["Record"]) -> None:
        cards = [self._formatter.format(contact) for contact in contacts]

        if not cards:
            self.show_message("No contacts")
            return

        self.show_message("\n".join(cards))

    def show_commands(self, commands: Iterable["str"]) -> None:
        self.show_message(
            "Available commands:\n" + "\n".join(commands)
        )