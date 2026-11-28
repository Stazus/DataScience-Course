# Lekcja 14 - Zadanie 3
# CREATE - Dodawanie studentow

from sqlalchemy import select, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

from zadanie02 import Base, Student, engine, DATABASE_PATH


Session = sessionmaker(bind=engine)


STUDENTS_DATA = [
    ("Anna", 18, "anna@example.com"),
    ("Piotr", 20, "piotr@example.com"),
    ("Maria", 22, "maria@example.com"),
    ("Tomasz", 24, "tomasz@example.com"),
    ("Katarzyna", 25, "katarzyna@example.com")
]


def section(title):
    print(f"\n{title}")
    print("-" * 70)


def main():

    print("=" * 70)
    print("ZADANIE 3 - CREATE - DODAWANIE STUDENTOW")
    print("=" * 70)

    try:

        section("1. KONFIGURACJA BAZY DANYCH")

        print(f"Baza danych: {DATABASE_PATH}")
        print(f"Model: {Student.__name__}")
        print(f"Tabela: {Student.__tablename__}")

        Base.metadata.create_all(engine)

        section("2. UTWORZENIE SESJI")

        print("Session = sessionmaker(bind=engine)")

        section("3. UTWORZENIE 5 OBIEKTOW STUDENT")

        students = [
            Student(
                name=name,
                age=age,
                email=email
            )
            for name, age, email in STUDENTS_DATA
        ]

        for student in students:
            print(student)

        print(f"\nUtworzono obiektow: {len(students)}")

        expected_emails = [
            email
            for _, _, email in STUDENTS_DATA
        ]

        section("4. STAN BAZY PRZED DODANIEM")

        with Session() as session:

            count_before = session.scalar(
                select(func.count()).select_from(Student)
            )

            print(f"Liczba studentow: {count_before}")

            existing_emails = set(
                session.scalars(
                    select(Student.email).where(
                        Student.email.in_(expected_emails)
                    )
                ).all()
            )

            section("5. DODAWANIE STUDENTOW - ADD_ALL")

            # Zabezpieczenie przed duplikatami
            # przy ponownym uruchomieniu skryptu.

            new_students = [
                student
                for student in students
                if student.email not in existing_emails
            ]

            session.add_all(new_students)

            print(
                f"Nowe obiekty w sesji: "
                f"{len(session.new)}"
            )

            print(
                f"Pominiete istniejace rekordy: "
                f"{len(students) - len(new_students)}"
            )

            section("6. COMMIT TRANSAKCJI")

            session.commit()

            print("session.commit() wykonany poprawnie.")
            print(f"Dodano rekordow: {len(new_students)}")

        section("7. WERYFIKACJA W NOWEJ SESJI")

        # Nowa sesja potwierdza trwaly zapis danych.

        with Session() as session:

            saved_students = session.scalars(
                select(Student)
                .where(Student.email.in_(expected_emails))
                .order_by(Student.id)
            ).all()

            count_after = session.scalar(
                select(func.count()).select_from(Student)
            )

            print(f"Liczba studentow przed: {count_before}")
            print(f"Liczba studentow po: {count_after}")
            print(f"Znaleziono studentow: {len(saved_students)}")

            section("8. ZAPISANE REKORDY")

            print(
                f"{'ID':<5}"
                f"{'IMIE':<15}"
                f"{'WIEK':<8}"
                f"{'EMAIL':<30}"
            )

            print("-" * 70)

            for student in saved_students:

                print(
                    f"{student.id:<5}"
                    f"{student.name:<15}"
                    f"{student.age:<8}"
                    f"{student.email:<30}"
                )

            section("9. STATYSTYKI STUDENTOW")

            ages = [
                student.age
                for student in saved_students
            ]

            print(f"Liczba studentow: {len(saved_students)}")
            print(f"Najmlodszy student: {min(ages)} lat")
            print(f"Najstarszy student: {max(ages)} lat")
            print(f"Sredni wiek: {sum(ages) / len(ages):.2f}")

            section("10. AUTOMATYCZNE TESTY")

            actual_data = {
                (student.name, student.age, student.email)
                for student in saved_students
            }

            expected_data = set(STUDENTS_DATA)

            tests = {
                "Plik test.db istnieje":
                    DATABASE_PATH.is_file(),

                "Utworzono 5 obiektow Student":
                    len(students) == 5,

                "Wszystkie obiekty sa typu Student":
                    all(
                        isinstance(student, Student)
                        for student in students
                    ),

                "Odczytano 5 zapisanych studentow":
                    len(saved_students) == 5,

                "Wszyscy studenci maja ID":
                    all(
                        student.id is not None
                        for student in saved_students
                    ),

                "Identyfikatory sa unikalne":
                    len({
                        student.id
                        for student in saved_students
                    }) == 5,

                "Wszyscy studenci maja imiona":
                    all(
                        bool(student.name)
                        for student in saved_students
                    ),

                "Wiek studentow wynosi od 18 do 25 lat":
                    all(
                        18 <= student.age <= 25
                        for student in saved_students
                    ),

                "Adresy email sa unikalne":
                    len({
                        student.email
                        for student in saved_students
                    }) == 5,

                "Adresy email maja domene example.com":
                    all(
                        student.email.endswith("@example.com")
                        for student in saved_students
                    ),

                "Format adresow email jest poprawny":
                    all(
                        student.email
                        == f"{student.name.lower()}@example.com"
                        for student in saved_students
                    ),

                "Dane zapisane sa zgodne z oczekiwanymi":
                    actual_data == expected_data,

                "Liczba dodanych rekordow jest poprawna":
                    count_after - count_before
                    == len(new_students),

                "Dane sa dostepne w nowej sesji":
                    len(saved_students) == len(STUDENTS_DATA)
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

        section("11. PODSUMOWANIE")

        print("Model: Student")
        print("Tabela: students")
        print("Operacja CRUD: CREATE")
        print(f"Utworzono obiektow: {len(students)}")
        print(f"Dodano nowych rekordow: {len(new_students)}")
        print(f"Liczba rekordow w tabeli: {count_after}")
        print("Wykorzystano session.add_all().")
        print("Wykonano session.commit().")
        print("Zweryfikowano dane w nowej sesji.")
        print("Wszystkie testy zakonczone pomyslnie.")
        print("Zadanie 3 wykonane poprawnie.")

    except SQLAlchemyError as error:

        print(f"Blad SQLAlchemy: {error}")
        raise

    finally:

        engine.dispose()


if __name__ == "__main__":
    main()
