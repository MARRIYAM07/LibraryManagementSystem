import json
import os
from datetime import datetime, timedelta

# File paths for data storage
BOOKS_FILE = 'books.json'
MEMBERS_FILE = 'members.json'
TRANSACTIONS_FILE = 'transactions.json'


# Initialize data files if they don't exist
def initialize_files():
    files = [BOOKS_FILE, MEMBERS_FILE, TRANSACTIONS_FILE]
    for file in files:
        if not os.path.exists(file):
            with open(file, 'w') as f:
                json.dump([], f)


# File handling functions
def load_data(filename):
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_data(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)


# Book Management Functions
def add_new_book():
    books = load_data(BOOKS_FILE)

    print("\n=== Add New Book ===")
    isbn = input("Enter ISBN: ")

    # Check if book already exists
    for book in books:
        if book['isbn'] == isbn:
            print("Book with this ISBN already exists!")
            return

    title = input("Enter Title: ")
    author = input("Enter Author: ")
    category = input("Enter Category: ")
    copies = int(input("Enter number of copies: "))

    new_book = {
        'isbn': isbn,
        'title': title,
        'author': author,
        'category': category,
        'total_copies': copies,
        'available_copies': copies
    }

    books.append(new_book)
    save_data(BOOKS_FILE, books)
    print("Book added successfully!")


def update_book_details():
    books = load_data(BOOKS_FILE)

    print("\n=== Update Book Details ===")
    isbn = input("Enter ISBN of book to update: ")

    for i, book in enumerate(books):
        if book['isbn'] == isbn:
            print(f"Current details: {book}")

            title = input(f"Enter new title (current: {book['title']}): ") or book['title']
            author = input(f"Enter new author (current: {book['author']}): ") or book['author']
            category = input(f"Enter new category (current: {book['category']}): ") or book['category']
            total_copies = input(f"Enter new total copies (current: {book['total_copies']}): ")

            if total_copies:
                total_copies = int(total_copies)
                # Adjust available copies based on the difference
                difference = total_copies - book['total_copies']
                available_copies = book['available_copies'] + difference
            else:
                total_copies = book['total_copies']
                available_copies = book['available_copies']

            books[i] = {
                'isbn': isbn,
                'title': title,
                'author': author,
                'category': category,
                'total_copies': total_copies,
                'available_copies': max(0, available_copies)
            }

            save_data(BOOKS_FILE, books)
            print("Book updated successfully!")
            return

    print("Book not found!")


def remove_book():
    books = load_data(BOOKS_FILE)
    transactions = load_data(TRANSACTIONS_FILE)

    print("\n=== Remove Book ===")
    isbn = input("Enter ISBN of book to remove: ")

    # Check if book is currently issued
    for transaction in transactions:
        if transaction['isbn'] == isbn and transaction['status'] == 'issued':
            print("Cannot remove book. It is currently issued to members.")
            return

    for i, book in enumerate(books):
        if book['isbn'] == isbn:
            books.pop(i)
            save_data(BOOKS_FILE, books)
            print("Book removed successfully!")
            return

    print("Book not found!")


def view_all_books():
    books = load_data(BOOKS_FILE)

    print("\n=== All Books ===")
    if not books:
        print("No books found!")
        return

    print(f"{'ISBN':<15} {'Title':<30} {'Author':<20} {'Category':<15} {'Total':<8} {'Available':<10}")
    print("-" * 100)

    for book in books:
        print(f"{book['isbn']:<15} {book['title'][:29]:<30} {book['author'][:19]:<20} "
              f"{book['category']:<15} {book['total_copies']:<8} {book['available_copies']:<10}")


# Member Management Functions
def register_new_member():
    members = load_data(MEMBERS_FILE)

    print("\n=== Register New Member ===")
    member_id = input("Enter Member ID: ")

    # Check if member already exists
    for member in members:
        if member['member_id'] == member_id:
            print("Member with this ID already exists!")
            return

    name = input("Enter Name: ")
    email = input("Enter Email: ")
    phone = input("Enter Phone: ")
    address = input("Enter Address: ")

    new_member = {
        'member_id': member_id,
        'name': name,
        'email': email,
        'phone': phone,
        'address': address,
        'registration_date': datetime.now().strftime("%Y-%m-%d"),
        'status': 'active'
    }

    members.append(new_member)
    save_data(MEMBERS_FILE, members)
    print("Member registered successfully!")


def update_member_details():
    members = load_data(MEMBERS_FILE)

    print("\n=== Update Member Details ===")
    member_id = input("Enter Member ID to update: ")

    for i, member in enumerate(members):
        if member['member_id'] == member_id:
            print(f"Current details: {member}")

            name = input(f"Enter new name (current: {member['name']}): ") or member['name']
            email = input(f"Enter new email (current: {member['email']}): ") or member['email']
            phone = input(f"Enter new phone (current: {member['phone']}): ") or member['phone']
            address = input(f"Enter new address (current: {member['address']}): ") or member['address']

            members[i]['name'] = name
            members[i]['email'] = email
            members[i]['phone'] = phone
            members[i]['address'] = address

            save_data(MEMBERS_FILE, members)
            print("Member updated successfully!")
            return

    print("Member not found!")


