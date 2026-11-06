from datetime import datetime

# Books: key = Book ID
books = {
    101: {
        "title": "Python Programming",
        "author": "John Smith",
        "category": "Programming",
        "total": 5,
        "available": 5
    },
    102: {
        "title": "Data Science Basics",
        "author": "David Miller",
        "category": "Technology",
        "total": 3,
        "available": 3
    },
    103: {
        "title": "Database Management",
        "author": "Robert Brown",
        "category": "Database",
        "total": 4,
        "available": 4
    }
}

# Members: key = Member ID
members = {
    1: {
        "name": "Aarav Sharma",
        "phone": "9876543210",
        "email": "aarav@gmail.com"
    },
    2: {
        "name": "Meera Kapoor",
        "phone": "9876543211",
        "email": "meera@gmail.com"
    },
    3: {
        "name": "Rahul Verma",
        "phone": "9876543212",
        "email": "rahul@gmail.com"
    }
}

# Transactions: key = Transaction ID (starts empty)
# Each value: {"book_id", "member_id", "issue_date", "return_date", "status"}
transactions = {}

print("Library database loaded.")
print(f"Books: {len(books)} | Members: {len(members)} | Transactions: {len(transactions)}")


def get_int(prompt):
    """Read a whole number safely. Returns None if the input is not a number."""
    try:
        return int(input(prompt).strip())
    except ValueError:
        print("Invalid input! Please enter a numeric value.")
        return None


def get_text(prompt):
    """Read text and remove leading/trailing spaces."""
    return input(prompt).strip()


def is_valid_email(email):
    """Check that an email contains one @ and a valid-looking domain, e.g. name@gmail.com."""
    if " " in email or email.count("@") != 1:
        return False
    local_part, domain = email.split("@")
    if local_part == "" or "." not in domain:
        return False
    if domain.startswith(".") or domain.endswith(".") or ".." in domain:
        return False
    return True


def show_book(book_id):
    book = books[book_id]
    print(f"Book ID: {book_id}")
    print(f"Title: {book['title']}")
    print(f"Author: {book['author']}")
    print(f"Category: {book['category']}")
    print(f"Total Copies: {book['total']}")
    print(f"Available Copies: {book['available']}")
    print("-" * 32)


def show_member(member_id):
    member = members[member_id]
    print(f"Member ID: {member_id}")
    print(f"Name: {member['name']}")
    print(f"Phone: {member['phone']}")
    print(f"Email: {member['email']}")
    print("-" * 32)


def show_transaction(txn_id):
    txn = transactions[txn_id]
    # .get() protects against a book or member that no longer exists
    title = books.get(txn["book_id"], {}).get("title", "[Book deleted]")
    name = members.get(txn["member_id"], {}).get("name", "[Member not found]")
    print(f"Transaction ID: {txn_id}")
    print(f"Book: {title} (ID {txn['book_id']})")
    print(f"Member: {name} (ID {txn['member_id']})")
    print(f"Issue Date: {txn['issue_date']}")
    print(f"Return Date: {txn['return_date'] if txn['return_date'] else 'Not returned yet'}")
    print(f"Status: {txn['status']}")
    print("-" * 32)


def display_menu():
    print("\n========================================")
    print("       LIBRARY MANAGEMENT SYSTEM")
    print("========================================")
    print("1. Book Management")
    print("2. Member Management")
    print("3. Issue a Book")
    print("4. Return a Book")
    print("5. Search Books")
    print("6. Library Reports")
    print("7. Exit")
    print("========================================")


def add_book():
    print("\n--- Add New Book ---")
    book_id = get_int("Enter Book ID: ")
    if book_id is None:
        return
    if book_id <= 0:
        print("Book ID must be a positive number.")
        return
    if book_id in books:
        print(f"Book ID {book_id} already exists. Please use a unique Book ID.")
        return

    title = get_text("Enter Book Title: ")
    author = get_text("Enter Author Name: ")
    category = get_text("Enter Category: ")
    if title == "" or author == "" or category == "":
        print("Title, author and category cannot be empty. Book not added.")
        return

    copies = get_int("Enter Number of Copies: ")
    if copies is None:
        return
    if copies <= 0:
        print("Number of copies must be greater than zero. Book not added.")
        return

    books[book_id] = {
        "title": title,
        "author": author,
        "category": category,
        "total": copies,
        "available": copies      # all copies are available at the start
    }
    print(f"Book '{title}' added successfully with ID {book_id}.")


def view_books():
    print("\n--- All Books ---")
    if not books:
        print("No books in the library.")
        return
    for book_id in books:
        show_book(book_id)


