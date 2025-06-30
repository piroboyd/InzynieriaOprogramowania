from models.reservation import Reservation
from strategies.notification_strategy import NotificationStrategy


class NotifyingReservation:

    # Dekorator (wrapper) dla klasy Reservation, rozszerzający jej funkcjonalność o wysyłanie
    # powiadomień do pacjenta po potwierdzeniu wizyty.
    def __init__(self, reservation: Reservation, channel: NotificationStrategy):
        # :param reservation: Obiekt klasy Reservation (wizyty).
        # :param channel: Obiekt strategii powiadamiania (np. EmailStrategy, SMSStrategy).
        self._reservation = reservation  # Obiekt klasy Reservation
        self._channel = channel  # Strategia wysyłania powiadomień

    def confirm(self):
        # Potwierdza rezerwację i wysyła powiadomienie do pacjenta.
        self._reservation.confirm()
        self._channel.send(self._reservation.patient)

    def start(self):
        # Rozpoczyna wizytę – deleguje do oryginalnej rezerwacji.
        self._reservation.start()

    def complete(self):
        # Kończy wizytę – deleguje do oryginalnej rezerwacji.
        self._reservation.complete()

    def cancel(self):
        # Anuluje wizytę – deleguje do oryginalnej rezerwacji.
        self._reservation.cancel()
