# Import requests library so I can talk to the API
import requests

# Hello sys. Useful for CLI stuff
import sys 

# Eyy privacy bro
from dotenv import load_dotenv
import os

load_dotenv()

# dotenv consts
API_KEY = os.getenv("API_KEY")
BASE_ID = os.getenv("BASE_ID")

# Table IDs yay
TABLE_IDS = {
    "BOOKS": "mth1bd75romp8p3",
    "AUTHORS": "mgd51sp0b93cu0y",
    "EDITIONS": "mdgeonaqlm8fjxd",
    "PUBLISHERS": "mqg3ii2ioil1bld",
    "ARTWORKS": "mp3s5cruo63kxvi",
    "REVIEWS": "mjr2am3o9mlpyo1",
}

# HTTP headers because yummy. Asks for JSON to be returned and does the auth
headers = {
    "accept": "application/json",
    "xc-token": API_KEY
}


def get_records(table_id_arg):
    '''Sends a GET request to the API. Takes a table ID as an argument and returns the record data or an error message'''

    table_id = table_id_arg

    # API GET URL
    url = f"http://127.0.0.1:8080/api/v2/tables/{table_id}/records"
    
    # Sends the GET request
    response = requests.get(url, headers=headers)

    # If the request succeeds (HTTP status 200), return list of records
    if response.status_code == 200:
        return response.json()["list"]

    # If request fails, print error and return empty list
    else:
        print("Error:", response.status_code, response.text)
        return []

def format_books(book):
    '''Formats book records cleanly. Takes a record from the Books table as an argument and prints the output nicely'''
    print(f"{book['Title']} ({book['First Published']})")
    print(f"   Author(s): {', '.join(book['Author(s)'])}")
    print(f"   Genre: {book.get('Genre', 'N/A').replace(',', ', ')}")
    print(f"   Tags: {book.get('Tags', 'N/A').replace(',', ', ')}")
    print(f"   Status: {book['Status']} | Rating: {book['Rating']}")
    print(f"   Owned: {'Yes' if book['Owned'] else 'No'} | Annotated: {'Yes' if book['Annotated'] else 'No'}")
    print("-" * 47)


def format_authors(author):
    '''Formats author records cleanly. Takes a record from the Authors table as an argument and prints the output nicely'''
    print(f"{author['Name']} ({author.get('Pronouns', 'N/A')})")
    print(f"  Website: {author.get('Website', 'N/A')}")
    print(f"  Notes: {author.get('Notes', '')}")
    print("-" * 47)

def format_editions(edition):
    '''Formats edition records cleanly. Takes a record from the Editions table as an argument and prints the output nicely.'''
    print(f"{edition['Title']} ({edition.get('Year', 'Unknown')})")
    print(f"  Book: {edition['Books'].get('Display Name', 'N/A')}")
    print(f"  Publisher: {edition.get('Publisher', 'N/A')} ({edition.get('City', 'N/A')})")
    print(f"  Language: {edition.get('Language', 'N/A')} | Pages: {edition.get('Pages', 'N/A')}")
    print(f"  ISBN: {edition.get('ISBN', 'N/A')}")
    citation = edition.get('Citation (Cite Them Right)', 'N/A')
    if citation and citation.strip():
        print(f"  Citation: {citation}")
    if edition.get('Notes'):
        print(f"  Notes: {edition['Notes']}")
    print("-" * 47)

def format_publishers(publisher):
    '''Formats publisher records cleanly.'''
    print(f"{publisher['Publisher']} ({publisher.get('Countries', 'N/A')})")
    if publisher.get('Imprint Of'):
        print(f"  Imprint of: {publisher['Imprint Of']}")
    if publisher.get('Website'):
        print(f"  Website: {publisher['Website']}")
    if publisher.get('Notes'):
        print(f"  Notes: {publisher['Notes']}")
    print(f"  Editions Published: {publisher.get('Editions', 0)}")
    print("-" * 47)

def format_artworks(artwork):
    '''Formats artwork records cleanly.'''
    title = artwork.get('Title', 'Untitled')
    print(f"{title}")
    print(f"  Medium: {artwork.get('Medium', 'Unknown')} | Date: {artwork.get('Date', 'Unknown')}")
    if artwork.get('Books') and artwork['Books'].get('Display Name'):
        print(f"  Related to: {artwork['Books']['Display Name']}")
    else:
        print("  Related to: None")
    print("-" * 47)

