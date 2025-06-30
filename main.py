# main.py – demonstracja działania systemu rezerwacji wizyt lekarskich z loggerem, fabryką i strategiami

from utils.aaaaexceptions import ReservationException
from factories.user_factory import UserFactory
from models.reservation import Reservation
from decorators.notifying_reservation import NotifyingReservation
from strategies.notification_strategy import EmailStrategy, SMSStrategy
from services.logger import Logger
from services.reservation_facade import ReservationFacade
from templates.confirmation_process import StandardConfirmation, PaidConfirmation

def main():
    logger = Logger()  # Logger singleton z zapisem do pliku
    logger.log("System rezerwacji uruchomiony")

    # Tworzenie użytkowników przez fabrykę – zamiast bezpośrednio: Patient(...) / Doctor(...)
    patient = UserFactory.create_user("patient", 1, "Anna", "Kowalska", "anna@example.com")
    doctor = UserFactory.create_user("doctor", 2, "Jan", "Nowak", "jan@example.com")
    logger.log(f"Zalogowano pacjenta: {patient.email}")

    # Logowanie i rejestracja pacjenta
    patient.login()
    patient.register()

    # Tworzenie rezerwacji
    reservation = Reservation(date="2025-07-01", patient=patient, doctor=doctor)
    logger.log(f"Utworzono rezerwację na dzień {reservation.date}")

    # Wybór strategii powiadamiania
    print("Wybierz kanał powiadomienia:")
    print("1. Email")
    print("2. SMS")
    choice = input("Wpisz 1 lub 2: ")

    if choice == "1":
        channel = EmailStrategy()
    elif choice == "2":
        channel = SMSStrategy()
    else:
        print("Nieprawidłowy wybór. Domyślnie wybrano Email.")
        channel = EmailStrategy()

    # Dekorator dodający powiadamianie
    notifying_reservation = NotifyingReservation(reservation, channel)

    # Interaktywne sterowanie wizytą
    while True:
        print(f"\n[Aktualny status]: {reservation.status}")
        action = input("Co chcesz zrobić? (confirm/start/complete/cancel/exit): ").lower()

        try:
            if action == "confirm":
                notifying_reservation.confirm()
                logger.log("Rezerwacja została potwierdzona.")
            elif action == "start":
                notifying_reservation.start()
                logger.log("Wizyta została rozpoczęta.")
            elif action == "complete":
                notifying_reservation.complete()
                logger.log("Wizyta została zakończona.")
            elif action == "cancel":
                notifying_reservation.cancel()
                logger.log("Rezerwacja została anulowana.")
            elif action == "exit":
                logger.log("Zamknięto system.")
                break
            else:
                print("Nieznana komenda. Wpisz confirm/start/complete/cancel/exit.")
        except ReservationException as e:
            print(f"Błąd: {e}")
            logger.log(f"Błąd operacji: {e}")

    print("=== DEMONSTRACJA WZORCÓW PROJEKTOWYCH ===")

    # SINGLETON – logger zawsze tworzy tylko jedną instancję
    logger = Logger()
    logger.log("=== DEMONSTRACJA WZORCÓW PROJEKTOWYCH ===")

    # FACTORY – tworzenie użytkowników przez fabrykę (bez ręcznego new)
    patient = UserFactory.create_user("patient", 1, "Anna", "Kowalska", "anna@example.com")
    doctor = UserFactory.create_user("doctor", 2, "Jan", "Nowak", "jan@example.com")

    # STRATEGY + DECORATOR – strategia powiadamiania + dekorowanie rezerwacji
    print("\n[1] Wzorzec STRATEGY + DECORATOR:")
    strategy = EmailStrategy()  # wybór kanału powiadomienia (strategia)
    reservation = Reservation("2025-07-01", patient, doctor)
    notifying_reservation = NotifyingReservation(reservation, strategy)
    notifying_reservation.confirm()  # confirm + powiadomienie

    # SINGLETON – pokazanie że Logger to jedna instancja
    print("\n[2] Wzorzec SINGLETON:")
    logger2 = Logger()
    print(f"Czy logger to ta sama instancja? {logger is logger2}")
    logger.log(f"Czy logger to ta sama instancja? {logger is logger2}")
    logger2.log("To też trafia do tego samego loga.")

    # FACADE – uproszczenie obsługi procesu rezerwacji
    print("\n[3] Wzorzec FACADE:")
    facade = ReservationFacade(strategy)
    facade.full_process("2025-07-02", patient, doctor)  # pełen proces: create, confirm, start, complete

    # TEMPLATE METHOD – potwierdzanie na dwa różne sposoby
    print("\n[4] Wzorzec TEMPLATE METHOD:")
    res1 = Reservation("2025-07-03", patient, doctor)
    StandardConfirmation(res1, strategy).confirm()

    res2 = Reservation("2025-07-04", patient, doctor)
    PaidConfirmation(res2, strategy).confirm()


if __name__ == "__main__":
    main()
