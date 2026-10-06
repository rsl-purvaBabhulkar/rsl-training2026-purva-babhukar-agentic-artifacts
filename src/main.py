from models.book import Book
from models.member import Member
from services.library_manager import LibraryManager
from reports.formatter import generate_inventory_report, generate_financial_report

def main() -> None:
    """Runs the interactive command-line library menu until the user exits."""
    # 1. Initialize the system[cite: 1]
    library = LibraryManager()

    # 2. Add some data[cite: 1]
    book1 = Book("Odyssey", "Homer", 750)
    book2 = Book("Dune", "Frank Herbert", 1965)
    book3 = Book("Harry Potter and The Half Blood Prince", "J.K. Rowling", 2005)
    book4 = Book("1984", "George Orwell", 1949)

    library.add_book(book1)
    library.add_book(book2)
    library.add_book(book3)
    library.add_book(book4)

    # Feel free to add your own name
    member1 = Member("Kavin Mehta", "mehtaKavin@rsl.com")
    member2 = Member("Sameer Karoshi", "karoshiSameer@rsl.com")
    member3 = Member("Michael Scott", "scottMichael@rsl.com")

    library.register_member(member1)
    library.register_member(member2)
    library.register_member(member3)

    # Convert dictionary values to lists for easy indexing in the CLI
    members_list = list(library.members.values())
    books_list = list(library.books.values())

    # 3. Interactive CLI Flow
    while True:
        print("\n--- Library System Menu ---")
        print("1. Borrow a Book")
        print("2. Return a Book")
        print("3. Generate Reports")
        print("4. Exit")

        choice = input("\nSelect an option (1-4): ")

        if choice == '1':
            print("\n--- Select Member ---")
            for i, m in enumerate(members_list):
                print(f"{i + 1}. {m.name}")

            try:
                m_idx = int(input("Member number: ")) - 1
                member = members_list[m_idx]

                print("\n--- Available Books ---")
                # Filter out books that are already borrowed[cite: 5]
                available_books = [b for b in books_list if not b.is_borrowed]
                if not available_books:
                    print("No books available to borrow.")
                    continue

                for i, b in enumerate(available_books):
                    print(f"{i + 1}. {b.title}")

                b_idx = int(input("Book number: ")) - 1
                book = available_books[b_idx]

                # Process checkout[cite: 3]
                library.checkout_book(member.member_id, book.book_id)
                print(f"\nSuccess! '{book.title}' checked out to {member.name}.")

            except (ValueError, IndexError):
                print("\nInvalid selection. Please enter a valid number.")
            except PermissionError as e:
                # Catch fine limits (fines > ₹250.00)[cite: 3]
                print(f"\nError: {e}")

        elif choice == '2':
            print("\n--- Select Member ---")
            for i, m in enumerate(members_list):
                print(f"{i + 1}. {m.name}")

            try:
                m_idx = int(input("Member number: ")) - 1
                member = members_list[m_idx]

                if not member.borrowed_book_ids:
                    print(f"\n{member.name} has no borrowed books.")
                    continue

                print(f"\n--- Books borrowed by {member.name} ---")
                borrowed_books = [library.books[bid] for bid in member.borrowed_book_ids]
                for i, b in enumerate(borrowed_books):
                    print(f"{i + 1}. {b.title}")

                b_idx = int(input("Book number to return: ")) - 1
                book = borrowed_books[b_idx]

                # Optional testing flow to trigger the daily fine logic[cite: 3]
                is_late = input("Simulate a late return to trigger a fine? (y/n): ")
                if is_late.lower() == 'y':
                    book.due_date = "2020-01-01T12:00:00"

                library.process_return(member.member_id, book.book_id)
                print(f"\nSuccess! '{book.title}' returned by {member.name}.")

            except (ValueError, IndexError, KeyError):
                print("\nInvalid selection.")

        elif choice == '3':
            # 4. Generate Reports[cite: 1]
            print("\n")
            print(generate_inventory_report(books_list))
            print("\n")
            print(generate_financial_report(members_list))

        elif choice == '4':
            print("\nExiting library system. Goodbye!")
            break

        else:
            print("\nInvalid option. Please choose 1-4.")

if __name__ == "__main__":
    main()