def deregister_member():
    members = load_data(MEMBERS_FILE)
    transactions = load_data(TRANSACTIONS_FILE)

    print("\n=== Deregister Member ===")
    member_id = input("Enter Member ID to deregister: ")

    # Check if member has any issued books
    for transaction in transactions:
        if transaction['member_id'] == member_id and transaction['status'] == 'issued':
            print("Cannot deregister member. They have issued books.")
            return

    for i, member in enumerate(members):
        if member['member_id'] == member_id:
            members[i]['status'] = 'deregistered'
            save_data(MEMBERS_FILE, members)
            print("Member deregistered successfully!")
            return

    print("Member not found!")


def view_all_members():
    members = load_data(MEMBERS_FILE)

    print("\n=== All Members ===")
    if not members:
        print("No members found!")
        return

    print(f"{'ID':<10} {'Name':<25} {'Email':<30} {'Phone':<15} {'Status':<12} {'Reg Date':<12}")
    print("-" * 110)

    for member in members:
        print(f"{member['member_id']:<10} {member['name'][:24]:<25} {member['email'][:29]:<30} "
              f"{member['phone']:<15} {member['status']:<12} {member['registration_date']:<12}")


# Issue/Return Functions
def issue_book():
    books = load_data(BOOKS_FILE)
    members = load_data(MEMBERS_FILE)
    transactions = load_data(TRANSACTIONS_FILE)

    print("\n=== Issue Book ===")
    member_id = input("Enter Member ID: ")
    isbn = input("Enter Book ISBN: ")

    # Check if member exists and is active
    member_found = False
    for member in members:
        if member['member_id'] == member_id and member['status'] == 'active':
            member_found = True
            break

    if not member_found:
        print("Member not found or inactive!")
        return

    # Check if book exists and is available
    book_found = False
    for i, book in enumerate(books):
        if book['isbn'] == isbn:
            if book['available_copies'] > 0:
                book_found = True
                # Update available copies
                books[i]['available_copies'] -= 1
                break
            else:
                print("Book not available!")
                return

    if not book_found:
        print("Book not found!")
        return

    # Create transaction record
    issue_date = datetime.now().strftime("%Y-%m-%d")
    due_date = (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d")

    transaction = {
        'transaction_id': len(transactions) + 1,
        'member_id': member_id,
        'isbn': isbn,
        'issue_date': issue_date,
        'due_date': due_date,
        'return_date': None,
        'status': 'issued',
        'fine': 0
    }

    transactions.append(transaction)
    save_data(BOOKS_FILE, books)
    save_data(TRANSACTIONS_FILE, transactions)
    print(f"Book issued successfully! Due date: {due_date}")


def return_book():
    books = load_data(BOOKS_FILE)
    transactions = load_data(TRANSACTIONS_FILE)

    print("\n=== Return Book ===")
    member_id = input("Enter Member ID: ")
    isbn = input("Enter Book ISBN: ")

    # Find the issued transaction
    for i, transaction in enumerate(transactions):
        if (transaction['member_id'] == member_id and
                transaction['isbn'] == isbn and
                transaction['status'] == 'issued'):

            return_date = datetime.now().strftime("%Y-%m-%d")
            due_date = datetime.strptime(transaction['due_date'], "%Y-%m-%d")
            return_date_obj = datetime.strptime(return_date, "%Y-%m-%d")

            # Calculate fine if overdue
            fine = 0
            if return_date_obj > due_date:
                days_overdue = (return_date_obj - due_date).days
                fine = days_overdue * 2  # $2 per day fine

            # Update transaction
            transactions[i]['return_date'] = return_date
            transactions[i]['status'] = 'returned'
            transactions[i]['fine'] = fine

            # Update book availability
            for j, book in enumerate(books):
                if book['isbn'] == isbn:
                    books[j]['available_copies'] += 1
                    break

            save_data(BOOKS_FILE, books)
            save_data(TRANSACTIONS_FILE, transactions)

            if fine > 0:
                print(f"Book returned successfully! Fine: ${fine}")
            else:
                print("Book returned successfully!")
            return

    print("No issued book found for this member and ISBN!")


def view_issued_books():
    transactions = load_data(TRANSACTIONS_FILE)
    books = load_data(BOOKS_FILE)
    members = load_data(MEMBERS_FILE)

    print("\n=== Currently Issued Books ===")
    issued_transactions = [t for t in transactions if t['status'] == 'issued']

    if not issued_transactions:
        print("No books currently issued!")
        return

    print(f"{'Member ID':<12} {'Member Name':<25} {'ISBN':<15} {'Book Title':<30} {'Issue Date':<12} {'Due Date':<12}")
    print("-" * 120)

    for transaction in issued_transactions:
        # Get member name
        member_name = "Unknown"
        for member in members:
            if member['member_id'] == transaction['member_id']:
                member_name = member['name']
                break

        # Get book title
        book_title = "Unknown"
        for book in books:
            if book['isbn'] == transaction['isbn']:
                book_title = book['title']
                break

        print(f"{transaction['member_id']:<12} {member_name[:24]:<25} {transaction['isbn']:<15} "
              f"{book_title[:29]:<30} {transaction['issue_date']:<12} {transaction['due_date']:<12}")


# Search Functions
def search_by_title():
    books = load_data(BOOKS_FILE)

    print("\n=== Search by Title ===")
    title = input("Enter title to search: ").lower()

    found_books = [book for book in books if title in book['title'].lower()]

    if found_books:
        print(f"{'ISBN':<15} {'Title':<30} {'Author':<20} {'Available':<10}")
        print("-" * 75)
        for book in found_books:
            print(
                f"{book['isbn']:<15} {book['title'][:29]:<30} {book['author'][:19]:<20} {book['available_copies']:<10}")
    else:
        print("No books found!")


def search_by_author():
    books = load_data(BOOKS_FILE)

    print("\n=== Search by Author ===")
    author = input("Enter author to search: ").lower()

    found_books = [book for book in books if author in book['author'].lower()]

    if found_books:
        print(f"{'ISBN':<15} {'Title':<30} {'Author':<20} {'Available':<10}")
        print("-" * 75)
        for book in found_books:
            print(
                f"{book['isbn']:<15} {book['title'][:29]:<30} {book['author'][:19]:<20} {book['available_copies']:<10}")
    else:
        print("No books found!")


def search_by_isbn():
    books = load_data(BOOKS_FILE)

    print("\n=== Search by ISBN ===")
    isbn = input("Enter ISBN to search: ")

    for book in books:
        if book['isbn'] == isbn:
            print(f"ISBN: {book['isbn']}")
            print(f"Title: {book['title']}")
            print(f"Author: {book['author']}")
            print(f"Category: {book['category']}")
            print(f"Total Copies: {book['total_copies']}")
            print(f"Available Copies: {book['available_copies']}")
            return

    print("Book not found!")


def search_by_category():
    books = load_data(BOOKS_FILE)

    print("\n=== Search by Category ===")
    category = input("Enter category to search: ").lower()

    found_books = [book for book in books if category in book['category'].lower()]

    if found_books:
        print(f"{'ISBN':<15} {'Title':<30} {'Author':<20} {'Available':<10}")
        print("-" * 75)
        for book in found_books:
            print(
                f"{book['isbn']:<15} {book['title'][:29]:<30} {book['author'][:19]:<20} {book['available_copies']:<10}")
    else:
        print("No books found!")


# Report Functions
def issued_books_report():
    view_issued_books()


def fines_report():
    transactions = load_data(TRANSACTIONS_FILE)
    members = load_data(MEMBERS_FILE)

    print("\n=== Fines Report ===")
    fined_transactions = [t for t in transactions if t['fine'] > 0]

    if not fined_transactions:
        print("No fines recorded!")
        return

    print(f"{'Member ID':<12} {'Member Name':<25} {'ISBN':<15} {'Fine Amount':<12} {'Return Date':<12}")
    print("-" * 85)

    total_fines = 0
    for transaction in fined_transactions:
        # Get member name
        member_name = "Unknown"
        for member in members:
            if member['member_id'] == transaction['member_id']:
                member_name = member['name']
                break

        print(f"{transaction['member_id']:<12} {member_name[:24]:<25} {transaction['isbn']:<15} "
              f"${transaction['fine']:<11} {transaction['return_date']:<12}")
        total_fines += transaction['fine']

    print("-" * 85)
    print(f"Total Fines Collected: ${total_fines}")


def member_activity_report():
    transactions = load_data(TRANSACTIONS_FILE)
    members = load_data(MEMBERS_FILE)

    print("\n=== Member Activity Report ===")

    # Count transactions per member
    member_activity = {}
    for transaction in transactions:
        member_id = transaction['member_id']
        if member_id not in member_activity:
            member_activity[member_id] = {'issued': 0, 'returned': 0, 'fines': 0}

        if transaction['status'] == 'issued':
            member_activity[member_id]['issued'] += 1
        elif transaction['status'] == 'returned':
            member_activity[member_id]['returned'] += 1
            member_activity[member_id]['fines'] += transaction['fine']

    if not member_activity:
        print("No member activity found!")
        return

    print(f"{'Member ID':<12} {'Member Name':<25} {'Books Issued':<13} {'Books Returned':<15} {'Total Fines':<12}")
    print("-" * 85)

    for member_id, activity in member_activity.items():
        # Get member name
        member_name = "Unknown"
        for member in members:
            if member['member_id'] == member_id:
                member_name = member['name']
                break

        print(f"{member_id:<12} {member_name[:24]:<25} {activity['issued']:<13} "
              f"{activity['returned']:<15} ${activity['fines']:<11}")


def inventory_report():
    books = load_data(BOOKS_FILE)

    print("\n=== Inventory Report ===")
    if not books:
        print("No books in inventory!")
        return

    total_books = sum(book['total_copies'] for book in books)
    available_books = sum(book['available_copies'] for book in books)
    issued_books = total_books - available_books

    print(f"Total Books in Library: {total_books}")
    print(f"Available Books: {available_books}")
    print(f"Currently Issued: {issued_books}")
    print(f"Total Book Titles: {len(books)}")

    print(f"\n{'Category':<20} {'Total Books':<12} {'Available':<10} {'Issued':<8}")
    print("-" * 50)

    # Group by category
    categories = {}
    for book in books:
        cat = book['category']
        if cat not in categories:
            categories[cat] = {'total': 0, 'available': 0}
        categories[cat]['total'] += book['total_copies']
        categories[cat]['available'] += book['available_copies']

    for category, data in categories.items():
        issued = data['total'] - data['available']
        print(f"{category:<20} {data['total']:<12} {data['available']:<10} {issued:<8}")


# Menu Functions
def display_menu():
    print("\n=== Library Management System ===")
    print("1. Book Management")
    print("2. Member Management")
    print("3. Issue/Return Book")
    print("4. Search Books")
    print("5. Reports")
    print("6. Exit")


def book_management_menu():
    while True:
        print("\n=== Book Management ===")
        print("1. Add New Book")
        print("2. Update Book Details")
        print("3. Remove Book")
        print("4. View All Books")
        print("5. Back to Main Menu")

        choice = input("Enter your choice: ")

        if choice == '1':
            add_new_book()
        elif choice == '2':
            update_book_details()
        elif choice == '3':
            remove_book()
        elif choice == '4':
            view_all_books()
        elif choice == '5':
            break
        else:
            print("Invalid choice. Please try again.")


def member_management_menu():
    while True:
        print("\n=== Member Management ===")
        print("1. Register New Member")
        print("2. Update Member Details")
        print("3. Deregister Member")
        print("4. View All Members")
        print("5. Back to Main Menu")

        choice = input("Enter your choice: ")

        if choice == '1':
            register_new_member()
        elif choice == '2':
            update_member_details()
        elif choice == '3':
            deregister_member()
        elif choice == '4':
            view_all_members()
        elif choice == '5':
            break
        else:
            print("Invalid choice. Please try again.")


def issue_return_menu():
    while True:
        print("\n=== Issue/Return Book ===")
        print("1. Issue Book")
        print("2. Return Book")
        print("3. View Issued Books")
        print("4. Back to Main Menu")

        choice = input("Enter your choice: ")

        if choice == '1':
            issue_book()
        elif choice == '2':
            return_book()
        elif choice == '3':
            view_issued_books()
        elif choice == '4':
            break
        else:
            print("Invalid choice. Please try again.")


def search_books_menu():
    while True:
        print("\n=== Search Books ===")
        print("1. Search by Title")
        print("2. Search by Author")
        print("3. Search by ISBN")
        print("4. Search by Category")
        print("5. Back to Main Menu")

        choice = input("Enter your choice: ")

        if choice == '1':
            search_by_title()
        elif choice == '2':
            search_by_author()
        elif choice == '3':
            search_by_isbn()
        elif choice == '4':
            search_by_category()
        elif choice == '5':
            break
        else:
            print("Invalid choice. Please try again.")


def reports_menu():
    while True:
        print("\n=== Reports ===")
        print("1. Issued Books Report")
        print("2. Fines Report")
        print("3. Member Activity Report")
        print("4. Inventory Report")
        print("5. Back to Main Menu")

        choice = input("Enter your choice: ")

        if choice == '1':
            issued_books_report()
        elif choice == '2':
            fines_report()
        elif choice == '3':
            member_activity_report()
        elif choice == '4':
            inventory_report()
        elif choice == '5':
            break
        else:
            print("Invalid choice. Please try again.")


def main():
    # Initialize data files
    initialize_files()

    while True:
        display_menu()
        choice = input("Enter your choice: ")

        if choice == '1':
            book_management_menu()
        elif choice == '2':
            member_management_menu()
        elif choice == '3':
            issue_return_menu()
        elif choice == '4':
            search_books_menu()
        elif choice == '5':
            reports_menu()
        elif choice == '6':
            print("Exiting the system. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()