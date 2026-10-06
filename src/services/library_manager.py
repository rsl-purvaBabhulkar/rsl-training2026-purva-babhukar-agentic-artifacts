from datetime import datetime, timedelta
from typing import Dict, List, Optional
from models.book import Book
from models.member import Member

class LibraryManager:
    def __init__(self):
        # In-memory "databases"
        self.books: Dict[str, Book] = {}
        self.members: Dict[str, Member] = {}
        self.daily_fine_rate: float = 50
        self.max_outstanding_fine: float = 250

    def add_book(self, book: Book) -> None:
        """Adds a book to the in-memory catalog.

        Side effects: inserts `book` into `self.books`, keyed by its ID.
        """
        self.books[book.book_id] = book

    def register_member(self, member: Member) -> None:
        """Registers a new member.

        Side effects: inserts `member` into `self.members`, keyed by their ID.
        """
        self.members[member.member_id] = member

    def checkout_book(self, member_id: str, book_id: str) -> None:
        """Checks a book out to a member, if allowed.

        Side effects: marks `book` as borrowed and sets its due date;
        appends `book_id` to `member.borrowed_book_ids`.

        Raises:
            ValueError: if the member or book ID is invalid.
            PermissionError: if the member's outstanding fines exceed
                `self.max_outstanding_fine`.
        """
        member = self.members.get(member_id)
        book = self.books.get(book_id)

        if not member or not book:
            raise ValueError("Invalid member ID or book ID.")

        if member.accumulated_fines > self.max_outstanding_fine:
            raise PermissionError(
                f"Cannot borrow books with outstanding fines over ₹{self.max_outstanding_fine:.2f}."
            )

        book.check_out()
        member.borrow_book(book_id)

    def process_return(self, member_id: str, book_id: str) -> None:
        """Processes a member returning a book, applying a fine if it's overdue.

        Side effects: clears `book`'s borrowed status/due date; removes
        `book_id` from `member.borrowed_book_ids`; adds a flat fine to
        `member.accumulated_fines` if the book was overdue.

        Raises:
            ValueError: if the member or book ID is invalid.
        """
        member = self.members.get(member_id)
        book = self.books.get(book_id)

        if not member or not book:
            raise ValueError("Invalid member ID or book ID.")

        if book.is_overdue():
            # Flat fine for simplicity, but could be calculated by days overdue
            member.add_fine(self.daily_fine_rate * 5) 

        book.return_book()
        member.return_book(book_id)

    def renew_book(self, member_id: str, book_id: str) -> None:
        """Extends a borrowed book's due date by seven days when it is not overdue.

        Side effects: updates `book.due_date` to a later timestamp for the same loan.

        Raises:
            ValueError: if the member or book ID is invalid, if the member does not own
                the book, if the book is not currently borrowed, or if the book is overdue.
        """
        member = self.members.get(member_id)
        book = self.books.get(book_id)

        if not member or not book:
            raise ValueError("Invalid member ID or book ID.")

        if book_id not in member.borrowed_book_ids:
            raise ValueError(f"Book '{book_id}' is not currently borrowed by member '{member.member_id}'.")

        if not book.is_borrowed:
            raise ValueError(f"Book '{book.title}' is not currently borrowed.")

        if book.is_overdue():
            raise ValueError(f"Book '{book.title}' is already overdue and cannot be renewed.")

        if not book.due_date:
            raise ValueError(f"Book '{book.title}' has no due date set.")

        current_due = datetime.fromisoformat(book.due_date)
        book.due_date = (current_due + timedelta(days=7)).isoformat()

    def get_overdue_loans(self) -> List[Dict[str, object]]:
        """Finds all currently overdue books and the members holding them.

        Side effects: none — this is a read-only query, no state is mutated.

        Returns:
            A list of dicts, each with keys "book" (Book) and "member" (Member),
            for every borrowed book that is currently overdue.
        """
        overdue = []
        for book in self.books.values():
            if not book.is_overdue():
                continue
            owner = next(
                (m for m in self.members.values() if book.book_id in m.borrowed_book_ids),
                None,
            )
            if owner is not None:
                overdue.append({"book": book, "member": owner})
        return overdue

    def search_books_by_author(self, author_name: str) -> List[Book]:
        """Finds all books whose author name contains `author_name` (case-insensitive).

        Side effects: none — read-only query.
        """
        return [book for book in self.books.values() if author_name.lower() in book.author.lower()]