def update_book():
    print("\n--- Update Book Details ---")
    book_id = get_int("Enter Book ID: ")
    if book_id is None:
        return
    if book_id not in books:
        print(f"Book ID {book_id} does not exist.")
        return

    book = books[book_id]
    show_book(book_id)
    print("What would you like to update?")
    print("1. Title")
    print("2. Author")
    print("3. Category")
    print("4. Total Copies")
    print("5. Cancel")
    option = get_int("Enter your option: ")

    if option in (1, 2, 3):
        field = {1: "title", 2: "author", 3: "category"}[option]
        new_value = get_text(f"Enter new {field}: ")
        if new_value == "":
            print(f"{field.capitalize()} cannot be empty. No changes made.")
        else:
            old_value = book[field]
            book[field] = new_value
            print(f"{field.capitalize()} updated from '{old_value}' to '{new_value}'.")
    elif option == 4:
        issued = book["total"] - book["available"]
        new_total = get_int(f"Enter new total copies (currently issued: {issued}): ")
        if new_total is None:
            return
        if new_total <= 0:
            print("Total copies must be greater than zero.")
        elif new_total < issued:
            print(f"Not allowed! {issued} copies are currently issued, "
                  f"so total copies cannot be less than {issued}.")
        else:
            book["total"] = new_total
            book["available"] = new_total - issued
            print(f"Total copies updated to {new_total}. Available copies: {book['available']}.")
    elif option == 5:
        print("Update cancelled.")
    elif option is not None:
        print("Invalid option! Please select between 1 and 5.")


def delete_book():
    print("\n--- Delete Book ---")
    book_id = get_int("Enter Book ID: ")
    if book_id is None:
        return
    if book_id not in books:
        print(f"Book ID {book_id} does not exist.")
        return

    book = books[book_id]
    issued = book["total"] - book["available"]
    if issued > 0:
        print(f"Cannot delete '{book['title']}'. {issued} copy/copies are currently issued.")
        return

    confirm = get_text(f"Are you sure you want to delete '{book['title']}'? (y/n): ").lower()
    if confirm == "y":
        removed = books.pop(book_id)
        print(f"Book '{removed['title']}' (ID {book_id}) deleted successfully.")
    else:
        print("Deletion cancelled.")


def book_management():
    while True:
        print("\n-------- BOOK MANAGEMENT --------")
        print("1. Add New Book")
        print("2. View All Books")
        print("3. Update Book Details")
        print("4. Delete Book")
        print("5. Back to Main Menu")
        choice = get_int("Enter your choice: ")

        if choice == 1:
            add_book()
        elif choice == 2:
            view_books()
        elif choice == 3:
            update_book()
        elif choice == 4:
            delete_book()
        elif choice == 5:
            break
        elif choice is not None:
            print("Invalid choice! Please select between 1 and 5.")


def register_member():
    print("\n--- Register New Member ---")
    member_id = get_int("Enter Member ID: ")
    if member_id is None:
        return
    if member_id <= 0:
        print("Member ID must be a positive number.")
        return
    if member_id in members:
        print(f"Member ID {member_id} already exists. Please use a unique Member ID.")
        return

    name = get_text("Enter Full Name: ")
    if name == "":
        print("Name cannot be empty. Member not registered.")
        return

    phone = get_text("Enter Phone Number (10 digits): ")
    if len(phone) != 10 or not phone.isdigit():
        print("Phone number must contain exactly 10 digits. Member not registered.")
        return

    email = get_text("Enter Email Address: ").lower()
    if not is_valid_email(email):
        print("Invalid email address (example: name@gmail.com). Member not registered.")
        return

    members[member_id] = {"name": name, "phone": phone, "email": email}
    print(f"Member '{name}' registered successfully with ID {member_id}.")


def view_members():
    print("\n--- All Members ---")
    if not members:
        print("No members registered.")
        return
    for member_id in members:
        show_member(member_id)


def search_member():
    print("\n--- Search Member ---")
    member_id = get_int("Enter Member ID: ")
    if member_id is None:
        return
    if member_id not in members:
        print(f"Member ID {member_id} is not registered.")
        return

    print("Member found:")
    show_member(member_id)
    holding = 0
    for txn in transactions.values():
        if txn["member_id"] == member_id and txn["status"] == "Issued":
            holding += 1
    print(f"Books currently issued to this member: {holding}")


def member_management():
    while True:
        print("\n-------- MEMBER MANAGEMENT --------")
        print("1. Register New Member")
        print("2. View All Members")
        print("3. Search Member")
        print("4. Back to Main Menu")
        choice = get_int("Enter your choice: ")

        if choice == 1:
            register_member()
        elif choice == 2:
            view_members()
        elif choice == 3:
            search_member()
        elif choice == 4:
            break
        elif choice is not None:
            print("Invalid choice! Please select between 1 and 4.")


def generate_transaction_id():
    if not transactions:
        return 1001
    return max(transactions.keys()) + 1


