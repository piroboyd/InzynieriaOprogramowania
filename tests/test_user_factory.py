import pytest
from factories.user_factory import UserFactory, Admin, Doctor, Patient

"""
Testy jednostkowe dla klasy UserFactory, odpowiedzialnej za tworzenie użytkowników różnych typów.

Testowane scenariusze:

1. test_create_admin:
   Sprawdza, czy fabryka tworzy poprawnie obiekt klasy Admin dla typu "admin".

2. test_create_doctor:
   Sprawdza, czy fabryka tworzy poprawnie obiekt klasy Doctor dla typu "doctor".

3. test_create_patient:
   Sprawdza, czy fabryka tworzy poprawnie obiekt klasy Patient dla typu "patient".

4. test_create_invalid_user_type:
   Weryfikuje, że próba utworzenia użytkownika o nieznanym typie skutkuje wyrzuceniem wyjątku ValueError.
"""


def test_create_admin():
    user = UserFactory.create_user("admin", 1, "Alicja", "Nowak", "admin@example.com")
    assert isinstance(user, Admin)


def test_create_doctor():
    user = UserFactory.create_user("doctor", 2, "Jan", "Kowalski", "doc@example.com")
    assert isinstance(user, Doctor)


def test_create_patient():
    user = UserFactory.create_user("patient", 3, "Anna", "Zielińska", "anna@example.com")
    assert isinstance(user, Patient)


def test_create_invalid_user_type():
    with pytest.raises(ValueError):
        UserFactory.create_user("unknown", 4, "Imie", "Nazw", "x@x.pl")
