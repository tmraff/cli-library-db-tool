import requests

API_KEY = "fbDo38Joogrf8-In0vjcVb5dCK0yuhZL5M06GM1A"
BASE_ID = "pov40kx5cdtfqty"
BOOKS_ID = "mth1bd75romp8p3"

url = f"http://127.0.0.1:8080/api/v2/tables/{BOOKS_ID}/records"

headers = {
    "accept": "application/json",
    "xc-token": API_KEY
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    books = response.json()["list"]
    print("-" * 40)

    for book in books:
        print(f"{book['Title']} ({book['First Published']})")
        print(f"   Author(s): {', '.join(book['Author(s)'])}")
        print(f"   Genre: {book.get('Genre', 'N/A')}")
        print(f"   Tags: {book.get('Tags', 'N/A')}")
        print(f"   Status: {book['Status']} | Rating: {book['Rating']}")
        print(f"   Owned: {'Yes' if book['Owned'] else 'No'} | Annotated: {'Yes' if book['Annotated'] else 'No'}")
        print("-" * 40)

else:
    print("Error:", response.status_code, response.text)
