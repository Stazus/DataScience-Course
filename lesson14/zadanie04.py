# Lekcja 14 - Zadanie 4
# READ - Zapytania podstawowe

from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

from zadanie02 import Base, Student, engine, DATABASE_PATH


Session = sessionmaker(bind=engine)


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

    print(f"\nLiczba wynikow: {len(students)}")


def main():

    print("=" * 70)
    print("ZADANIE 4 - READ - ZAPYTANIA PODSTAWOWE")
    print("=" * 70)

    try:

        section("1. KONFIGURACJA BAZY DANYCH")

        print(f"Baza danych: {DATABASE_PATH}")
        print(f"Model: {Student.__name__}")
        print(f"Tabela: {Student.__tablename__}")

        Base.metadata.create_all(engine)

        with Session() as session:

            count_before = session.query(Student).count()

            # Zapytanie 1 - wszyscy studenci

            section("2. POBRANIE WSZYSTKICH STUDENTOW")

            print("Metoda: .all()")

            all_students = (
                session.query(Student)
                .order_by(Student.id)
                .all()
            )

            print_students(all_students)

            # Zapytanie 2 - student o konkretnym imieniu

            section("3. WYSZUKIWANIE STUDENTA PO IMIENIU")

            searched_name = "Maria"

            print(f"Szukane imie: {searched_name}")
            print("Metody: .filter() i .first()")

            found_student = (
                session.query(Student)
                .filter(Student.name == searched_name)
                .order_by(Student.id)
                .first()
            )

            if found_student is not None:

                print_students([found_student])

            else:

                print("Nie znaleziono studenta.")

            # Zapytanie 3 - studenci starsi niz 20 lat

            section("4. STUDENCI STARSI NIZ 20 LAT")

            print("Warunek: Student.age > 20")
            print("Metody: .filter() i .all()")

            older_students = (
                session.query(Student)
                .filter(Student.age > 20)
                .order_by(Student.age)
                .all()
            )

            print_students(older_students)

            # Zapytanie 4 - liczba studentow

            section("5. LICZENIE WSZYSTKICH STUDENTOW")

            print("Metoda: .count()")

            total_students = (
                session.query(Student)
                .count()
            )

            print(f"Liczba studentow: {total_students}")

            # Dodatkowe zapytanie - brak wyniku

            section("6. WYSZUKIWANIE NIEISTNIEJACEGO STUDENTA")

            missing_student = (
                session.query(Student)
                .filter(Student.name == "Nieistniejacy")
                .first()
            )

            print(f"Wynik: {missing_student}")

            # Dodatkowe statystyki

            section("7. STATYSTYKI WYNIKOW")

            older_count = len(older_students)

            percentage = (
                older_count / total_students * 100
                if total_students else 0
            )

            print(f"Wszyscy studenci: {total_students}")
            print(f"Studenci starsi niz 20 lat: {older_count}")
            print(f"Udzial procentowy: {percentage:.2f}%")

            # Sprawdzenie, czy READ nie zmienil danych

            count_after = session.query(Student).count()

            section("8. AUTOMATYCZNE TESTY")

            tests = {

                "Plik test.db istnieje":
                    DATABASE_PATH.is_file(),

                "Pobrano wszystkich 5 studentow":
                    len(all_students) == 5,

                "Wszystkie wyniki sa obiektami Student":
                    all(
                        isinstance(student, Student)
                        for student in all_students
                    ),

                "Identyfikatory studentow sa unikalne":
                    len({
                        student.id
                        for student in all_students
                    }) == 5,

                "Znaleziono studenta o imieniu Maria":
                    found_student is not None
                    and found_student.name == "Maria",

                "Maria ma 22 lata":
                    found_student is not None
                    and found_student.age == 22,

                "Adres email Marii jest poprawny":
                    found_student is not None
                    and found_student.email
                    == "maria@example.com",

                "Znaleziono 3 studentow starszych niz 20 lat":
                    len(older_students) == 3,

                "Wszyscy odfiltrowani studenci maja ponad 20 lat":
                    all(
                        student.age > 20
                        for student in older_students
                    ),

                "Student w wieku 20 lat nie zostal uwzgledniony":
                    all(
                        student.age != 20
                        for student in older_students
                    ),

                "Imiona odfiltrowanych studentow sa poprawne":
                    [student.name for student in older_students]
                    == ["Maria", "Tomasz", "Katarzyna"],

                "Wyniki sa posortowane wedlug wieku":
                    [student.age for student in older_students]
                    == sorted(
                        student.age
                        for student in older_students
                    ),

                "Metoda count zwrocila 5":
                    total_students == 5,

                "Wyniki all i count sa zgodne":
                    len(all_students) == total_students,

                "Nieistniejacy student zwraca None":
                    missing_student is None,

                "Studenci powyzej 20 lat stanowia 60 procent":
                    abs(percentage - 60.0) < 0.000001,

                "Liczba rekordow nie ulegla zmianie":
                    count_before == count_after == 5,

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

        section("9. PODSUMOWANIE")

        print("Model: Student")
        print("Tabela: students")
        print("Operacja CRUD: READ")
        print(f"Wszyscy studenci: {total_students}")
        print(f"Studenci starsi niz 20 lat: {older_count}")
        print(f"Udzial procentowy: {percentage:.2f}%")

        print("Wykorzystano metode .all().")
        print("Wykorzystano metode .filter().")
        print("Wykorzystano metode .first().")
        print("Wykorzystano metode .count().")

        print("Dane w bazie pozostaly niezmienione.")
        print("Wszystkie testy zakonczone pomyslnie.")
        print("Zadanie 4 wykonane poprawnie.")

    except SQLAlchemyError as error:

        print(f"Blad SQLAlchemy: {error}")
        raise

    finally:

        engine.dispose()


if __name__ == "__main__":
    main()
