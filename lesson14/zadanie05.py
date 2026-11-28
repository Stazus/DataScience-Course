# Lekcja 14 - Zadanie 5
# UPDATE - Aktualizacja danych

from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

from zadanie02 import Base, Student, engine, DATABASE_PATH


Session = sessionmaker(bind=engine)


EXPECTED_BEFORE = {
    "Anna": 18,
    "Piotr": 20,
    "Maria": 22,
    "Tomasz": 24,
    "Katarzyna": 25
}


EXPECTED_AFTER = {
    "Anna": 23,
    "Piotr": 21,
    "Maria": 23,
    "Tomasz": 25,
    "Katarzyna": 26
}


def section(title):
    print(f"\n{title}")
    print("-" * 70)


def print_students(students):

    print(
        f"{'ID':<5}"
        f"{'IMIE':<15}"
        f"{'WIEK':<8}"
        f"{'EMAIL':<30}"
    )

    print("-" * 70)

    for student in students:

        print(
            f"{student.id:<5}"
            f"{student.name:<15}"
            f"{student.age:<8}"
            f"{student.email:<30}"
        )

    print(f"\nLiczba studentow: {len(students)}")


def main():

    print("=" * 70)
    print("ZADANIE 5 - UPDATE - AKTUALIZACJA DANYCH")
    print("=" * 70)

    try:

        section("1. KONFIGURACJA BAZY DANYCH")

        print(f"Baza danych: {DATABASE_PATH}")
        print(f"Model: {Student.__name__}")
        print(f"Tabela: {Student.__tablename__}")

        Base.metadata.create_all(engine)

        with Session() as session:

            section("2. STAN BAZY PRZED AKTUALIZACJA")

            students_before = (
                session.query(Student)
                .order_by(Student.id)
                .all()
            )

            print_students(students_before)

            ages_before = {
                student.name: student.age
                for student in students_before
            }

            identities_before = {
                (student.id, student.name, student.email)
                for student in students_before
            }

            count_before = len(students_before)

            # Zabezpieczenie przed ponownym
            # zwiekszeniem wieku studentow.

            if ages_before == EXPECTED_AFTER and count_before == 5:

                print("\nZadanie zostalo juz wykonane.")
                print("Nie wykonujemy ponownej aktualizacji.")
                return

            if ages_before != EXPECTED_BEFORE or count_before != 5:

                raise ValueError(
                    "Stan bazy jest inny niz oczekiwany "
                    "po zadaniu 3."
                )

            average_before = (
                sum(ages_before.values()) / count_before
            )

            section("3. POBRANIE POJEDYNCZEGO STUDENTA")

            student = (
                session.query(Student)
                .filter(Student.email == "anna@example.com")
                .first()
            )

            if student is None:

                raise ValueError(
                    "Nie znaleziono studentki Anna."
                )

            print(f"Znaleziony student: {student}")

            old_age = student.age

            print(f"Wiek przed zmiana: {old_age}")

            section("4. AKTUALIZACJA POJEDYNCZEGO OBIEKTU")

            student.age = 22

            print(f"Wiek po zmianie: {student.age}")

            print(
                f"Obiekty zmodyfikowane w sesji: "
                f"{len(session.dirty)}"
            )

            # Wyslanie zmiany do bazy bez zatwierdzania
            # calej transakcji.

            session.flush()

            intermediate_age = student.age

            print("session.flush() wykonany poprawnie.")

            section("5. STAN PO PIERWSZEJ AKTUALIZACJI")

            students_intermediate = (
                session.query(Student)
                .order_by(Student.id)
                .all()
            )

            print_students(students_intermediate)

            ages_intermediate = {
                item.name: item.age
                for item in students_intermediate
            }

            average_intermediate = (
                sum(ages_intermediate.values()) / count_before
            )

            section("6. BULK UPDATE - WSZYSCY STUDENCI")

            print("Zwiekszamy wiek wszystkich studentow o 1 rok.")

            updated_count = (
                session.query(Student)
                .update(
                    {Student.age: Student.age + 1},
                    synchronize_session="fetch"
                )
            )

            print(
                f"Liczba zaktualizowanych rekordow: "
                f"{updated_count}"
            )

            section("7. COMMIT TRANSAKCJI")

            session.commit()

            print("session.commit() wykonany poprawnie.")

        section("8. WERYFIKACJA W NOWEJ SESJI")

        with Session() as session:

            students_after = (
                session.query(Student)
                .order_by(Student.id)
                .all()
            )

            print_students(students_after)

            ages_after = {
                student.name: student.age
                for student in students_after
            }

            identities_after = {
                (student.id, student.name, student.email)
                for student in students_after
            }

            count_after = len(students_after)

            average_after = (
                sum(ages_after.values()) / count_after
            )

            section("9. POROWNANIE WIEKU STUDENTOW")

            print(
                f"{'IMIE':<15}"
                f"{'PRZED':<10}"
                f"{'ETAP 1':<10}"
                f"{'PO':<10}"
                f"{'ZMIANA':<10}"
            )

            print("-" * 70)

            for name in ages_before:

                difference = (
                    ages_after[name] - ages_before[name]
                )

                print(
                    f"{name:<15}"
                    f"{ages_before[name]:<10}"
                    f"{ages_intermediate[name]:<10}"
                    f"{ages_after[name]:<10}"
                    f"{difference:+d}"
                )

            section("10. STATYSTYKI")

            print(
                f"Sredni wiek przed aktualizacja: "
                f"{average_before:.2f}"
            )

            print(
                f"Sredni wiek po pierwszej zmianie: "
                f"{average_intermediate:.2f}"
            )

            print(
                f"Sredni wiek po Bulk Update: "
                f"{average_after:.2f}"
            )

            print(
                f"Zmiana sredniego wieku: "
                f"{average_after - average_before:.2f}"
            )

            print(
                f"Liczba studentow przed: "
                f"{count_before}"
            )

            print(
                f"Liczba studentow po: "
                f"{count_after}"
            )

            section("11. AUTOMATYCZNE TESTY")

            tests = {

                "Plik test.db istnieje":
                    DATABASE_PATH.is_file(),

                "Przed aktualizacja bylo 5 studentow":
                    count_before == 5,

                "Anna poczatkowo miala 18 lat":
                    old_age == 18,

                "Wiek Anny zmieniono na 22 lata":
                    intermediate_age == 22,

                "Pierwsza aktualizacja zmienila wiek Anny":
                    ages_intermediate["Anna"] == 22,

                "Pierwsza aktualizacja nie zmienila innych":
                    all(
                        ages_intermediate[name] == age
                        for name, age in ages_before.items()
                        if name != "Anna"
                    ),

                "Bulk Update objal 5 rekordow":
                    updated_count == 5,

                "Wiek wszystkich zwiekszono o 1 rok":
                    all(
                        ages_after[name] == age + 1
                        for name, age in ages_intermediate.items()
                    ),

                "Anna ma 23 lata":
                    ages_after.get("Anna") == 23,

                "Piotr ma 21 lat":
                    ages_after.get("Piotr") == 21,

                "Maria ma 23 lata":
                    ages_after.get("Maria") == 23,

                "Tomasz ma 25 lat":
                    ages_after.get("Tomasz") == 25,

                "Katarzyna ma 26 lat":
                    ages_after.get("Katarzyna") == 26,

                "Wszystkie wartosci wieku sa poprawne":
                    ages_after == EXPECTED_AFTER,

                "Liczba studentow pozostala niezmieniona":
                    count_before == count_after == 5,

                "Identyfikatory imiona i emaile bez zmian":
                    identities_before == identities_after,

                "Sredni wiek przed wynosil 21.8":
                    abs(average_before - 21.8) < 0.000001,

                "Sredni wiek po pierwszej zmianie wynosi 22.6":
                    abs(average_intermediate - 22.6) < 0.000001,

                "Sredni wiek po Bulk Update wynosi 23.6":
                    abs(average_after - 23.6) < 0.000001,

                "Zmiana sredniego wieku wynosi 1.8":
                    abs(
                        average_after - average_before - 1.8
                    ) < 0.000001,

                "Dane sa dostepne w nowej sesji":
                    len(students_after) == 5,

                "Brak nowych obiektow w sesji":
                    len(session.new) == 0,

                "Brak zmodyfikowanych obiektow w sesji":
                    len(session.dirty) == 0,

                "Brak usunietych obiektow w sesji":
                    len(session.deleted) == 0
            }

            for name, passed in tests.items():
                print(f"Czy {name}: {passed}")

            passed_count = sum(tests.values())

            print(
                f"\nZaliczone testy: "
                f"{passed_count}/{len(tests)}"
            )

            assert all(tests.values()), (
                "Nie wszystkie testy zaliczone."
            )

        section("12. PODSUMOWANIE")

        print("Model: Student")
        print("Tabela: students")
        print("Operacja CRUD: UPDATE")
        print(f"Wiek Anny przed: {old_age}")
        print(f"Wiek Anny po pierwszej zmianie: {intermediate_age}")
        print(f"Wiek Anny po Bulk Update: {ages_after['Anna']}")
        print(f"Bulk Update: {updated_count} rekordow")
        print(f"Liczba studentow: {count_after}")
        print(f"Sredni wiek: {average_after:.2f}")

        print("Wykorzystano modyfikacje obiektu ORM.")
        print("Wykorzystano query.update().")
        print("Wykonano session.commit().")
        print("Zweryfikowano dane w nowej sesji.")
        print("Wszystkie testy zakonczone pomyslnie.")
        print("Zadanie 5 wykonane poprawnie.")

    except SQLAlchemyError as error:

        print(f"Blad SQLAlchemy: {error}")
        raise

    finally:

        engine.dispose()


if __name__ == "__main__":
    main()
