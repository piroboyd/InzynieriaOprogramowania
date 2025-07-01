import os
import tempfile
import pytest

from factories.user_factory import UserFactory
from models.reservation import Reservation
from decorators.notifying_reservation import NotifyingReservation
from strategies.notification_strategy import EmailStrategy, SMSStrategy
from services.logger import Logger
from services.reservation_facade import ReservationFacade
from utils.aaaaexceptions import ReservationException


class TestSimpleIntegration:

    def setup_method(self):
        """Przygotowanie środowiska testowego z tymczasowym plikiem logu"""
        self.temp_log = tempfile.NamedTemporaryFile(delete=False)
        self.temp_log_path = self.temp_log.name
        self.temp_log.close()

        # Reset singleton instance for clean testing
        Logger._instance = None
        logger = Logger()
        logger.log_file = self.temp_log_path

    def teardown_method(self):
        """Usuwanie tymczasowych plików po każdym teście"""
        if os.path.exists(self.temp_log_path):
            os.remove(self.temp_log_path)
        Logger._instance = None

    def test_complete_reservation_workflow(self):
        """Testuje cały przebieg rezerwacji z powiadomieniami"""
        # Create users via factory
        patient = UserFactory.create_user("patient", 1, "Anna", "Test", "anna@test.com")
        doctor = UserFactory.create_user("doctor", 2, "Jan", "Test", "jan@test.com")

        # Create reservation with notification
        reservation = Reservation("2025-07-15", patient, doctor)
        email_strategy = EmailStrategy()
        notifying_reservation = NotifyingReservation(reservation, email_strategy)

        # Log the test start
        logger = Logger()
        logger.log("Integration test started")

        # Test workflow
        assert reservation.status == "new"
        notifying_reservation.confirm()
        assert reservation.status == "confirmed"
        notifying_reservation.start()
        assert reservation.status == "in_progress"
        notifying_reservation.complete()
        assert reservation.status == "done"

        # Verify logging
        with open(self.temp_log_path, "r") as f:
            content = f.read()
            assert "Integration test started" in content

    def test_facade_integration(self):
        """Test wzorca Fasada — cały proces przez jedną klasę"""
        patient = UserFactory.create_user("patient", 3, "Maria", "Test", "maria@test.com")
        doctor = UserFactory.create_user("doctor", 4, "Piotr", "Test", "piotr@test.com")

        facade = ReservationFacade(EmailStrategy())
        reservation = facade.full_process("2025-08-01", patient, doctor)

        assert reservation.status == "done"

    def test_error_handling(self):
        """Test obsługi wyjątków — np. złej kolejności operacji"""
        patient = UserFactory.create_user("patient", 5, "Test", "Error", "error@test.com")
        doctor = UserFactory.create_user("doctor", 6, "Doc", "Error", "doc@test.com")

        reservation = Reservation("2025-10-01", patient, doctor)
        notifying_reservation = NotifyingReservation(reservation, EmailStrategy())

        # Try to start without confirming
        with pytest.raises(ReservationException):
            notifying_reservation.start()

        # Confirm first
        notifying_reservation.confirm()

        # Try to confirm again
        with pytest.raises(ReservationException):
            notifying_reservation.confirm()

    def test_singleton_logger(self):
        """Test, czy Logger działa jako singleton"""
        logger1 = Logger()
        logger2 = Logger()

        assert logger1 is logger2

        logger1.log("Test message 1")
        logger2.log("Test message 2")

        with open(self.temp_log_path, "r") as f:
            content = f.read()
            assert "Test message 1" in content
            assert "Test message 2" in content

    def test_different_notification_strategies(self):
        """Test działania dwóch strategii powiadamiania"""
        patient = UserFactory.create_user("patient", 7, "Strategy", "Test", "strategy@test.com")
        doctor = UserFactory.create_user("doctor", 8, "Pattern", "Test", "pattern@test.com")

        # Email strategy
        email_reservation = Reservation("2025-12-01", patient, doctor)
        email_notifying = NotifyingReservation(email_reservation, EmailStrategy())
        email_notifying.confirm()
        assert email_reservation.status == "confirmed"

        # SMS strategy
        sms_reservation = Reservation("2025-12-02", patient, doctor)
        sms_notifying = NotifyingReservation(sms_reservation, SMSStrategy())
        sms_notifying.confirm()
        assert sms_reservation.status == "confirmed"