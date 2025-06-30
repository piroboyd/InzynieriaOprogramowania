from models.user import Patient, Doctor, Admin


class UserFactory:
    """
    Wzorzec projektowy: Factory Method

    Klasa `UserFactory` odpowiada za tworzenie obiektów użytkowników na podstawie podanego typu.
    Dzięki temu kod klienta nie musi znać szczegółów implementacji klas `Patient`, `Doctor`, `Admin`.
    """

    @staticmethod
    def create_user(user_type, user_id, first_name, last_name, email):
        """
        Tworzy instancję odpowiedniego typu użytkownika.

        Parametry:
        - user_type (str): Typ użytkownika, np. 'patient', 'doctor', 'admin'
        - user_id (int): ID użytkownika
        - first_name (str): Imię
        - last_name (str): Nazwisko
        - email (str): Adres e-mail

        Zwraca:
        - Obiekt jednej z klas dziedziczących po User: Patient, Doctor lub Admin

        Podnosi:
        - ValueError: Jeśli podano nieznany typ użytkownika
        """

        if user_type == "patient":
            # Tworzy obiekt klasy Patient
            return Patient(user_id, first_name, last_name, email)
        elif user_type == "doctor":
            # Tworzy obiekt klasy Doctor
            return Doctor(user_id, first_name, last_name, email)
        elif user_type == "admin":
            # Tworzy obiekt klasy Admin
            return Admin(user_id, first_name, last_name, email)
        else:
            # Obsługa nieznanego typu – rzucenie wyjątku
            raise ValueError("Unknown user type")
