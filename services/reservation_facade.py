# Fasada dla procesu rezerwacji – uproszczenie interfejsu do obsługi procesu rezerwacji.
# Klient korzysta tylko z jednej klasy, nie musi znać szczegółów działania ReservationService i strategii powiadomień.
from services.reservation_service import ReservationService
from strategies.notification_strategy import NotificationStrategy
from models.user import Patient, Doctor


class ReservationFacade:
    def __init__(self, strategy: NotificationStrategy):
        # Inicjalizacja serwisu i strategii (np. EmailStrategy, SMSStrategy)
        self._service = ReservationService()
        self._strategy = strategy

    # Metoda upraszczająca stworzenie i potwierdzenie rezerwacji – jeden krok dla użytkownika
    def create_and_confirm_reservation(self, date: str, patient: Patient, doctor: Doctor):
        reservation = self._service.create_reservation(date, patient, doctor, self._strategy)
        self._service.confirm_reservation(reservation)
        return reservation

    # Pełny proces: stworzenie → potwierdzenie → rozpoczęcie → zakończenie wizyty
    def full_process(self, date: str, patient: Patient, doctor: Doctor):
        reservation = self.create_and_confirm_reservation(date, patient, doctor)
        self._service.start_reservation(reservation)
        self._service.complete_reservation(reservation)
        return reservation