def format_reviews(review):
    '''Formats review records cleanly.'''
    title = review.get('Title', 'Untitled Review')
    print(f"{title}")
    if review.get('Books') and review['Books'].get('Display Name'):
        print(f"  Book: {review['Books']['Display Name']}")
    else:
        print("  Book: None")
    print(f"  Date: {review.get('Review Date', 'Unknown')}")
    print(f"  Location: {review.get('Reviewed For', 'Private')} | Published In: {review.get('Published In', 'N/A')}")
    if review.get('Review Path'):
        print(f"  Path: {review['Review Path']}")
    print("-" * 47)

FORMATTERS = {
    "BOOKS": format_books,
    "AUTHORS": format_authors,
    "EDITIONS": format_editions,
    "PUBLISHERS": format_publishers,
    "ARTWORKS": format_artworks,
    "REVIEWS": format_reviews,
}

def find_empty_fields(table_key, field_name, formatter):
    '''Finds records with a specific empty field. Takes the table ID and the field name as arguments and returns the matching records'''
    # Find table ID
    table_id = TABLE_IDS.get(table_key.upper())
    
    # Table not found contingency
    if not table_id:
        print("Table not found.")
        return

    # Fetch data from the specified table
    records = get_records(table_id)
    print(f"Records with empty '{field_name}' in {table_key}:")
    print("-" * 47)

    # Check for records with empty specified field
    for record in records:
        value = record.get(field_name)
        if not value or (isinstance(value, str) and not value.strip()):
            formatter(record)

def list_fields(table_key):
    '''Prints all field names for a table by inspecting the first record. Takes table key as an argument'''
    
    table_id = TABLE_IDS.get(table_key.upper())

    # Contingency for if table is wrong
    if not table_id:
        print("Table not found.")
        return

    records = get_records(table_id)

    # Contingency for if there are no records in the table
    if not records:
        print("No records found.")
        return

    print(f"Fields for {table_key.upper()}:")
    for field in records[0].keys():
        print(field)

def list_author_works(author_name):
    author_id = None

    # Find matching author ID
    authors = get_records(TABLE_IDS["AUTHORS"])
    for author in authors:
        if author['Name'].lower() == author_name.lower():
            author_id = author['Id']
            break
    if not author_id:
        print("Author not found.")
        return

    # Fetch the books
    books = get_records(TABLE_IDS["BOOKS"])
    print(f"Books by {author_name}: ")
    print("-" * 47)
    found = False
    for book in books:
        rels = book.get("nc_7ok3___nc_m2m_Books_Authors", [])
        for relation in rels:
            if relation.get("Authors", {}).get("Id") == author_id:
                format_books(book)
                found = True
                break

    if not found:
        print("No books found from this author.")

def print_valid_tables():
    print("Available tables: ")
    for name in TABLE_IDS.keys():
        print(name)

def resolve_key_case(target_dict, input_key):
    for key in target_dict:
        if key.lower() == input_key.lower():
            return key
    return None


def search_records(term, table_key, fields="Title"):
    '''Searches for a term in one or more fields of a table. Takes arguments: search term, table key, and a single field or list of fields.'''

    table_id = TABLE_IDS.get(table_key.upper())
    if not table_id:
        print("Table not found.")
        print_valid_tables()
        print_help()
        return

    # Allow both strings and lists as field input
    if isinstance(fields, str):
        fields = [fields]

    records = get_records(table_id)
    found = False

    for record in records:
        for field in fields:
            real_field = resolve_key_case(record, field)
            if not real_field:
                continue

            # List and string logic
            raw_value = record.get(real_field, "")
            if isinstance(raw_value, list):
                match_string = ", ".join(map(str, raw_value)).lower()
            else:
                match_string = str(raw_value).lower()

            # print(f"Checking '{term.lower()}' in field '{real_field}': {match_string}")

            if term.lower() in match_string:
                formatter = FORMATTERS.get(table_key.upper(), lambda x: print(x))
                formatter(record)
                found = True
                break

    if not found:
        if len(fields) == 1:
            print(f"No matches found for '{term}' in {fields[0]} of {table_key}.")
        else:
            fields_joined = ", ".join(fields)
            print(f"No matches found for '{term}' in any of [{fields_joined}] of {table_key}.")
        
def list_book_editions(book_title):
    book_id = None
    books = get_records(TABLE_IDS["BOOKS"])

    for book in books:
        title = book.get("Title", "").lower()
        display = book.get("Display Name", "").lower()
        if book_title.lower() in (title, display):
            book_id = book['Id']
            book_display_name = book.get("Display Name", book.get("Title"))
            break

    if not book_id:
        print("Book not found.")
        return

    editions = get_records(TABLE_IDS["EDITIONS"])
    print(f"Editions of {book_display_name}:")
    print("-" * 47)
    found = False

    for edition in editions:
        if edition.get("Books", {}).get("Id") == book_id:
            format_editions(edition)
            found = True

    if not found:
        print("No editions found for this book.")

