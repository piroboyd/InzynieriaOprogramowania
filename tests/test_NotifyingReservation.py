from decorators.notifying_reservation import NotifyingReservation
from models.reservation import Reservation
from models.user import Patient, Doctor
from unittest.mock import MagicMock
from factories.user_factory import UserFactory


"""
Testy jednostkowe dla dekoratora NotifyingReservation, który rozszerza klasę Reservation
o możliwość wysyłania powiadomień przy potwierdzeniu wizyty.

Testowane scenariusze:

1. test_notifying_reservation_calls_notification:
   Sprawdza, czy metoda confirm() w dekoratorze wywołuje strategię powiadamiania
   (mock_strategy.send) z odpowiednim użytkownikiem (pacjentem).

2. test_notification_sent:
   Weryfikuje, że strategia powiadamiania została wywołana dokładnie raz po potwierdzeniu wizyty.
   Użytkownicy są tworzeni przez fabrykę UserFactory.
"""


def test_notifying_reservation_calls_notification():
    patient = Patient(1, "Anna", "Kowalska", "anna@example.com")
    doctor = Doctor(2, "Jan", "Nowak", "jan@example.com")
    reservation = Reservation("2025-08-10", patient, doctor)

    mock_strategy = MagicMock()
    notifying = NotifyingReservation(reservation, mock_strategy)

    notifying.confirm()

    mock_strategy.send.assert_called_once_with(patient)


def test_notification_sent():
    patient = UserFactory.create_user("patient", 1, "Anna", "Kowalska", "anna@example.com")
    doctor = UserFactory.create_user("doctor", 2, "Jan", "Nowak", "jan@example.com")

    reservation = Reservation("2025-08-10", patient, doctor)
    mock_strategy = MagicMock()
    wrapper = NotifyingReservation(reservation, mock_strategy)
    wrapper.confirm()
    mock_strategy.send.assert_called_once()
