# Lekcja 14 - Zadanie 6
# DELETE - Usuwanie studentow

from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

from zadanie02 import Base, Student, engine, DATABASE_PATH


Session = sessionmaker(bind=engine)


EXPECTED_BEFORE = {
    1: ("Anna", 23, "anna@example.com"),
    2: ("Piotr", 21, "piotr@example.com"),
    3: ("Maria", 23, "maria@example.com"),
    4: ("Tomasz", 25, "tomasz@example.com"),
    5: ("Katarzyna", 26, "katarzyna@example.com")
}


EXPECTED_AFTER = {
    1: ("Anna", 23, "anna@example.com"),
    3: ("Maria", 23, "maria@example.com")
}


def section(title):
    print(f"\n{title}")
    print("-" * 70)


def snapshot(students):

    return {
        student.id: (
            student.name,
            student.age,
            student.email
        )
        for student in students
    }


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
    print("ZADANIE 6 - DELETE - USUWANIE STUDENTOW")
    print("=" * 70)

    try:

        section("1. KONFIGURACJA BAZY DANYCH")

        print(f"Baza danych: {DATABASE_PATH}")
        print(f"Model: {Student.__name__}")
        print(f"Tabela: {Student.__tablename__}")

        Base.metadata.create_all(engine)

        with Session() as session:

            section("2. STAN BAZY PRZED USUWANIEM")

            students_before = (
                session.query(Student)
                .order_by(Student.id)
                .all()
            )

            print_students(students_before)

            data_before = snapshot(students_before)

            count_before = len(students_before)

            # Zabezpieczenie przed ponownym usuwaniem.

            if data_before == EXPECTED_AFTER:

                print("\nZadanie zostalo juz wykonane.")
                print("Nie usuwamy kolejnych studentow.")
                return

            if data_before != EXPECTED_BEFORE:

                raise ValueError(
                    "Stan bazy jest inny niz oczekiwany "
                    "po zadaniu 5. Przerwano usuwanie."
                )

            section("3. WYSZUKIWANIE NAJMLODSZEGO STUDENTA")

            youngest_student = (
                session.query(Student)
                .order_by(
                    Student.age.asc(),
                    Student.id.asc()
                )
                .first()
            )

            if youngest_student is None:

                raise ValueError(
                    "Nie znaleziono studentow."
                )

            youngest_id = youngest_student.id
            youngest_name = youngest_student.name
            youngest_age = youngest_student.age

            print(f"ID: {youngest_id}")
            print(f"Imie: {youngest_name}")
            print(f"Wiek: {youngest_age}")

            section("4. USUWANIE POJEDYNCZEGO STUDENTA")

            print("Metoda: session.delete()")

            session.delete(youngest_student)

            pending_deleted = len(session.deleted)

            print(
                f"Obiekty oznaczone do usuniecia: "
                f"{pending_deleted}"
            )

            session.flush()

            print("session.flush() wykonany poprawnie.")
            print(f"Usunieto studenta: {youngest_name}")

            section("5. STAN PO PIERWSZYM USUNIECIU")

            students_intermediate = (
                session.query(Student)
                .order_by(Student.id)
                .all()
            )

            print_students(students_intermediate)

            data_intermediate = snapshot(
                students_intermediate
            )

            count_intermediate = len(
                students_intermediate
            )

            section("6. STUDENCI STARSI NIZ 24 LATA")

            older_students = (
                session.query(Student)
                .filter(Student.age > 24)
                .order_by(Student.id)
                .all()
            )

            print_students(older_students)

            older_ids = {
                student.id
                for student in older_students
            }

            older_names = [
                student.name
                for student in older_students
            ]

            section("7. BULK DELETE")

            print("Warunek: Student.age > 24")
            print("Metoda: query.delete()")

            deleted_count = (
                session.query(Student)
                .filter(Student.age > 24)
                .delete(
                    synchronize_session="fetch"
                )
            )

            print(
                f"Liczba usunietych rekordow: "
                f"{deleted_count}"
            )

            section("8. WERYFIKACJA PRZED COMMIT")

            students_pending = (
                session.query(Student)
                .order_by(Student.id)
                .all()
            )

            data_pending = snapshot(students_pending)

            print_students(students_pending)

            # Sprawdzenie wyniku przed trwalym zapisem.

            assert youngest_id == 2
            assert pending_deleted == 1
            assert count_intermediate == 4
            assert deleted_count == 2
            assert data_pending == EXPECTED_AFTER

            section("9. COMMIT TRANSAKCJI")

            session.commit()

            print("session.commit() wykonany poprawnie.")

        section("10. WERYFIKACJA W NOWEJ SESJI")

        with Session() as session:

            students_after = (
                session.query(Student)
                .order_by(Student.id)
                .all()
            )

            print_students(students_after)

            data_after = snapshot(students_after)

            count_after = (
                session.query(Student)
                .count()
            )

            removed_ids = (
                set(data_before) - set(data_after)
            )

            removed_names = [
                data_before[student_id][0]
                for student_id in sorted(removed_ids)
            ]

            total_deleted = (
                count_before - count_after
            )

            reduction = (
                total_deleted / count_before * 100
            )

            section("11. RAPORT USUNIETYCH STUDENTOW")

            print(
                f"{'ID':<5}"
                f"{'IMIE':<15}"
                f"{'WIEK':<8}"
                f"{'OPERACJA':<25}"
            )

            print("-" * 70)

            for student_id in sorted(removed_ids):

                name, age, email = data_before[
                    student_id
                ]

                operation = (
                    "DELETE"
                    if student_id == youngest_id
                    else "BULK DELETE"
                )

                print(
                    f"{student_id:<5}"
                    f"{name:<15}"
                    f"{age:<8}"
                    f"{operation:<25}"
                )

            section("12. STATYSTYKI")

            print(
                f"Liczba studentow przed: "
                f"{count_before}"
            )

            print(
                f"Po pojedynczym DELETE: "
                f"{count_intermediate}"
            )

            print(
                f"Po Bulk Delete: "
                f"{count_after}"
            )

            print(
                f"Lacznie usunieto: "
                f"{total_deleted}"
            )

            print(
                f"Redukcja liczby rekordow: "
                f"{reduction:.2f}%"
            )

            print(
                f"Pozostalo studentow: "
                f"{count_after}"
            )

            section("13. AUTOMATYCZNE TESTY")

            tests = {

                "Plik test.db istnieje":
                    DATABASE_PATH.is_file(),

                "Przed usuwaniem bylo 5 studentow":
                    count_before == 5,

                "Najmlodszy student to Piotr":
                    youngest_name == "Piotr",

                "Najmlodszy student ma 21 lat":
                    youngest_age == 21,

                "Poprawne ID najmlodszego studenta":
                    youngest_id == 2,

                "Oznaczono jeden obiekt do usuniecia":
                    pending_deleted == 1,

                "Po pierwszym DELETE pozostalo 4 studentow":
                    count_intermediate == 4,

                "Piotr zostal usuniety":
                    youngest_id not in data_intermediate,

                "Pozostali studenci po DELETE bez zmian":
                    data_intermediate == {
                        student_id: data
                        for student_id, data
                        in data_before.items()
                        if student_id != youngest_id
                    },

                "Znaleziono 2 studentow starszych niz 24 lata":
                    len(older_ids) == 2,

                "Poprawne imiona starszych studentow":
                    older_names == [
                        "Tomasz",
                        "Katarzyna"
                    ],

                "Bulk Delete usunal 2 rekordy":
                    deleted_count == 2,

                "Tomasz zostal usuniety":
                    4 not in data_after,

                "Katarzyna zostala usunieta":
                    5 not in data_after,

                "Nie pozostali studenci starsi niz 24 lata":
                    all(
                        student.age <= 24
                        for student in students_after
                    ),

                "Pozostalo 2 studentow":
                    count_after == 2,

                "Anna pozostala w bazie":
                    1 in data_after,

                "Maria pozostala w bazie":
                    3 in data_after,

                "Pozostali studenci maja 23 lata":
                    all(
                        student.age == 23
                        for student in students_after
                    ),

                "Identyfikatory pozostaly niezmienione":
                    set(data_after) == {1, 3},

                "Dane pozostalych studentow bez zmian":
                    all(
                        data == data_before[student_id]
                        for student_id, data
                        in data_after.items()
                    ),

                "Usunieto wlasciwe identyfikatory":
                    removed_ids == {2, 4, 5},

                "Usunieto wlasciwych studentow":
                    removed_names == [
                        "Piotr",
                        "Tomasz",
                        "Katarzyna"
                    ],

                "Lacznie usunieto 3 rekordy":
                    total_deleted == 3,

                "Redukcja liczby rekordow wynosi 60 procent":
                    abs(reduction - 60.0) < 0.000001,

                "Wynik jest zgodny z oczekiwanym":
                    data_after == EXPECTED_AFTER,

                "Wynik po commit zgodny z wynikiem przed commit":
                    data_after == data_pending,

                "Dane sa dostepne w nowej sesji":
                    len(students_after) == 2,

                "Brak nowych obiektow w sesji":
                    len(session.new) == 0,

                "Brak zmodyfikowanych obiektow w sesji":
                    len(session.dirty) == 0,

                "Brak obiektow oczekujacych na usuniecie":
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

        section("14. PODSUMOWANIE")

        print("Model: Student")
        print("Tabela: students")
        print("Operacja CRUD: DELETE")

        print(
            f"Najmlodszy usuniety student: "
            f"{youngest_name}"
        )

        print(f"Bulk Delete: {deleted_count} rekordy")
        print(f"Lacznie usunieto: {total_deleted}")
        print(f"Pozostalo studentow: {count_after}")
        print(f"Redukcja: {reduction:.2f}%")

        print("Wykorzystano order_by().")
        print("Wykorzystano first().")
        print("Wykorzystano session.delete().")
        print("Wykorzystano query.delete().")
        print("Wykonano session.commit().")
        print("Zweryfikowano dane w nowej sesji.")
        print("Wszystkie testy zakonczone pomyslnie.")
        print("Zadanie 6 wykonane poprawnie.")

    except SQLAlchemyError as error:

        print(f"Blad SQLAlchemy: {error}")
        raise

    finally:

        engine.dispose()


if __name__ == "__main__":
    main()
