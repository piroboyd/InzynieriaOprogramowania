from datetime import datetime


class Logger:
    _instance = None  # Jedyna instancja klasy Logger – implementacja wzorca Singleton

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
            cls._instance.log_file = "system-rezerwacji-log.log"  # Ustawienie pliku logu (wspólnego dla wszystkich)
        return cls._instance

    def log(self, message):
        """
        Zapisuje komunikat z timestampem do pliku oraz wypisuje go na konsolę.
        :param message: Tekst komunikatu do zapisania w logu.
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Aktualna data i godzina
        log_entry = f"[{timestamp}] {message}"  # Formatowanie wpisu logu z timestampem

        # Zapis komunikatu do pliku logu
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(log_entry + "\n")

        # Wypisanie komunikatu logu na konsolę (dla użytkownika/developera)
        print(f"[LOG] {log_entry}")
