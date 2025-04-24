# Import requests library so I can talk to the API
import requests

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
    print("-" * 40)


def format_authors(author):
    '''Formats author records cleanly. Takes a record from the Authors table as an argument and prints the output nicely'''
    print(f"{author['Name']} ({author.get('Pronouns', 'N/A')})")
    print(f"  Website: {author.get('Website', 'N/A')}")
    print(f"  Notes: {author.get('Notes', '')}")
    print("-" * 40)

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
    print("-" * 40)

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
    print("-" * 40)

def format_artworks(artwork):
    '''Formats artwork records cleanly.'''
    title = artwork.get('Title', 'Untitled')
    print(f"{title}")
    print(f"  Medium: {artwork.get('Medium', 'Unknown')} | Date: {artwork.get('Date', 'Unknown')}")
    if artwork.get('Books') and artwork['Books'].get('Display Name'):
        print(f"  Related to: {artwork['Books']['Display Name']}")
    else:
        print("  Related to: None")
    print("-" * 40)

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
    print("-" * 40)

# Print fun lil ASCII title
print("-" * 40)
print(r"""
 ____  _  _    __    __  ____  ____  __  ____ 
(  __)( \/ )  (  )  (  )(  _ \(  _ \(  )/ ___)
 ) _)  )  (   / (_/\ )(  ) _ ( )   / )( \___ \
(____)(_/\_)  \____/(__)(____/(__\_)(__)(____/
""")
print("-" * 40)

# Loops the program
while True:

    # Ask the user which table to print the records from and print them
    table_key = input("Which table? ").strip().upper()
    table_id = TABLE_IDS.get(table_key)
    if table_key in("EXIT", "QUIT"):
        break

    print("-" * 40)

    # If the table doesn't exist, tell the user
    if table_id is None:
        print("Table not found.")

    # Otherwise, get the records
    else:
        table_records = get_records(table_id)

    # Format the records according to their table
    if table_key == "BOOKS":
        for record in table_records:
            format_books(record)
    elif table_key == "AUTHORS":
        for record in table_records:
            format_authors(record)
    elif table_key == "EDITIONS":
        for record in table_records:
            format_editions(record)
    elif table_key == "PUBLISHERS":
        for record in table_records:
            format_publishers(record)
    elif table_key == "ARTWORKS":
        for record in table_records:
            format_artworks(record)
    elif table_key == "REVIEWS":
        for record in table_records:
            format_reviews(record)



    # Contingency for if the formatting fails
    else:
        print(table_records)
    


