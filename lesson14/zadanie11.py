# Lekcja 14 - Zadanie 11
# Filtrowanie i agregacje

import random
import calendar

from datetime import datetime, timedelta
from decimal import Decimal
from collections import defaultdict

from sqlalchemy import (
    Column,
    Integer,
    String,
    Numeric,
    DateTime,
    func,
    inspect
)

from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

from zadanie02 import Base, engine, DATABASE_PATH


Session = sessionmaker(bind=engine)

SEED = 42
N_CUSTOMERS = 10
N_ORDERS = 100

CUSTOMERS = [
    "Anna",
    "Piotr",
    "Maria",
    "Tomasz",
    "Katarzyna",
    "Adam",
    "Magdalena",
    "Pawel",
    "Joanna",
    "Michal"
]


class Order(Base):

    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)

    customer_name = Column(
        String(100),
        nullable=False
    )

    total = Column(
        Numeric(10, 2),
        nullable=False
    )

    created_at = Column(
        DateTime,
        nullable=False
    )

    def __repr__(self):
        return (
            f"Order(id={self.id}, "
            f"customer_name={self.customer_name!r}, "
            f"total={self.total}, "
            f"created_at={self.created_at})"
        )


def section(title):

    print(f"\n{title}")
    print("-" * 80)


def months_ago(value, months):

    month_index = (
        value.year * 12
        + value.month - 1
        - months
    )

    year, month = divmod(month_index, 12)

    month += 1

    day = min(
        value.day,
        calendar.monthrange(year, month)[1]
    )

    return value.replace(
        year=year,
        month=month,
        day=day
    )


def generate_orders(now):

    rng = random.Random(SEED)

    start_date = months_ago(now, 3)

    max_seconds = int(
        (now - start_date).total_seconds()
    )

    orders = []

    for customer in CUSTOMERS:

        for _ in range(10):

            amount = (
                Decimal(rng.randint(1000, 100000))
                / Decimal("100")
            )

            created_at = start_date + timedelta(
                seconds=rng.randint(0, max_seconds)
            )

            order = Order(
                customer_name=customer,
                total=amount,
                created_at=created_at
            )

            orders.append(order)

    return orders


def print_orders(orders):

    print(
        f"{'ID':<6}"
        f"{'KLIENT':<15}"
        f"{'WARTOSC PLN':>15}"
        f"{'DATA':>24}"
    )

    print("-" * 80)

    for order in orders:

        print(
            f"{order.id:<6}"
            f"{order.customer_name:<15}"
            f"{order.total:>15.2f}"
            f"{order.created_at:%Y-%m-%d %H:%M:%S}".rjust(24)
        )


