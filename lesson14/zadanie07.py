# Lekcja 14 - Zadanie 7
# Relacja One-to-Many

from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    inspect
)

from sqlalchemy.orm import (
    relationship,
    sessionmaker
)

from sqlalchemy.exc import SQLAlchemyError

from zadanie02 import (
    Base,
    Student,
    engine,
    DATABASE_PATH
)


Session = sessionmaker(bind=engine)


# MODEL TEACHER

class Teacher(Base):

    __tablename__ = "teachers"

    id = Column(Integer, primary_key=True)

    name = Column(String(100), nullable=False)

    courses = relationship(
        "Course",
        back_populates="teacher"
    )

    def __repr__(self):

        return (
            f"Teacher(id={self.id}, "
            f"name='{self.name}')"
        )


# MODEL COURSE

class Course(Base):

    __tablename__ = "courses"

    id = Column(Integer, primary_key=True)

    title = Column(String(150), nullable=False)

    teacher_id = Column(
        Integer,
        ForeignKey("teachers.id"),
        nullable=False
    )

    teacher = relationship(
        "Teacher",
        back_populates="courses"
    )

    def __repr__(self):

        return (
            f"Course(id={self.id}, "
            f"title='{self.title}', "
            f"teacher_id={self.teacher_id})"
        )


TEACHER_NAME = "Jan Kowalski"

COURSE_TITLES = [
    "Python",
    "SQL",
    "Data Science"
]


def section(title):

    print(f"\n{title}")
    print("-" * 70)


