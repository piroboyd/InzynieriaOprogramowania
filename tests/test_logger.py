import os
import tempfile
from services.logger import Logger


"""
Testy jednostkowe dla klasy Logger (implementującej wzorzec Singleton).

Testowane scenariusze:

1. test_singleton_instance:
   Sprawdza, czy Logger działa jako singleton – tzn. dwie utworzone instancje
   wskazują na ten sam obiekt w pamięci.

2. test_logger_logfile_written:
   Weryfikuje, czy metoda log() poprawnie zapisuje komunikat do pliku logów.
   Tworzony jest tymczasowy plik, do którego zapisuje się testowy komunikat,
   a następnie zawartość pliku jest sprawdzana.
"""


def test_singleton_instance():
    logger1 = Logger()
    logger2 = Logger()
    assert logger1 is logger2


def test_logger_logfile_written():
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        log_path = temp_file.name
    logger = Logger()
    logger.log_file = log_path
    logger.log("Test message")
    with open(log_path, "r") as f:
        content = f.read()
    assert "Test message" in content
    os.remove(log_path)
