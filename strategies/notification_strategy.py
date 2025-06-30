from abc import ABC, abstractmethod


class NotificationStrategy(ABC):
    """
    Wzorzec: Strategia

    Abstrakcyjna klasa bazowa dla strategii powiadamiania użytkownika.
    Definiuje wspólny interfejs `send`, który musi być zaimplementowany
    przez konkretne strategie (np. EmailStrategy, SMSStrategy).

    Dzięki temu klient (np. NotifyingReservation) może dynamicznie
    wybrać sposób wysyłki powiadomienia bez znajomości szczegółów implementacji.
    """
    @abstractmethod
    def send(self, user):

        # Wysyła powiadomienie do użytkownika.
        # :param user: Obiekt użytkownika (np. pacjent), zawierający dane kontaktowe.
        pass


class EmailStrategy(NotificationStrategy):
    def send(self, user):
        # Wypisuje komunikat symulujący wysyłkę e-maila do użytkownika.
        print(f"Wysyłanie e-maila do: {user.email}")


class SMSStrategy(NotificationStrategy):
    def send(self, user):
        # Wypisuje komunikat symulujący wysyłkę SMS-a do użytkownka.
        print(f"Wysyłanie SMS-a do: {user.first_name}")