def main():

    print("=" * 70)
    print("ZADANIE 7 - RELACJA ONE-TO-MANY")
    print("=" * 70)

    try:

        section("1. KONFIGURACJA BAZY DANYCH")

        print(f"Baza danych: {DATABASE_PATH}")
        print(f"Dialekt: {engine.dialect.name}")

        section("2. DEFINICJA MODELI")

        print(f"Model: {Teacher.__name__}")
        print(f"Tabela: {Teacher.__tablename__}")

        for column in Teacher.__table__.columns:

            print(
                f"Kolumna: {column.name}, "
                f"Typ: {column.type}, "
                f"PK: {column.primary_key}"
            )

        print(f"\nModel: {Course.__name__}")
        print(f"Tabela: {Course.__tablename__}")

        for column in Course.__table__.columns:

            print(
                f"Kolumna: {column.name}, "
                f"Typ: {column.type}, "
                f"PK: {column.primary_key}"
            )

        section("3. TWORZENIE TABEL")

        Base.metadata.create_all(engine)

        inspector = inspect(engine)

        tables = inspector.get_table_names()

        print(f"Tabele w bazie: {tables}")

        section("4. SPRAWDZENIE KLUCZA OBCEGO")

        foreign_keys = inspector.get_foreign_keys(
            "courses"
        )

        for foreign_key in foreign_keys:

            print(foreign_key)

        valid_foreign_key = any(
            fk["constrained_columns"] == ["teacher_id"]
            and fk["referred_table"] == "teachers"
            and fk["referred_columns"] == ["id"]
            for fk in foreign_keys
        )

        section("5. SPRAWDZENIE RELACJI ORM")

        teacher_relation = inspect(
            Teacher
        ).relationships["courses"]

        course_relation = inspect(
            Course
        ).relationships["teacher"]

        print(
            "Teacher.courses: "
            f"{teacher_relation.direction.name}"
        )

        print(
            "Course.teacher: "
            f"{course_relation.direction.name}"
        )

        print(
            f"Teacher.courses uselist: "
            f"{teacher_relation.uselist}"
        )

        print(
            f"Course.teacher uselist: "
            f"{course_relation.uselist}"
        )

        with Session() as session:

            section("6. STAN BAZY PRZED DODANIEM")

            teachers_before = (
                session.query(Teacher).count()
            )

            courses_before = (
                session.query(Course).count()
            )

            students_before = [
                (s.id, s.name, s.age, s.email)
                for s in session.query(Student)
                .order_by(Student.id).all()
            ]

            print(f"Nauczyciele: {teachers_before}")
            print(f"Kursy: {courses_before}")
            print(f"Studenci: {len(students_before)}")

            section("7. UTWORZENIE NAUCZYCIELA")

            teacher = (
                session.query(Teacher)
                .filter(Teacher.name == TEACHER_NAME)
                .first()
            )

            teacher_created = teacher is None

            if teacher_created:

                teacher = Teacher(
                    name=TEACHER_NAME
                )

                session.add(teacher)

                print("Utworzono nowego nauczyciela.")

            else:

                print("Nauczyciel juz istnieje.")

            print(teacher)

            section("8. UTWORZENIE TRZECH KURSOW")

            existing_titles = {
                course.title
                for course in teacher.courses
            }

            added_courses = 0

            for title in COURSE_TITLES:

                if title in existing_titles:

                    print(f"Kurs juz istnieje: {title}")

                    continue

                course = Course(title=title)

                teacher.courses.append(course)

                added_courses += 1

                print(f"Przypisano kurs: {title}")

            print(
                f"\nLiczba nowych kursow: "
                f"{added_courses}"
            )

            print(
                f"Kursy nauczyciela: "
                f"{len(teacher.courses)}"
            )

            section("9. FLUSH I WERYFIKACJA")

            session.flush()

            teacher_id = teacher.id

            print(f"ID nauczyciela: {teacher_id}")

            for course in teacher.courses:

                print(course)

            assert len(teacher.courses) == 3

            assert {
                course.title
                for course in teacher.courses
            } == set(COURSE_TITLES)

            assert all(
                course.teacher_id == teacher_id
                for course in teacher.courses
            )

            section("10. COMMIT TRANSAKCJI")

            session.commit()

            print("session.commit() wykonany poprawnie.")

        section("11. WERYFIKACJA W NOWEJ SESJI")

        with Session() as session:

            saved_teacher = session.get(
                Teacher,
                teacher_id
            )

            assert saved_teacher is not None

            saved_courses = saved_teacher.courses

            print(f"Nauczyciel: {saved_teacher.name}")
            print(f"ID: {saved_teacher.id}")
            print(f"Liczba kursow: {len(saved_courses)}")

            print("\nNAUCZYCIEL -> KURSY")

            print(saved_teacher.name)

            for course in sorted(
                saved_courses,
                key=lambda item: item.id
            ):

                print(
                    f"  -> {course.title} "
                    f"(ID: {course.id}, "
                    f"teacher_id: {course.teacher_id})"
                )

            section("12. RELACJA ODWROTNA")

            for course in saved_courses:

                print(
                    f"{course.title} -> "
                    f"{course.teacher.name}"
                )

            section("13. STATYSTYKI")

            teachers_after = (
                session.query(Teacher).count()
            )

            courses_after = (
                session.query(Course).count()
            )

            students_after = [
                (s.id, s.name, s.age, s.email)
                for s in session.query(Student)
                .order_by(Student.id).all()
            ]

            print(
                f"Nauczyciele przed: "
                f"{teachers_before}"
            )

            print(
                f"Nauczyciele po: "
                f"{teachers_after}"
            )

            print(
                f"Kursy przed: "
                f"{courses_before}"
            )

            print(
                f"Kursy po: "
                f"{courses_after}"
            )

            print(
                f"Liczba kursow nauczyciela: "
                f"{len(saved_courses)}"
            )

            print(
                f"Liczba studentow: "
                f"{len(students_after)}"
            )

            section("14. AUTOMATYCZNE TESTY")

            tests = {

                "Plik test.db istnieje":
                    DATABASE_PATH.is_file(),

                "Model Teacher dziedziczy po Base":
                    issubclass(Teacher, Base),

                "Model Course dziedziczy po Base":
                    issubclass(Course, Base),

                "Tabela teachers istnieje":
                    "teachers" in tables,

                "Tabela courses istnieje":
                    "courses" in tables,

                "Tabela students nadal istnieje":
                    "students" in tables,

                "Teacher zawiera 2 kolumny":
                    len(inspector.get_columns(
                        "teachers"
                    )) == 2,

                "Course zawiera 3 kolumny":
                    len(inspector.get_columns(
                        "courses"
                    )) == 3,

                "Teacher ma klucz glowny id":
                    inspector.get_pk_constraint(
                        "teachers"
                    )["constrained_columns"] == ["id"],

                "Course ma klucz glowny id":
                    inspector.get_pk_constraint(
                        "courses"
                    )["constrained_columns"] == ["id"],

                "Poprawny klucz obcy teacher_id":
                    valid_foreign_key,

                "Relacja Teacher to One-to-Many":
                    teacher_relation.direction.name
                    == "ONETOMANY",

                "Relacja Course to Many-to-One":
                    course_relation.direction.name
                    == "MANYTOONE",

                "Teacher.courses jest kolekcja":
                    teacher_relation.uselist is True,

                "Course.teacher jest pojedynczym obiektem":
                    course_relation.uselist is False,

                "Poprawne back_populates Teacher":
                    teacher_relation.back_populates
                    == "teacher",

                "Poprawne back_populates Course":
                    course_relation.back_populates
                    == "courses",

                "Nauczyciel ma poprawne ID":
                    saved_teacher.id == teacher_id,

                "Poprawne imie nauczyciela":
                    saved_teacher.name == TEACHER_NAME,

                "Nauczyciel ma 3 kursy":
                    len(saved_courses) == 3,

                "Poprawne nazwy kursow":
                    {
                        course.title
                        for course in saved_courses
                    } == set(COURSE_TITLES),

                "Wszystkie kursy maja ID":
                    all(
                        course.id is not None
                        for course in saved_courses
                    ),

                "Identyfikatory kursow sa unikalne":
                    len({
                        course.id
                        for course in saved_courses
                    }) == 3,

                "Wszystkie kursy maja poprawny teacher_id":
                    all(
                        course.teacher_id == teacher_id
                        for course in saved_courses
                    ),

                "Relacja odwrotna dziala poprawnie":
                    all(
                        course.teacher is saved_teacher
                        for course in saved_courses
                    ),

                "Poprawna liczba nowych nauczycieli":
                    teachers_after - teachers_before
                    == int(teacher_created),

                "Poprawna liczba nowych kursow":
                    courses_after - courses_before
                    == added_courses,

                "Dane dostepne w nowej sesji":
                    len(saved_teacher.courses) == 3,

                "Dane studentow pozostaly niezmienione":
                    students_before == students_after,

                "Brak nowych obiektow w sesji":
                    len(session.new) == 0,

                "Brak zmodyfikowanych obiektow":
                    len(session.dirty) == 0,

                "Brak obiektow do usuniecia":
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

        section("15. PODSUMOWANIE")

        print("Modele: Teacher, Course")
        print("Tabele: teachers, courses")
        print("Relacja: One-to-Many (1:N)")
        print(f"Nauczyciel: {TEACHER_NAME}")
        print("Liczba przypisanych kursow: 3")
        print("Wykorzystano ForeignKey.")
        print("Wykorzystano relationship.")
        print("Wykorzystano back_populates.")
        print("Wykonano session.commit().")
        print("Zweryfikowano dane w nowej sesji.")
        print("Tabela students pozostala bez zmian.")
        print("Wszystkie testy zakonczone pomyslnie.")
        print("Zadanie 7 wykonane poprawnie.")

    except SQLAlchemyError as error:

        print(f"Blad SQLAlchemy: {error}")

        raise

    finally:

        engine.dispose()


if __name__ == "__main__":
    main()
