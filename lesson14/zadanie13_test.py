# Lekcja 14 - Zadanie 13
# E-commerce Database Design - testy koncowe

import unittest

from collections import defaultdict
from decimal import Decimal
from unittest.mock import patch

from sqlalchemy import (
    create_engine,
    event,
    inspect,
    text
)

from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

import zadanie13 as app


class TestEcommerce(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        cls.engine = create_engine(
            "sqlite:///:memory:",
            echo=False
        )

        @event.listens_for(cls.engine, "connect")
        def enable_foreign_keys(connection, record):
            cursor = connection.cursor()
            cursor.execute("PRAGMA foreign_keys=ON")
            cursor.close()

        cls.Session = sessionmaker(
            bind=cls.engine
        )

        cls.engine_patch = patch.object(
            app,
            "engine",
            cls.engine
        )

        cls.session_patch = patch.object(
            app,
            "SessionLocal",
            cls.Session
        )

        cls.engine_patch.start()
        cls.session_patch.start()

        cls.addClassCleanup(cls.engine.dispose)
        cls.addClassCleanup(cls.engine_patch.stop)
        cls.addClassCleanup(cls.session_patch.stop)

        app.create_database()
        app.generate_sample_data()

    def setUp(self):
        self.session = self.Session()

    def tearDown(self):
        self.session.rollback()
        self.session.close()

    def assert_sql_rejected(self, statement):

        with self.assertRaises(IntegrityError):
            self.session.execute(text(statement))

        self.session.rollback()

    # ==================================================
    # 1. SCHEMAT I GENERATOR DANYCH
    # ==================================================

    def test_01_tables(self):

        self.assertEqual(
            set(inspect(self.engine).get_table_names()),
            {
                "users",
                "categories",
                "products",
                "orders",
                "order_items",
                "product_categories"
            }
        )

    def test_02_schema_verification(self):

        self.assertTrue(
            app.verify_database_schema()
        )

    def test_03_record_counts(self):

        self.assertEqual(
            app.get_database_counts(self.session),
            {
                "users": 10,
                "categories": 5,
                "products": 20,
                "orders": 30,
                "order_items": 90,
                "product_categories": 28
            }
        )

    def test_04_generator_idempotency(self):

        before = app.get_database_counts(
            self.session
        )

        self.session.rollback()

        self.assertFalse(
            app.generate_sample_data()
        )

        after = app.get_database_counts(
            self.session
        )

        self.assertEqual(before, after)

    def test_05_database_integrity(self):

        connection = self.session.connection()

        self.assertEqual(
            connection.exec_driver_sql(
                "PRAGMA foreign_keys"
            ).scalar(),
            1
        )

        self.assertEqual(
            connection.exec_driver_sql(
                "PRAGMA integrity_check"
            ).scalar(),
            "ok"
        )

        self.assertEqual(
            connection.exec_driver_sql(
                "PRAGMA foreign_key_check"
            ).all(),
            []
        )

    # ==================================================
    # 2. RELACJE ORM
    # ==================================================

    def test_06_user_orders(self):

        users = self.session.query(app.User).all()

        for user in users:
            self.assertEqual(len(user.orders), 3)

            for order in user.orders:
                self.assertEqual(order.user_id, user.id)

    def test_07_order_items(self):

        orders = self.session.query(app.Order).all()

        for order in orders:
            self.assertEqual(len(order.items), 3)

            for item in order.items:
                self.assertEqual(item.order_id, order.id)

    def test_08_product_categories(self):

        products = self.session.query(app.Product).all()

        for product in products:

            self.assertTrue(product.categories)

            for category in product.categories:
                self.assertIn(product, category.products)

        self.assertEqual(
            sum(len(p.categories) > 1 for p in products),
            8
        )

    def test_09_product_order_items(self):

        products = self.session.query(app.Product).all()

        for product in products:

            self.assertTrue(product.order_items)

            for item in product.order_items:
                self.assertEqual(
                    item.product_id,
                    product.id
                )

    def test_10_delete_orphan(self):

        order = self.session.get(app.Order, 1)

        item = order.items[0]
        item_id = item.id

        order.items.remove(item)

        self.session.flush()

        self.assertIsNone(
            self.session.get(app.OrderItem, item_id)
        )

        self.session.rollback()

        self.assertIsNotNone(
            self.session.get(app.OrderItem, item_id)
        )

    # ==================================================
    # 3. WALIDATORY PYTHON
    # ==================================================

    def test_11_invalid_product_price(self):

        for value in (0, -1, "abc", "NaN"):

            with self.subTest(value=value):

                with self.assertRaises(ValueError):
                    app.Product(
                        name="Test",
                        price=value,
                        stock=10
                    )

    def test_12_invalid_stock(self):

        for value in (-1, 1.5, True):

            with self.subTest(value=value):

                with self.assertRaises(ValueError):
                    app.Product(
                        name="Test",
                        price=Decimal("10.00"),
                        stock=value
                    )

    def test_13_invalid_email(self):

        for value in ("", "abc", "abc@", "@example.com"):

            with self.subTest(value=value):

                with self.assertRaises(ValueError):
                    app.User(
                        name="Test User",
                        email=value
                    )

    def test_14_invalid_order_status(self):

        with self.assertRaises(ValueError):
            app.Order(status="unknown")

    def test_15_invalid_order_item(self):

        for value in (0, -1, 1.5, True):

            with self.subTest(quantity=value):

                with self.assertRaises(ValueError):
                    app.OrderItem(
                        quantity=value,
                        unit_price=Decimal("10.00")
                    )

        for value in (0, -1, "NaN"):

            with self.subTest(unit_price=value):

                with self.assertRaises(ValueError):
                    app.OrderItem(
                        quantity=1,
                        unit_price=value
                    )

    # ==================================================
    # 4. OGRANICZENIA BAZY DANYCH
    # ==================================================

    def test_16_unique_email(self):

        self.assert_sql_rejected(
            """
            UPDATE users
            SET email = (
                SELECT email FROM users WHERE id = 1
            )
            WHERE id = 2
            """
        )

    def test_17_positive_product_price(self):

        self.assert_sql_rejected(
            "UPDATE products SET price = 0 WHERE id = 1"
        )

    def test_18_nonnegative_stock(self):

        self.assert_sql_rejected(
            "UPDATE products SET stock = -1 WHERE id = 1"
        )

    def test_19_positive_quantity(self):

        self.assert_sql_rejected(
            "UPDATE order_items SET quantity = 0 WHERE id = 1"
        )

    def test_20_positive_unit_price(self):

        self.assert_sql_rejected(
            "UPDATE order_items SET unit_price = -1 WHERE id = 1"
        )

    def test_21_valid_order_status(self):

        self.assert_sql_rejected(
            """
            UPDATE orders
            SET status = 'unknown'
            WHERE id = 1
            """
        )

    def test_22_foreign_key(self):

        self.assert_sql_rejected(
            """
            UPDATE orders
            SET user_id = 999999
            WHERE id = 1
            """
        )

    # ==================================================
    # 5. RAPORT SPRZEDAZOWY
    # ==================================================

    def test_23_top_five(self):

        top = app.get_top_products(self.session)

        self.assertEqual(len(top), 5)

        self.assertEqual(
            [p.product_id for p in top],
            [3, 9, 8, 10, 7]
        )

    def test_24_top_units(self):

        top = app.get_top_products(self.session)

        self.assertEqual(
            [p.units_sold for p in top],
            [23, 22, 16, 16, 16]
        )

        self.assertEqual(
            sum(p.units_sold for p in top),
            93
        )

    def test_25_top_revenue(self):

        top = app.get_top_products(self.session)

        self.assertEqual(
            sum(p.revenue for p in top),
            Decimal("67077.70")
        )

    def test_26_sales_summary(self):

        summary = app.get_sales_summary(self.session)

        self.assertEqual(summary.order_count, 26)
        self.assertEqual(summary.item_count, 78)
        self.assertEqual(summary.units_sold, 219)

        self.assertEqual(
            summary.revenue,
            Decimal("136886.43")
        )

    def test_27_independent_calculation(self):

        totals = defaultdict(
            lambda: [0, Decimal("0.00")]
        )

        orders = self.session.query(app.Order).all()

        for order in orders:

            if order.status not in (
                "completed", "paid", "shipped"
            ):
                continue

            for item in order.items:

                totals[item.product_id][0] += (
                    item.quantity
                )

                totals[item.product_id][1] += (
                    item.quantity * item.unit_price
                )

        expected = sorted(
            totals.items(),
            key=lambda entry: (
                -entry[1][0],
                -entry[1][1],
                entry[0]
            )
        )[:5]

        actual = app.get_top_products(self.session)

        self.assertEqual(
            [
                (p.product_id, p.units_sold, p.revenue)
                for p in actual
            ],
            [
                (product_id, values[0], values[1])
                for product_id, values in expected
            ]
        )

    def test_28_invalid_limit(self):

        for limit in (0, -1, 2.5, "5", None, True):

            with self.subTest(limit=limit):

                with self.assertRaises(ValueError):
                    app.get_top_products(
                        self.session,
                        limit=limit
                    )

    def test_29_historical_price(self):

        before = app.get_sales_summary(
            self.session
        ).revenue

        product = self.session.get(app.Product, 3)

        product.price = Decimal("999.99")

        self.session.flush()

        after = app.get_sales_summary(
            self.session
        ).revenue

        self.assertEqual(before, after)

    def test_30_empty_sales_report(self):

        orders = self.session.query(app.Order).all()

        for order in orders:
            order.status = "cancelled"

        self.session.flush()

        self.assertEqual(
            app.get_top_products(self.session),
            []
        )

        summary = app.get_sales_summary(
            self.session
        )

        self.assertEqual(summary.order_count, 0)
        self.assertEqual(summary.item_count, 0)
        self.assertEqual(summary.units_sold, 0)
        self.assertEqual(
            summary.revenue,
            Decimal("0.00")
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
