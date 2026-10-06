import uuid
from datetime import datetime, timedelta
from typing import Dict, Any, Optional

class Book:
    def __init__(self, title: str, author: str, year_published: int):
        self.book_id: str = str(uuid.uuid4())
        self.title: str = title
        self.author: str = author
        self.year_published: int = year_published
        self.added_on: str = datetime.now().isoformat()
        
        # State management
        self.is_borrowed: bool = False
        self.due_date: Optional[str] = None

    def check_out(self, loan_days: int = 14) -> None:
        """Marks the book as borrowed and sets a due date."""
        if self.is_borrowed:
            raise ValueError(f"Book '{self.title}' is already borrowed.")
        
        self.is_borrowed = True
        due = datetime.now() + timedelta(days=loan_days)
        self.due_date = due.isoformat()

    def return_book(self) -> None:
        """Clears the borrowed status and due date."""
        self.is_borrowed = False
        self.due_date = None

   
    def is_overdue(self) -> bool:
        """Checks if the current date is past the due date."""
        if not self.is_borrowed or not self.due_date:
            return False
        return datetime.now() > datetime.fromisoformat(self.due_date)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "book_id": self.book_id,
            "title": self.title,
            "author": self.author,
            "year_published": self.year_published,
            "is_borrowed": self.is_borrowed,
            "due_date": self.due_date
        }