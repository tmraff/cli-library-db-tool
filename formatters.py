# FORMATTER FUNCTIONS

def format_books(book):
    '''Formats book records cleanly. Takes a record from the Books table as an argument and prints the output nicely'''
    print(f"{book['Title']} ({book['First Published']})")
    authors = book.get('Author(s)', [])
    print(f"   Author(s): {', '.join(authors) if authors else 'N/A'}")
    genre = book.get('Genre')
    print(f"   Genre: {genre.replace(',', ', ') if genre else 'N/A'}")
    tags = book.get('Tags')
    print(f"   Tags: {tags.replace(',', ', ') if tags else 'N/A'}")
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

