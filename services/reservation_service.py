from models.reservation import Reservation
from strategies.notification_strategy import NotificationStrategy  # tylko typ
from strategies.notification_strategy import EmailStrategy  # domyślnie


class ReservationService:
    """
    Warstwa serwisowa zarządzająca rezerwacjami wizyt lekarskich.
    """

    def create_reservation(self, date, patient, doctor, channel: NotificationStrategy = None):
        """
        Tworzy nową rezerwację, wysyła powiadomienie do pacjenta
        i symuluje zapis do bazy danych.
        """
        if channel is None:
            channel = EmailStrategy()

        reservation = Reservation(date, patient, doctor)
        print("Validacja rezerwacji...")
        channel.send(patient)
        print("Zapis do bazy danych (symulacja)...")
        return reservation

    def confirm_reservation(self, reservation):
        reservation.confirm()

    def start_reservation(self, reservation):
        reservation.start()

    def complete_reservation(self, reservation):
        reservation.complete()

    def cancel_reservation(self, reservation):
        reservation.cancel()
