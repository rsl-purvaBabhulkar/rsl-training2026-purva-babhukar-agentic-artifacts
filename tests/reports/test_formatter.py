import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "src"))

from models.book import Book
from models.member import Member
from reports.formatter import generate_overdue_report, generate_member_loan_counts_report


def test_generate_overdue_report_empty_list_does_not_raise():
    """reports/ rule: must never raise, even on empty input."""
    report = generate_overdue_report([])
    assert "No books are currently overdue." in report


def test_generate_overdue_report_is_pure():
    """reports/ rule: must never mutate the objects it's given."""
    book = Book("Dune", "Frank Herbert", 1965)
    book.check_out()
    book.due_date = "2020-01-01T12:00:00"
    member = Member("Ada Lovelace", "ada@example.com")

    before = (book.is_borrowed, book.due_date, member.borrowed_book_ids[:])
    generate_overdue_report([{"book": book, "member": member}])
    after = (book.is_borrowed, book.due_date, member.borrowed_book_ids[:])

    assert before == after


def test_generate_overdue_report_follows_existing_shape():
    """reports/ rule: title line + '=' * 24 underline, like the other reports."""
    report = generate_overdue_report([])
    lines = report.split("\n")
    assert lines[0] == "Overdue Books Report"
    assert lines[1] == "=" * 24


def test_generate_member_loan_counts_report_happy_path():
    """Skill output: non-empty input renders one line per member with their count."""
    member = Member("Ada Lovelace", "ada@example.com")
    member.borrowed_book_ids = ["book-1", "book-2"]

    report = generate_member_loan_counts_report([member])

    assert "Ada Lovelace: 2 book(s) currently borrowed" in report


def test_generate_member_loan_counts_report_empty_does_not_raise():
    """Skill output: empty input never raises, matches project convention."""
    report = generate_member_loan_counts_report([])
    assert "No members registered." in report
