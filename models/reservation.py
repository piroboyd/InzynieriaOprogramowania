from utils.aaaaexceptions import ReservationException


class Reservation:
    """
    Klasa reprezentująca rezerwację wizyty lekarskiej.
    Obsługuje cykl życia wizyty: nowa → potwierdzona → w trakcie → zakończona / anulowana.
    """

    def __init__(self, date, patient, doctor):
        """
        Inicjalizacja rezerwacji.
        :param date: Data wizyty.
        :param patient: Obiekt pacjenta (instancja klasy Patient).
        :param doctor: Obiekt lekarza (instancja klasy Doctor).
        """
        self.date = date
        self.patient = patient
        self.doctor = doctor
        self.status = "new"  # Domyślny status to "nowa"

    def confirm(self):
        # Potwierdzenie rezerwacji. Dozwolone tylko jeśli aktualny status to "new".
        if self.status != "new":
            raise ReservationException("Nie można potwierdzić rezerwacji w obecnym stanie.")
        self.status = "confirmed"
        print("Rezerwacja została potwierdzona.")

    def start(self):
        # Rozpoczęcie wizyty.Dozwolone tylko jeśli status to "confirmed".
        if self.status != "confirmed":
            raise ReservationException("Nie można rozpocząć wizyty.")
        self.status = "in_progress"
        print("Wizyta została rozpoczęta.")

    def complete(self):
        # Zakończenie wizyty. Dozwolone tylko jeśli status to "in_progress".
        if self.status != "in_progress":
            raise ReservationException("Nie można zakończyć wizyty.")
        self.status = "done"
        print("Wizyta została zakończona.")

    def cancel(self):
        # Anulowanie wizyty. Dozwolone tylko jeśli status to "new" lub "confirmed".
        if self.status not in ["new", "confirmed"]:
            raise ReservationException("Nie można anulować wizyty.")
        self.status = "cancelled"
        print("Rezerwacja została anulowana.")
