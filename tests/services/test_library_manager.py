import sys
import os
from datetime import datetime, timedelta

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "src"))

import pytest
from models.book import Book
from models.member import Member
from services.library_manager import LibraryManager


def _setup_checked_out(manager: LibraryManager):
    book = Book("Dune", "Frank Herbert", 1965)
    member = Member("Ada Lovelace", "ada@example.com")
    manager.add_book(book)
    manager.register_member(member)
    manager.checkout_book(member.member_id, book.book_id)
    return member, book




def test_checkout_blocked_by_fines_uses_consistent_currency_format():
    """Regression test for Task 4 fix: PermissionError must use ₹{amount:.2f}, not '250₹'."""
    manager = LibraryManager()
    book = Book("Dune", "Frank Herbert", 1965)
    member = Member("Ada Lovelace", "ada@example.com")
    manager.add_book(book)
    manager.register_member(member)
    member.accumulated_fines = 300.0

    with pytest.raises(PermissionError, match=r"₹250\.00"):
        manager.checkout_book(member.member_id, book.book_id)


def test_get_overdue_loans_finds_overdue_books():
    """services/ rule: validated read-only query, documented side effects (none)."""
    manager = LibraryManager()
    member, book = _setup_checked_out(manager)
    book.due_date = "2020-01-01T12:00:00"  # force overdue

    overdue = manager.get_overdue_loans()

    assert len(overdue) == 1
    assert overdue[0]["book"] is book
    assert overdue[0]["member"] is member


def test_renew_book_extends_due_date_by_seven_days_when_not_overdue():
    """A valid renewal should extend the current due date by seven days."""
    manager = LibraryManager()
    member, book = _setup_checked_out(manager)
    original_due = datetime.fromisoformat(book.due_date)

    manager.renew_book(member.member_id, book.book_id)

    assert book.is_borrowed is True
    assert datetime.fromisoformat(book.due_date) == original_due + timedelta(days=7)


def test_renew_book_rejects_overdue_books():
    """Overdue books cannot be renewed until returned and checked out again."""
    manager = LibraryManager()
    member, book = _setup_checked_out(manager)
    book.due_date = "2020-01-01T12:00:00"

    with pytest.raises(ValueError, match="overdue"):
        manager.renew_book(member.member_id, book.book_id)
