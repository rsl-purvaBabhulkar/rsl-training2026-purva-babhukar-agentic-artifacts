import uuid
from datetime import datetime
from typing import Dict, Any, List

class Member:
    def __init__(self, name: str, email: str):
        self.member_id: str = str(uuid.uuid4())
        self.name: str = name
        self.email: str = email
        self.joined_date: str = datetime.now().isoformat()
        
        # Tracking member activity
        self.borrowed_book_ids: List[str] = []
        self.accumulated_fines: float = 0.0

    def borrow_book(self, book_id: str) -> None:
        if len(self.borrowed_book_ids) >= 5:
            raise ValueError(f"Member {self.name} has reached the maximum borrowing limit.")
        self.borrowed_book_ids.append(book_id)

    def return_book(self, book_id: str) -> None:
        if book_id in self.borrowed_book_ids:
            self.borrowed_book_ids.remove(book_id)

    def add_fine(self, amount: float) -> None:
        if amount > 0:
            self.accumulated_fines += amount

    def pay_fine(self, amount: float) -> float:
        """Pays off fines and returns any change if overpaid."""
        if amount >= self.accumulated_fines:
            change = amount - self.accumulated_fines
            self.accumulated_fines = 0.0
            return change
        
        self.accumulated_fines -= amount
        return 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "member_id": self.member_id,
            "name": self.name,
            "email": self.email,
            "borrowed_book_ids": self.borrowed_book_ids,
            "accumulated_fines": self.accumulated_fines
        }