def search_vibe(search_term):
    search_records(search_term, "Books", ["Genre", "Tags"])

def print_help():
    '''Prints a help menu explaining all available commands'''
    print("-" * 47)
    print(r"""
 ____  _  _    __    __  ____  ____  __  ____ 
(  __)( \/ )  (  )  (  )(  _ \(  _ \(  )/ ___)
 ) _)  )  (   / (_/\ )(  ) _ ( )   / )( \___ \
(____)(_/\_)  \____/(__)(____/(__\_)(__)(____/
          """)
    print("-" * 47)
    print(r"""
Usage:

    python library-tool.py -g <table>
        Get and display all records from a specified table.

    python library-tool.py -e <table> <field>
        Find and display all records in a table where the specified field is empty.

    python library-tool.py <table>
        Show all available fields in the specified table. Useful for checking valid field names.

    python library-tool.py tables
        Show all available tables. Useful for checking valid table names.

    python library-tool.py -a <author>
        List all books by a given author

    python library-tool.py -s <term> <table> [field]
        Search for a term in a specific field of a table. Field is optional; defaults to 'Title'.

          """)

# I stole all this from chatgpt. Something something stealing is learning if you figure out what each line does

# Checks if you have actually included an argument. If not, prints help and exits with error code 1
if len(sys.argv) < 2:
    print_help()
    sys.exit(1)

# Grabs first argument and makes it lowercase
command = sys.argv[1].lower()

# Logic for using get_records()
if command in ("-g", "--get"):

    # Makes sure there is one argument after -g
    if len(sys.argv) != 3:
        print("Error: Please specify a table name.")
        print_help()
        sys.exit(1)

    # Grabs table arg, converts to uppercase, and looks up the corresp table ID
    table_key = sys.argv[2].upper()
    table_id = TABLE_IDS.get(table_key)

    # Contingency for user choosing non-existent table
    if not table_id:
        print("Invalid table name.")
        print_help()
        sys.exit(1)

    # Fetches data from database
    records = get_records(table_id)

    # Chooses the right format. If none exists, prints raw
    formatter = FORMATTERS.get(table_key, lambda x: print(x))

    # Formats each record
    for record in records:
        formatter(record)

# Logic for using find_empty_fields()
elif command in ("-e", "--empty"):
    if len(sys.argv) != 4:
        print("Error: Please specify a table and field name.")
        print_help()
        sys.exit(1)
    table_key = sys.argv[2].upper()
    field_name = sys.argv[3]
    formatter = FORMATTERS.get(table_key, lambda x: print(x))
    find_empty_fields(table_key, field_name, formatter)

# Logic for listing all valid tables
elif len(sys.argv) == 2 and sys.argv[1].lower() == "tables":
    print_valid_tables()
    sys.exit(0)

# Logic for using python library-tool.py <table>
elif len(sys.argv) == 2:
    table_key = sys.argv[1].upper()
    list_fields(table_key)
    sys.exit(0)

# Logic for using list_author_works()
elif command in ("-a", "--author-works"):
    if len(sys.argv) != 3:
        print("Error: Please specify an author name.")
        print_help()
        sys.exit(1)
    author_name = sys.argv[2]
    list_author_works(author_name)

# Logic for using search_records()
elif command in ("-s", "--search"):
    if len(sys.argv) < 4:
        print("Error: Please provide a search term and table name.")
        print_help()
        sys.exit(1)

    search_term = sys.argv[2]
    table_key = sys.argv[3]
    fields = sys.argv[4:] if len(sys.argv) > 4 else ["Title"]  # Default to Title

    search_records(search_term, table_key, fields)

# Logic for list_book_editions()
elif command in ("-b", "--book-editions"):
    if len(sys.argv) != 3:
        print("Error: Please specify a book title.")
        print_help()
        sys.exit(1)
    book_title = sys.argv[2]
    list_book_editions(book_title)

# Logic for search_vibe()
elif command in ("-v", "--vibe"):
    if len(sys.argv) != 3:
        print("Error: Please include a search term.")
        print_help()
        sys.exit(1)
    search_term = sys.argv[2]
    search_vibe(search_term)

# If you've got through everything else and it ain't right, you've done fugged up
else:
    print("Error: Unknown command.")
    print_help()
    sys.exit(1)