def main():

    print("=" * 80)
    print("ZADANIE 11 - FILTROWANIE I AGREGACJE")
    print("=" * 80)

    now = datetime.now().replace(microsecond=0)

    three_months_ago = months_ago(now, 3)
    one_month_ago = months_ago(now, 1)

    section("1. PARAMETRY ANALIZY")

    print(f"Baza danych: {DATABASE_PATH}")
    print(f"Model: {Order.__name__}")
    print(f"Tabela: {Order.__tablename__}")
    print(f"Liczba klientow: {N_CUSTOMERS}")
    print(f"Liczba zamowien: {N_ORDERS}")
    print(f"Ziarno losowania: {SEED}")
    print(f"Data poczatkowa: {three_months_ago}")
    print(f"Data koncowa: {now}")
    print(f"Ostatni miesiac od: {one_month_ago}")

    section("2. TWORZENIE TABELI")

    tables_before = set(
        inspect(engine).get_table_names()
    )

    Base.metadata.create_all(engine)

    tables_after = set(
        inspect(engine).get_table_names()
    )

    print(f"Tabele przed: {sorted(tables_before)}")
    print(f"Tabele po: {sorted(tables_after)}")

    section("3. GENEROWANIE DANYCH")

    orders = generate_orders(now)

    print(f"Wygenerowano zamowien: {len(orders)}")

    for order in orders[:5]:
        print(order)

    try:

        with Session() as session:

            section("4. ZAPIS DANYCH DO BAZY")

            existing_count = session.query(
                Order
            ).count()

            print(
                f"Istniejace zamowienia: {existing_count}"
            )

            if existing_count == 0:

                session.add_all(orders)

                session.commit()

                print("Dodano 100 zamowien.")
                print("Commit wykonany poprawnie.")

            else:

                print(
                    "Tabela zawiera juz dane. "
                    "Nie dodajemy duplikatow."
                )

        with Session() as session:

            section("5. WERYFIKACJA DANYCH")

            all_orders = (
                session.query(Order)
                .order_by(Order.id)
                .all()
            )

            order_count = session.query(
                func.count(Order.id)
            ).scalar()

            customer_count = session.query(
                func.count(
                    func.distinct(Order.customer_name)
                )
            ).scalar()

            print(f"Liczba zamowien: {order_count}")
            print(f"Liczba klientow: {customer_count}")

            print("\nPierwsze 10 zamowien:")

            print_orders(all_orders[:10])

            section("6. SUMA ZAMOWIEN DLA KAZDEGO KLIENTA")

            customer_totals = (
                session.query(
                    Order.customer_name,
                    func.sum(Order.total).label(
                        "total_sum"
                    )
                )
                .group_by(Order.customer_name)
                .order_by(
                    func.sum(Order.total).desc(),
                    Order.customer_name.asc()
                )
                .all()
            )

            print(
                f"{'KLIENT':<20}"
                f"{'SUMA ZAMOWIEN PLN':>22}"
            )

            print("-" * 80)

            for customer, total in customer_totals:

                print(
                    f"{customer:<20}"
                    f"{total:>22.2f}"
                )

            section("7. SREDNIA WARTOSC ZAMOWIENIA")

            average_order = session.query(
                func.avg(Order.total)
            ).scalar()

            print(
                f"Srednia wartosc zamowienia: "
                f"{average_order:.2f} PLN"
            )

            section("8. KLIENT Z NAJWIEKSZA SUMA ZAMOWIEN")

            best_customer = (
                session.query(
                    Order.customer_name,
                    func.sum(Order.total).label(
                        "total_sum"
                    )
                )
                .group_by(Order.customer_name)
                .order_by(
                    func.sum(Order.total).desc(),
                    Order.customer_name.asc()
                )
                .first()
            )

            print(
                f"Najlepszy klient: "
                f"{best_customer.customer_name}"
            )

            print(
                f"Suma zamowien: "
                f"{best_customer.total_sum:.2f} PLN"
            )

            section("9. LICZBA ZAMOWIEN W OSTATNIM MIESIACU")

            recent_count = (
                session.query(
                    func.count(Order.id)
                )
                .filter(
                    Order.created_at >= one_month_ago,
                    Order.created_at <= now
                )
                .scalar()
            )

            recent_orders = (
                session.query(Order)
                .filter(
                    Order.created_at >= one_month_ago,
                    Order.created_at <= now
                )
                .order_by(Order.created_at.desc())
                .all()
            )

            print(f"Okres od: {one_month_ago}")
            print(f"Okres do: {now}")
            print(f"Liczba zamowien: {recent_count}")

            recent_percentage = (
                recent_count / order_count * 100
            )

            print(
                f"Udzial wszystkich zamowien: "
                f"{recent_percentage:.2f}%"
            )

            print("\nNajnowsze zamowienia:")

            print_orders(recent_orders[:10])

            section("10. DODATKOWE STATYSTYKI")

            statistics = session.query(
                func.sum(Order.total),
                func.min(Order.total),
                func.max(Order.total),
                func.count(Order.id)
            ).one()

            total_revenue = statistics[0]
            min_order = statistics[1]
            max_order = statistics[2]

            print(
                f"Laczna wartosc zamowien: "
                f"{total_revenue:.2f} PLN"
            )

            print(
                f"Najmniejsze zamowienie: "
                f"{min_order:.2f} PLN"
            )

            print(
                f"Najwieksze zamowienie: "
                f"{max_order:.2f} PLN"
            )

            print(
                f"Srednia wartosc: "
                f"{average_order:.2f} PLN"
            )

            section("11. RAPORT KLIENTOW")

            customer_report = (
                session.query(
                    Order.customer_name,
                    func.count(Order.id),
                    func.sum(Order.total),
                    func.avg(Order.total)
                )
                .group_by(Order.customer_name)
                .order_by(
                    func.sum(Order.total).desc(),
                    Order.customer_name.asc()
                )
                .all()
            )

            print(
                f"{'KLIENT':<15}"
                f"{'ZAMOWIENIA':>12}"
                f"{'SUMA PLN':>16}"
                f"{'SREDNIA PLN':>16}"
                f"{'UDZIAL':>12}"
            )

            print("-" * 80)

            for name, count, total, average in customer_report:

                share = (
                    total / total_revenue * 100
                )

                print(
                    f"{name:<15}"
                    f"{count:>12}"
                    f"{total:>16.2f}"
                    f"{average:>16.2f}"
                    f"{share:>11.2f}%"
                )

            section("12. WIZUALIZACJA SUM ZAMOWIEN")

            max_total = max(
                total
                for _, total in customer_totals
            )

            for name, total in customer_totals:

                bar_length = round(
                    total / max_total * 40
                )

                bar = "█" * bar_length

                print(
                    f"{name:<12} "
                    f"{bar:<40} "
                    f"{total:>10.2f} PLN"
                )

            print(
                "\nNajwieksza suma odpowiada 40 znakom."
            )

            section("13. NIEZALEZNA WERYFIKACJA W PYTHONIE")

            python_totals = defaultdict(
                lambda: Decimal("0.00")
            )

            python_counts = defaultdict(int)

            for order in all_orders:

                python_totals[
                    order.customer_name
                ] += order.total

                python_counts[
                    order.customer_name
                ] += 1

            python_sum = sum(
                order.total
                for order in all_orders
            )

            python_average = (
                python_sum / len(all_orders)
            )

            python_recent_count = sum(
                one_month_ago <= order.created_at <= now
                for order in all_orders
            )

            python_best = sorted(
                python_totals.items(),
                key=lambda item: (-item[1], item[0])
            )[0]

            sql_totals = dict(customer_totals)

            print(
                f"Sumy SQL i Python zgodne: "
                f"{sql_totals == dict(python_totals)}"
            )

            print(
                f"Srednia SQL: {average_order:.2f}"
            )

            print(
                f"Srednia Python: {python_average:.2f}"
            )

            print(
                f"Najlepszy klient SQL: "
                f"{best_customer.customer_name}"
            )

            print(
                f"Najlepszy klient Python: "
                f"{python_best[0]}"
            )

            print(
                f"Ostatni miesiac SQL: {recent_count}"
            )

            print(
                f"Ostatni miesiac Python: "
                f"{python_recent_count}"
            )

            section("14. AUTOMATYCZNE TESTY")

            columns = inspect(engine).get_columns(
                "orders"
            )

            primary_key = inspect(
                engine
            ).get_pk_constraint("orders")

            tests = {

                "Plik test.db istnieje":
                    DATABASE_PATH.exists(),

                "Tabela orders istnieje":
                    "orders" in tables_after,

                "Zachowano poprzednie tabele":
                    tables_before.issubset(tables_after),

                "Tabela zawiera 4 kolumny":
                    len(columns) == 4,

                "Nazwy kolumn sa poprawne":
                    {column["name"] for column in columns}
                    == {
                        "id",
                        "customer_name",
                        "total",
                        "created_at"
                    },

                "ID jest kluczem glownym":
                    primary_key["constrained_columns"]
                    == ["id"],

                "Wygenerowano 100 obiektow":
                    len(orders) == N_ORDERS,

                "Zapisano 100 zamowien":
                    order_count == N_ORDERS,

                "Odczytano 100 zamowien":
                    len(all_orders) == N_ORDERS,

                "Zapisano 10 klientow":
                    customer_count == N_CUSTOMERS,

                "Identyfikatory sa unikalne":
                    len({
                        order.id
                        for order in all_orders
                    }) == N_ORDERS,

                "Imiona klientow sa poprawne":
                    set(python_counts) == set(CUSTOMERS),

                "Kazdy klient ma 10 zamowien":
                    all(
                        count == 10
                        for count in python_counts.values()
                    ),

                "Wartosci zamowien od 10 do 1000 PLN":
                    all(
                        Decimal("10")
                        <= order.total
                        <= Decimal("1000")
                        for order in all_orders
                    ),

                "Daty nie sa z przyszlosci":
                    all(
                        order.created_at <= now
                        for order in all_orders
                    ),

                "Daty w ostatnich 3 miesiacach":
                    all(
                        three_months_ago
                        <= order.created_at
                        <= now
                        for order in all_orders
                    ),

                "Agregacja zwrocila 10 klientow":
                    len(customer_totals) == N_CUSTOMERS,

                "Sumy SQL i Python sa identyczne":
                    sql_totals == dict(python_totals),

                "Sumy posortowane malejaco":
                    all(
                        customer_totals[i][1]
                        >= customer_totals[i + 1][1]
                        for i in range(
                            len(customer_totals) - 1
                        )
                    ),

                "Srednia wartosc jest poprawna":
                    abs(
                        Decimal(str(average_order))
                        - python_average
                    ) < Decimal("0.000001"),

                "Najlepszy klient jest poprawny":
                    best_customer.customer_name
                    == python_best[0],

                "Suma najlepszego klienta jest poprawna":
                    best_customer.total_sum
                    == python_best[1],

                "Liczba zamowien ostatniego miesiaca":
                    recent_count == python_recent_count,

                "COUNT i liczba odczytanych rekordow zgodne":
                    recent_count == len(recent_orders),

                "Daty odfiltrowanych zamowien poprawne":
                    all(
                        one_month_ago
                        <= order.created_at
                        <= now
                        for order in recent_orders
                    ),

                "Laczna suma SQL i Python zgodna":
                    total_revenue == python_sum,

                "Suma agregacji zgodna z suma globalna":
                    sum(sql_totals.values())
                    == total_revenue,

                "Minimalna wartosc poprawna":
                    min_order == min(
                        order.total
                        for order in all_orders
                    ),

                "Maksymalna wartosc poprawna":
                    max_order == max(
                        order.total
                        for order in all_orders
                    ),

                "Raport zawiera 10 klientow":
                    len(customer_report) == N_CUSTOMERS,

                "Raport obejmuje 100 zamowien":
                    sum(
                        row[1]
                        for row in customer_report
                    ) == N_ORDERS,

                "Brak nowych obiektow w sesji":
                    len(session.new) == 0,

                "Brak zmodyfikowanych obiektow":
                    len(session.dirty) == 0,

                "Brak usunietych obiektow":
                    len(session.deleted) == 0,

                "Liczba rekordow nie ulegla zmianie":
                    session.query(Order).count()
                    == order_count
            }

            for name, result in tests.items():

                print(f"Czy {name}: {result}")

            passed = sum(
                bool(result)
                for result in tests.values()
            )

            print(
                f"\nZaliczone testy: "
                f"{passed}/{len(tests)}"
            )

            assert all(tests.values()), (
                "Nie wszystkie testy zostaly zaliczone."
            )

            section("15. PODSUMOWANIE")

            print("Model: Order")
            print("Tabela: orders")

            print(f"Liczba klientow: {customer_count}")
            print(f"Liczba zamowien: {order_count}")

            print(
                f"Laczna wartosc: "
                f"{total_revenue:.2f} PLN"
            )

            print(
                f"Srednia wartosc: "
                f"{average_order:.2f} PLN"
            )

            print(
                f"Najlepszy klient: "
                f"{best_customer.customer_name}"
            )

            print(
                f"Zamowienia w ostatnim miesiacu: "
                f"{recent_count}"
            )

            print("Wykorzystano func.sum().")
            print("Wykorzystano func.avg().")
            print("Wykorzystano func.count().")
            print("Wykorzystano group_by().")
            print("Wykorzystano order_by().")
            print("Wykorzystano filter().")
            print("Zweryfikowano wyniki w Pythonie.")
            print("Zachowano poprzednie tabele.")
            print("Wszystkie testy zakonczone pomyslnie.")
            print("Zadanie 11 wykonane poprawnie.")

    except SQLAlchemyError as error:

        print(f"Blad SQLAlchemy: {error}")
        raise

    finally:

        engine.dispose()


if __name__ == "__main__":
    main()
