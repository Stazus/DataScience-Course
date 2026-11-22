# Lekcja 09 - Zadanie 3: Klasa BankAccount


class BankAccount:
    def __init__(self, wlasciciel, saldo=0):
        self.wlasciciel = wlasciciel
        self.saldo = saldo

    def wplac(self, kwota):
        if kwota <= 0:
            print("Blad: kwota wplaty musi byc dodatnia.")
        else:
            self.saldo += kwota
            print(f"Wplacono {kwota:.2f} zl na konto {self.wlasciciel}")

    def wyplac(self, kwota):
        if kwota <= 0:
            print("Blad: kwota wyplaty musi byc dodatnia.")
        elif kwota > self.saldo:
            print(f"Brak wystarczajacych srodkow: {self.wlasciciel}")
        else:
            self.saldo -= kwota
            print(f"Wyplacono {kwota:.2f} zl z konta {self.wlasciciel}")

    def pokaz_saldo(self):
        print(f"Wlasciciel: {self.wlasciciel}")
        print(f"Saldo: {self.saldo:.2f} zl")


# Utworzenie trzech kont bankowych
konto1 = BankAccount("Jan Kowalski", 5000)
konto2 = BankAccount("Anna Nowak", 3000)
konto3 = BankAccount("Piotr Wisniewski", 1000)

konta = [konto1, konto2, konto3]

# Stan poczatkowy
print("STAN POCZATKOWY")
print("=" * 55)

for konto in konta:
    konto.pokaz_saldo()
    print("-" * 55)

# Wplaty
print("\nWPLATY")
print("=" * 55)

konto1.wplac(1500)
konto2.wplac(500)
konto3.wplac(2000)

# Wyplaty
print("\nWYPLATY")
print("=" * 55)

konto1.wyplac(2000)
konto2.wyplac(1000)
konto3.wyplac(500)

# Testy blednych operacji
print("\nTESTY BLEDNYCH OPERACJI")
print("=" * 55)

konto1.wyplac(10000)
konto2.wplac(-100)
konto3.wyplac(-50)

# Stan koncowy
print("\nSTAN KONCOWY")
print("=" * 55)

for konto in konta:
    konto.pokaz_saldo()
    print("-" * 55)

# Weryfikacja
print("\nWERYFIKACJA")
print("=" * 55)

oczekiwane_salda = [4500, 2500, 2500]

for konto, oczekiwane in zip(konta, oczekiwane_salda):
    print(
        f"{konto.wlasciciel}: "
        f"{konto.saldo == oczekiwane}"
    )

print(
    f"\nCzy wszystkie salda sa poprawne: "
    f"{all(konto.saldo == oczekiwane for konto, oczekiwane in zip(konta, oczekiwane_salda))}"
)
