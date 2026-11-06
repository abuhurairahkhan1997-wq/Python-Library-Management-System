# Library Management System (Python)

A menu-driven library system that runs in the console. A librarian can manage books, register members, issue and return books, search the catalogue and produce reports. It uses only core Python: no external libraries and no database.

> Project from my Python module on the Skill Versed Post Graduation in Data Analytics with Gen AI (batch PGDA0526).

## Features
| Module | What it does |
|---|---|
| Book management | Add, view, update and delete books |
| Member management | Register, view and search members (shows how many books each member holds) |
| Issue a book | Checks the book exists, has a copy available and the member is registered, then records today's date |
| Return a book | Updates availability and the return date, and blocks returning the same book twice |
| Search | By book ID, or a partial, case-insensitive match on title, author or category |
| Reports | Total titles, total and available copies, books currently issued, member count and full transaction history |

## Business rules it enforces
- Book and member IDs must be unique positive numbers, and copies must be greater than zero.
- Phone numbers must be exactly 10 digits, and emails must have a valid format.
- Total copies can't be set below the number currently issued.
- A book with copies on loan can't be deleted.
- Typing text where a number is expected shows an error message instead of crashing the program.

## Python concepts used
- **Dictionaries and nested dictionaries** to store books, members and transactions
- **Functions**: one per task, with small reusable helpers (`get_int`, `is_valid_email`, `show_book`)
- **`while` loops** for the main menu and each sub-menu
- **`try-except`** for safe number input
- **String methods** (`strip`, `lower`, `isdigit`, `split`) for validation and search
- **List comprehension** to collect search matches
- **`datetime`** for issue and return dates
- Every report figure is calculated from the live data, never hard-coded

## Example
```
--- Issue a Book ---
Enter Book ID: 101
Enter Member ID: 1

Book Issued Successfully!
Transaction ID: 1001
Book: Python Programming
Member: Aarav Sharma
Issue Date: 06-11-2026
Status: Issued
```
A full example session is in [`docs/sample_run.txt`](docs/sample_run.txt).

## Testing
All 16 test cases in the notebook passed, plus the four extra rules (copies below issued, deleting with copies on loan, phone and email checks). They cover duplicate IDs, issuing an unavailable book, invalid members, double returns, searches with no results, invalid menu options and text typed instead of numbers.

## How to run
**Google Colab:** open `Library_Management_System.ipynb` and choose **Runtime → Run all**. The last cell starts the menu.

**On your computer (Python 3):**
```
python library_management_system.py
```

## Files
| File | What it is |
|---|---|
| `Library_Management_System.ipynb` | Notebook with explanations for each step |
| `library_management_system.py` | The same code as a single script |
| `docs/sample_run.txt` | Example session output |

## Author
**Abuhurairah Rahman Pathan**, MSc Bioinformatics, University of Liverpool
[LinkedIn](https://www.linkedin.com/in/pathan-abuhurairah-rahman-1997-khan)
