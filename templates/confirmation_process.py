from abc import ABC, abstractmethod
from models.reservation import Reservation
from strategies.notification_strategy import NotificationStrategy


# Szablon metody (Template Method) – definiuje ogólny przebieg procesu potwierdzania rezerwacji,
# pozostawiając szczegóły implementacji podklasom.
class AbstractConfirmationProcess(ABC):
    def __init__(self, reservation: Reservation, strategy: NotificationStrategy):
        self.reservation = reservation  # Obiekt rezerwacji, na którym działamy
        self.strategy = strategy  # Strategia powiadomień (Email, SMS, itd.)

    # Główna metoda szablonowa – ustalona sekwencja kroków: walidacja, zmiana statusu, powiadomienie.
    def confirm(self):
        self.validate()
        self.change_status()
        self.send_notification()

    # Abstrakcyjne metody – każda podklasa musi zaimplementować własne wersje tych kroków.
    @abstractmethod
    def validate(self): ...

    @abstractmethod
    def change_status(self): ...

    @abstractmethod
    def send_notification(self): ...


# Konkretna implementacja procesu potwierdzenia rezerwacji – typ standardowy
class StandardConfirmation(AbstractConfirmationProcess):
    # Walidacja – potwierdzenie tylko jeśli rezerwacja jest "nowa"
    def validate(self):
        if self.reservation.status != "new":
            raise Exception("Rezerwacja nie może być potwierdzona.")

    # Zmiana statusu – potwierdzenie rezerwacji
    def change_status(self):
        self.reservation.confirm()

    # Wysyłka powiadomienia – przez przekazaną strategię (np. EmailStrategy)
    def send_notification(self):
        self.strategy.send(self.reservation.patient)


# Druga wersja potwierdzenia – np. gdy wymagamy płatności
class PaidConfirmation(AbstractConfirmationProcess):
    def validate(self):
        if self.reservation.status != "new":
            raise Exception("Rezerwacja nie może być potwierdzona.")

    # Zmiana statusu – najpierw symulujemy pobranie płatności, potem potwierdzenie
    def change_status(self):
        print("Pobieranie płatności...")  # Tu mogłaby być integracja z bramką płatności
        self.reservation.confirm()

    # Powiadomienie pacjenta po potwierdzeniu (np. email lub SMS)
    def send_notification(self):
        self.strategy.send(self.reservation.patient)
