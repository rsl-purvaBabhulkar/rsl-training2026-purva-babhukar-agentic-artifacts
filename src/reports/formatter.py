from typing import List, Dict
from models.book import Book
from models.member import Member


def generate_overdue_report(overdue_loans: List[Dict[str, object]]) -> str:
    """Formats a list of overdue loans into a human-readable report.

    Args:
        overdue_loans: list of dicts with keys "book" (Book) and
            "member" (Member), e.g. as produced by
            LibraryManager.get_overdue_loans(). This function does not
            decide what counts as overdue — it only formats what it's given.

    Returns:
        A formatted report string. Never raises; an empty list of loans
        produces a "nothing overdue" message instead of an error.
    """
    lines = ["Overdue Books Report", "=" * 24]

    if not overdue_loans:
        lines.append("No books are currently overdue.")
        return "\n".join(lines)

    for loan in overdue_loans:
        book = loan["book"]
        member = loan["member"]
        lines.append(f"{book.title} — held by {member.name} ({member.email})")
        lines.append(f"    -> Due: {book.due_date[:10]}")

    return "\n".join(lines)


def generate_member_loan_counts_report(members: List[Member]) -> str:
    """Reports how many books each member currently has checked out.

    Args:
        members: list of Member objects, typically library.members.values().

    Returns:
        A formatted report string. Never raises; an empty member list
        produces a "nothing to report" message instead of an error.
    """
    lines = ["Member Loan Counts Report", "=" * 24]

    if not members:
        lines.append("No members registered.")
        return "\n".join(lines)

    for member in members:
        count = len(member.borrowed_book_ids)
        lines.append(f"{member.name}: {count} book(s) currently borrowed")

    return "\n".join(lines)

def generate_inventory_report(books: List[Book]) -> str:
    lines = ["Library Inventory Report", "=" * 24]
    
    for book in books:
        status = "Borrowed" if book.is_borrowed else "Available"
        lines.append(f"[{status}] {book.title} by {book.author} ({book.year_published})")
        if book.is_borrowed:
            lines.append(f"    -> Due: {book.due_date[:10]}")
            
    return "\n".join(lines)

def generate_financial_report(members: List[Member]) -> str:
    lines = ["Outstanding Fines Report", "=" * 24]
    total_fines = 0.0
    
    for member in members:
        if member.accumulated_fines > 0:
            lines.append(f"{member.name} ({member.email}): ₹{member.accumulated_fines:.2f}")
            total_fines += member.accumulated_fines
            
    lines.append("-" * 24)
    lines.append(f"Total Outstanding: ₹{total_fines:.2f}")
    return "\n".join(lines)
