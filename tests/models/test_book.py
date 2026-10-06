import sys
import os
from datetime import datetime, timedelta

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "src"))

import pytest
from models.book import Book


def test_renew_extends_due_date_when_not_overdue():
    """Happy path: renewing a borrowed, not-yet-overdue book pushes the due date out."""
    book = Book("Dune", "Frank Herbert", 1965)
    book.check_out(loan_days=14)
    original_due = datetime.fromisoformat(book.due_date)

    book.renew(extra_days=7)

    new_due = datetime.fromisoformat(book.due_date)
    assert new_due == original_due + timedelta(days=7)


def test_renew_raises_when_book_not_borrowed():
    """Failure path: renewing a book that was never checked out should fail clearly."""
    book = Book("1984", "George Orwell", 1949)

    with pytest.raises(ValueError, match="not currently borrowed"):
        book.renew()


def test_renew_raises_when_book_is_overdue():
    """Failure path: an overdue book cannot be renewed; it must be returned first."""
    book = Book("Odyssey", "Homer", 750)
    book.check_out(loan_days=14)
    book.due_date = (datetime.now() - timedelta(days=1)).isoformat()

    with pytest.raises(ValueError, match="overdue"):
        book.renew()
