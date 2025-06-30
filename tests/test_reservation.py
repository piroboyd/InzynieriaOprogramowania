import pytest

from models.reservation import Reservation
from models.user import Patient, Doctor
from utils.aaaaexceptions import ReservationException
from factories.user_factory import UserFactory
from services.reservation_service import ReservationService
from strategies.notification_strategy import EmailStrategy

"""
Testy jednostkowe dla klasy Reservation oraz warstwy serwisowej ReservationService.

Testowane scenariusze:

1. test_create_and_complete_reservation_with_factory:
   Używa UserFactory do utworzenia pacjenta i lekarza.
   Sprawdza cały przebieg cyklu życia rezerwacji: utworzenie → potwierdzenie → rozpoczęcie → zakończenie.
   Weryfikuje, że finalny status to "done".

2. test_start_without_confirm_raises:
   Próba rozpoczęcia wizyty bez wcześniejszego potwierdzenia.
   Spodziewany rezultat to wyjątek ReservationException – test sprawdza poprawność kontroli stanu.

3. test_cancel_reservation:
   Tworzy i potwierdza rezerwację, a następnie ją anuluje.
   Sprawdza, czy status zmienia się na "cancelled".
"""


def test_create_and_complete_reservation_with_factory():
    patient = UserFactory.create_user("patient", 1, "Test", "Patient", "patient@example.com")
    doctor = UserFactory.create_user("doctor", 2, "Test", "Doctor", "doctor@example.com")
    service = ReservationService()

    reservation = service.create_reservation("2025-08-01", patient, doctor, EmailStrategy())
    service.confirm_reservation(reservation)
    service.start_reservation(reservation)
    service.complete_reservation(reservation)

    assert reservation.status == "done"


def test_start_without_confirm_raises():
    patient = Patient(1, "A", "B", "a@b.com")
    doctor = Doctor(2, "C", "D", "c@d.com")
    reservation = Reservation("2025-08-01", patient, doctor)

    with pytest.raises(ReservationException):
        reservation.start()


def test_cancel_reservation():
    patient = UserFactory.create_user("patient", 1, "Test", "Patient", "test@example.com")
    doctor = UserFactory.create_user("doctor", 2, "Doc", "Tor", "doc@example.com")
    reservation = Reservation("2025-09-01", patient, doctor)
    reservation.confirm()
    reservation.cancel()
    assert reservation.status == "cancelled"