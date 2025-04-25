# SET UP

# Import statements
import requests
import argparse
from dotenv import load_dotenv
import os
from formatters import *

load_dotenv()

# argparse parser
parser = argparse.ArgumentParser(
    description="CLI tool to manage and query your personal library database.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
subparsers = parser.add_subparsers(dest="command", required=True)

# GLOBAL CONSTANTS

# dotenv consts
API_KEY = os.getenv("API_KEY")
BASE_ID = os.getenv("BASE_ID")

# HTTP headers. Asks for JSON to be returned and does the auth
headers = {
    "accept": "application/json",
    "xc-token": API_KEY
}
# Table ID map
TABLE_IDS = {
    "BOOKS": "mth1bd75romp8p3",
    "AUTHORS": "mgd51sp0b93cu0y",
    "EDITIONS": "mdgeonaqlm8fjxd",
    "PUBLISHERS": "mqg3ii2ioil1bld",
    "ARTWORKS": "mp3s5cruo63kxvi",
    "REVIEWS": "mjr2am3o9mlpyo1",
}

# Type map for field filtering
TYPE_MAP = {
    str: "string",
    int: "integer",
    float: "float",
    bool: "boolean",
    list: "list",
    dict: "dict",
}

# Verbose/debug mode
parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output for debugging")

# Formatters table with the imported functions
FORMATTERS = {
    "BOOKS": format_books,
    "AUTHORS": format_authors,
    "EDITIONS": format_editions,
    "PUBLISHERS": format_publishers,
    "ARTWORKS": format_artworks,
    "REVIEWS": format_reviews,
}

# UTILITY FUNCTIONS

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

def print_valid_tables():
    '''Prints a list of all valid tables'''
    print("Available tables: ")
    for name in TABLE_IDS.keys():
        print(name)

def resolve_key_case(target_dict, input_key):
    '''Supports case insensitivity in other functions. Takes the arguments target dictionary and input key. Returns the key or nothing'''
    for key in target_dict:
        if key.lower() == input_key.lower():
            return key
    return None

def infer_field_type(table_key, field_name, override_type=None):
    '''Infers the type of data in a field. Override type can be passed manually.'''

    if override_type:
        return override_type

    records = get_records(TABLE_IDS[table_key.upper()])
    seen_values = set()

    for record in records:
        value = record.get(field_name)

        if value is None or value == "":
            continue

        # Early return for non-int/float types
        if isinstance(value, str):
            return str
        elif isinstance(value, float):
            return float
        elif isinstance(value, list):
            return list
        elif isinstance(value, dict):
            return dict
        elif isinstance(value, bool):
            return bool  # In case NocoDB does return actual booleans someday

        # If it's an int, collect for later bool check
        elif isinstance(value, int):
            seen_values.add(value)

            # Early float detection
            if isinstance(value, float):
                return float

    # Post-loop logic for int fields
    if seen_values:
        if seen_values <= {0, 1}:
            return bool
        else:
            return int

    # Nothing found
    return None

def coerce_value_to_type(value, target_type):
    '''Attempts to coerce a string value to the specified Python type. Takes value and target type as arguments. Returns boolean. Raises ValueError on failure.'''
    if target_type is bool:
        if value.lower() in ["true", "yes", "1"]:
            return True
        elif value.lower() in ["false", "no", "0"]:
            return False
        else:
            raise ValueError(f"'{value}' is not a valid boolean.")
    try:
        return target_type(value)
    except Exception as e:
        raise ValueError(f"Cannot convert '{value}' to {target_type.__name__}: {e}")

def value_matches(field_value, target_value):
    """Returns True if target_value matches field_value. Handles lists and comma-separated strings."""
    target_value = target_value.lower()

    if isinstance(field_value, list):
        return any(target_value in str(v).lower() for v in field_value)

    if isinstance(field_value, str) and "," in field_value:
        # Split string into list and compare
        return target_value in [v.strip().lower() for v in field_value.split(",")]

    return target_value in str(field_value).lower()


def debug_print(*args, **kwargs):
    '''Prints debug things when -v is in the command'''
    if args_global.verbose:
        print("[DEBUG]", *args, **kwargs)

# CORE FEATURES

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
    '''Lists all works by a given author. Takes author name as an argument and returns a list of matching books'''
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
       
def list_book_editions(book_title):
    '''Lists all editions of a specific book. Takes the book title as an argument and returns all matching editions for that book'''
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

def parse_filter_criteria(criteria_list):
    '''Takes filter arguments and formats them for usage. Takes arguments and returns a list of dictionaries'''
    for criterion in criteria_list:

        # Initialise empty dict
        parsed_filter = {
                "field": None,
                "values": [],
                "logic": "AND", # Default logic. Also takes OR
                "negate": False,
        }

        parsed_filters = []

        # Check for logic prefixes
        if criterion.upper().startswith("NOT:"):
            parsed_filter["negate"] = True
            criterion = criterion[4:] # Removes NOT:
        elif criterion.upper().startswith("OR:"):
            parsed_filter["logic"] = "OR"
            criterion = criterion[3:] # Removes OR:
        elif criterion.upper().startswith("AND:"):
            parsed_filter["logic"] = "AND"
            criterion = criterion[4:] # Removes AND:
            
        # Split by = to get field and values
        if "=" not in criterion:
            raise ValueError("Filter must contain '=' to separate field and value")

        key, value = criterion.split("=", 1)

        # Normalise and split values
        parsed_filter["field"] = key.strip().lower()
        parsed_filter["values"] = [v.strip().lower() for v in value.split(",")]

        parsed_filters.append(parsed_filter)
    return parsed_filters

# We figuring out field validation
def get_valid_fields(table_key):
    '''Returns a list of valid field names for a given table. Takes table key as an argument'''
    table_id = TABLE_IDS.get(table_key.upper())
    if not table_id:
        raise ValueError("Table not found.")

    records = get_records(table_id)
    if not records:
        raise ValueError("No records found in the table.")

    return list(records[0].keys())

def validate_fields(input_fields, table_key):
    '''Validates that all input field names exist in the table'''
    valid_fields = get_valid_fields(table_key)
    valid_fields_lower = [f.lower() for f in valid_fields]

    for field in input_fields:
        if field.lower() not in valid_fields_lower:
            raise ValueError(f"Invalid field: {field}")

# Filter time baby
def record_matches_filter(record, parsed_filters):
    '''Compares record and filters. Takes record and parsed filter list as inputs and returns boolean'''
    for f in parsed_filters:
        field = f["field"]
        values = f["values"]
        logic = f["logic"]
        negate = f["negate"]

        debug_print(f"Field is {field}")  # debugging
        actual_field = resolve_key_case(record, field)
        debug_print(f"Actual field is {actual_field}")
        field_value = record.get(actual_field)
        debug_print(f"Field value is {field_value}")

        values = [v.lower() for v in values]

        if logic == "AND":
            match = all(value_matches(field_value, v) for v in values)
        elif logic == "OR":
            match = any(value_matches(field_value, v) for v in values)
        else:
            raise ValueError(f"Unknown logic operator: {logic}")

        if negate:
            match = not match

        if not match:
            return False

    return True

# HANDLER FUNCTIONS FOR CLEAN CLI LOGIC

def handle_get(table_key):
    '''Handles the logic for the get_records() function. Takes a table key and prints the formatted records'''
    table_id = TABLE_IDS.get(table_key.upper())
    if not table_id:
        print("Invalid table name.")
        print_valid_tables()
        return

    records = get_records(table_id)
    formatter = FORMATTERS.get(table_key.upper(), lambda x: print(x))
    for record in records:
        formatter(record)

def handle_empty(table_key, field_name):
    '''Handles the logic for the find_empty_fields() function. Takes a table key and field nakme and prints the matching formatted records'''
    formatter = FORMATTERS.get(table_key.upper(), lambda x: print(x))
    find_empty_fields(table_key, field_name, formatter)

def handle_list_fields(table_key):
    '''Handles the logic for the list_fields() function. Takes a table key and prints a list of fields'''
    list_fields(table_key)

def handle_list_tables():
    '''Handles the logic for the print_valid_tables() function. Prints a list of all valid tables'''
    print_valid_tables()

def handle_author_works(author_name):
    '''Handles the logic for the list_author_works() function. Takes an author name and prints a list of all of their books'''
    list_author_works(author_name)

def handle_list_editions(book_title):
    '''Handles the logic for the list_book_editions() function. Takes a book title and prints a list of editions of that book'''
    list_book_editions(book_title)

def handle_filter(table_key, criteria_list):
    '''Handles the logic for filtering records. Takes the inputs table key and criteria list and prints a list of records matching the filter'''
    parsed_filter_criteria = parse_filter_criteria(criteria_list)
    debug_print(f"Parsed filters: {parsed_filter_criteria}")
    
    # Validate fields. Raises an error if invalid
    input_fields = [f["field"] for f in parsed_filter_criteria]
    validate_fields(input_fields, table_key)

    for f in parsed_filter_criteria:
        field = f["field"]
        values = f["values"]

        inferred_type = infer_field_type(table_key, field)
        debug_print(f"Field '{field}' inferred as type {inferred_type.__name__ if inferred_type else 'Unknown'}")
        
        if inferred_type is None:
            debug_print(f"Skipping type validation for field '{field}' (no type could be inferred)")
            continue

        # Coerce to type
        for v in values:
            try:
                _ = coerce_value_to_type(v, inferred_type)
            except ValueError as e:
                raise ValueError(f"Invalid value for field '{field}': {e}")

        f["values"] = [coerce_value_to_type(v, inferred_type) for v in values]

    # Get all records from the table
    records = get_records(TABLE_IDS[table_key.upper()])

    # Filter records using passed and coerced data
    filtered_records = [record for record in records if record_matches_filter(record, parsed_filter_criteria)]

    # Output formatted filtered results
    formatter = FORMATTERS[table_key.upper()]
    for record in filtered_records:
        formatter(record)

    if not filtered_records:
        print("No matching records found.")
        

# DEBUG HANDLERS
def handle_debug_type(table_key, field):
    infer_field_type(table_key, field) 

# ARGPARSE LOGIC
get_parser = subparsers.add_parser("get", help="Get all records from a specified table")
get_parser.add_argument("table", choices=[t.lower() for t in TABLE_IDS.keys()], type=str.lower, help ="Table to fetch records from")

empty_parser = subparsers.add_parser("empty", help="Find records with empty fields")
empty_parser.add_argument("table", choices=[t.lower() for t in TABLE_IDS.keys()], type=str.lower, help="Table to search")
empty_parser.add_argument("field", help="Field name to check for emptiness")

filter_parser = subparsers.add_parser("filter", help="Filter records by multiple field=value criteria")
filter_parser.add_argument("table", choices=[t.lower() for t in TABLE_IDS.keys()], type=str.lower, help="Table to filter")
filter_parser.add_argument("criteria", nargs="+", help="List of filters, e.g. Genre=fiction Owned=true")

author_parser = subparsers.add_parser("author-works", help="List all books by a given author")
author_parser.add_argument("name", help="Author name")

vibe_parser = subparsers.add_parser("vibe", help="Search for a term in both Tags and Genre in the BOOKS table")
vibe_parser.add_argument("term", help="Search term")

editions_parser = subparsers.add_parser("list-editions", help="List all editions of a given book")
editions_parser.add_argument("title", help="Book title")

# DEBUGGING ARGPARSE LOGIC
fields_parser = subparsers.add_parser("debug-fields", help="Print all field names in a table")
fields_parser.add_argument("table", choices=[t.lower() for t in TABLE_IDS])

validate_parser = subparsers.add_parser("debug-validate", help="Validate field names for a table")
validate_parser.add_argument("table", choices=[t.lower() for t in TABLE_IDS])
validate_parser.add_argument("fields", nargs="+", help="Field names to validate")

type_parser = subparsers.add_parser("debug-type", help="Infer the data type of a field")
type_parser.add_argument("table", choices=[t.lower() for t in TABLE_IDS])
type_parser.add_argument("field", help="Field name to inspect")
type_parser.add_argument("--override-type", help="Manually override the inferred type (e.g. 'float', 'int', 'bool', 'str')")

# These lines come last
args = parser.parse_args()
args_global = args

# PARSE AND CALL
if args.command == "get":
    handle_get(args.table)

elif args.command == "empty":
    handle_empty(args.table, args.field)

elif args.command == "filter":
    handle_filter(args.table, args.criteria)

elif args.command == "author-works":
    handle_author_works(args.name)

elif args.command == "list-editions":
    handle_list_editions(args.title)

# DEBUGGING PARSE AND CALL
elif args.command == "debug-fields":
    fields = get_valid_fields(args.table)
    print(f"Fields in {args.table.upper()}:", fields)

elif args.command == "debug-validate":
    try:
        validate_fields(args.fields, args.table)
        print("Validation passed.")
    except ValueError as e:
        print(f"Validation error: {e}")

elif args.command == "debug-type":
    try:
        inferred_type = infer_field_type(args.table, args.field)
        print(f"Inferred type of {args.field} in {args.table}: {inferred_type}")
    except ValueError as e:
        print(f"Error: {e}")