def issue_book():
    print("\n--- Issue a Book ---")
    book_id = get_int("Enter Book ID: ")
    if book_id is None:
        return
    if book_id not in books:
        print(f"Invalid Book ID! Book {book_id} does not exist.")
        return

    book = books[book_id]
    if book["available"] <= 0:
        print(f"Sorry, '{book['title']}' is not available. All {book['total']} copies are issued.")
        return

    member_id = get_int("Enter Member ID: ")
    if member_id is None:
        return
    if member_id not in members:
        print(f"Member ID {member_id} is not registered. Book cannot be issued.")
        return

    txn_id = generate_transaction_id()
    transactions[txn_id] = {
        "book_id": book_id,
        "member_id": member_id,
        "issue_date": datetime.now().strftime("%d-%m-%Y"),
        "return_date": None,
        "status": "Issued"
    }
    book["available"] -= 1

    print("\nBook Issued Successfully!")
    print(f"Transaction ID: {txn_id}")
    print(f"Book: {book['title']}")
    print(f"Member: {members[member_id]['name']}")
    print(f"Issue Date: {transactions[txn_id]['issue_date']}")
    print(f"Status: Issued")


def return_book():
    print("\n--- Return a Book ---")
    txn_id = get_int("Enter Transaction ID: ")
    if txn_id is None:
        return
    if txn_id not in transactions:
        print(f"Transaction ID {txn_id} does not exist.")
        return

    txn = transactions[txn_id]
    if txn["status"] == "Returned":
        print(f"This book was already returned on {txn['return_date']}. "
              f"A transaction cannot be returned twice.")
        return

    txn["status"] = "Returned"
    txn["return_date"] = datetime.now().strftime("%d-%m-%Y")

    book = books.get(txn["book_id"])
    if book is not None and book["available"] < book["total"]:
        book["available"] += 1

    title = book["title"] if book else "[Book deleted]"
    print("\nBook Returned Successfully!")
    print(f"Book: {title}")
    print(f"Member: {members.get(txn['member_id'], {}).get('name', '[Member not found]')}")
    print(f"Return Date: {txn['return_date']}")
    print(f"Status: Returned")


def search_books():
    while True:
        print("\n-------- SEARCH BOOKS --------")
        print("1. Search by Book ID")
        print("2. Search by Book Title")
        print("3. Search by Author")
        print("4. Search by Category")
        print("5. Back to Main Menu")
        choice = get_int("Enter your choice: ")

        if choice == 1:
            book_id = get_int("Enter Book ID: ")
            if book_id is None:
                continue
            if book_id in books:
                print("\nBook found:")
                show_book(book_id)
            else:
                print(f"No record found for Book ID {book_id}.")

        elif choice in (2, 3, 4):
            field = {2: "title", 3: "author", 4: "category"}[choice]
            keyword = get_text(f"Enter {field} to search: ").lower()
            if keyword == "":
                print("Search text cannot be empty.")
                continue
            matches = [book_id for book_id in books if keyword in books[book_id][field].lower()]
            if matches:
                print(f"\n{len(matches)} matching book(s) found:")
                for book_id in matches:
                    show_book(book_id)
            else:
                print(f"No record found for {field} '{keyword}'.")

        elif choice == 5:
            break
        elif choice is not None:
            print("Invalid choice! Please select between 1 and 5.")


def library_reports():
    while True:
        print("\n-------- LIBRARY REPORTS --------")
        print("1. Total Books in Library")
        print("2. Total Book Copies")
        print("3. Available Book Copies")
        print("4. Currently Issued Books")
        print("5. Total Registered Members")
        print("6. Transaction History")
        print("7. Back to Main Menu")
        choice = get_int("Enter your choice: ")

        if choice == 1:
            print(f"\nTotal unique book titles in library: {len(books)}")

        elif choice == 2:
            total_copies = 0
            for book in books.values():
                total_copies += book["total"]
            print(f"\nTotal book copies (all titles): {total_copies}")

        elif choice == 3:
            available_copies = 0
            for book in books.values():
                available_copies += book["available"]
            print(f"\nAvailable book copies: {available_copies}")

        elif choice == 4:
            print("\n--- Currently Issued Books ---")
            issued_count = 0
            for txn_id, txn in transactions.items():
                if txn["status"] == "Issued":
                    show_transaction(txn_id)
                    issued_count += 1
            if issued_count == 0:
                print("No books are currently issued.")
            else:
                print(f"Total currently issued: {issued_count}")

        elif choice == 5:
            print(f"\nTotal registered members: {len(members)}")

        elif choice == 6:
            print("\n--- Transaction History ---")
            if not transactions:
                print("No transactions recorded yet.")
            else:
                for txn_id in transactions:
                    show_transaction(txn_id)
                print(f"Total transactions: {len(transactions)}")

        elif choice == 7:
            break
        elif choice is not None:
            print("Invalid choice! Please select between 1 and 7.")


def main():
    while True:
        display_menu()
        try:
            choice = int(input("Enter your choice: "))
            if choice == 1:
                book_management()
            elif choice == 2:
                member_management()
            elif choice == 3:
                issue_book()
            elif choice == 4:
                return_book()
            elif choice == 5:
                search_books()
            elif choice == 6:
                library_reports()
            elif choice == 7:
                print("Thank you for using Library Management System!")
                break
            else:
                print("Invalid choice! Please select between 1 and 7.")
        except ValueError:
            print("Please enter a valid numeric choice.")


main()
