class User:
    """
    Klasa bazowa reprezentująca użytkownika systemu.
    """
    def __init__(self, user_id, first_name, last_name, email):
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email

    def login(self):
        """
        Symuluje logowanie użytkownika.
        """
        print(f"{self.first_name} {self.last_name} zalogował(a) się do systemu.")

    def register(self):
        """
        Symuluje rejestrację użytkownika.
        """
        print(f"Rejestrowanie użytkownika: {self.email}")


class Patient(User):
    """
    Klasa reprezentująca pacjenta. Dziedziczy po klasie User.
    """
    def make_appointment(self, doctor_name, date):
        """
        Tworzy wizytę u wybranego lekarza w danym dniu.
        """
        print(f"Pacjent {self.first_name} umawia wizytę u dr {doctor_name} na {date}.")


class Doctor(User):
    """
    Klasa reprezentująca lekarza. Dziedziczy po klasie User.
    """
    def manage_appointments(self):
        """
        Symuluje zarządzanie wizytami przez lekarza.
        """
        print(f"Lekarz {self.first_name} zarządza wizytami.")


class Admin(User):
    """
    Klasa reprezentująca administratora systemu. Dziedziczy po klasie User.
    """
    def cancel_appointment(self, appointment_id):
        """
        Anuluje wizytę o podanym ID.
        """
        print(f"Administrator anuluje wizytę o ID {appointment_id}.")
