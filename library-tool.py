# Import requests library so I can talk to the API
import requests
# Hello sys. Useful for CLI stuff
import sys 

# Define constants
API_KEY = "fbDo38Joogrf8-In0vjcVb5dCK0yuhZL5M06GM1A"
BASE_ID = "pov40kx5cdtfqty"

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
    print("Available tables:")
    for name in TABLE_IDS.keys():
        print(f"  - {name.lower()}")
    sys.exit(0)

# Logic for using python library-tool.py <table>
elif len(sys.argv) == 2:
    table_key = sys.argv[1].upper()
    list_fields(table_key)
    sys.exit(0)

else:
    print("Error: Unknown command.")
    print_help()
    sys.exit(1)

