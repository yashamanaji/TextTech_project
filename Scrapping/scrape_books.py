import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

# Base URLs
base_url = 'https://books.toscrape.com/catalogue/page-{}.html'
book_base_url = 'https://books.toscrape.com/catalogue/'

# Create necessary directories
os.makedirs('data_sheet', exist_ok=True)
os.makedirs('images', exist_ok=True)

books = []

def extract_data_from_page(soup, page):
    for book in soup.find_all('article', class_='product_pod'):
        title = book.h3.a['title']
        price = book.find('p', class_='price_color').text
        availability = book.find('p', class_='instock availability').text.strip()
        rating_text = book.p['class'][1]
        rating = convert_rating_to_number(rating_text)
        relative_link = book.h3.a['href']
        product_link = book_base_url + relative_link.replace('../../../', '')  # normalize link
        thumbnail_url = 'https://books.toscrape.com/' + book.find('img', class_='thumbnail')['src']
        thumbnail_file_name = save_thumbnail_image(thumbnail_url, title)

        # Extract description from the individual book page
        description, genre = extract_book_details(product_link)

        book_data = {
            'Title': title,
            'Price': price,
            'Availability': availability,
            'Rating': rating,
            'Link': product_link,
            'Thumbnail URL': thumbnail_url,
            'Thumbnail File Name': thumbnail_file_name,
            'Description': description,
            'Genre': genre
        }

        books.append(book_data)

        print(f"Page: {page}")
        print(f"Title: {title}")
        print(f"Price: {price}")
        print(f"Availability: {availability}")
        print(f"Rating: {rating}")
        print(f"Link: {product_link}")
        print(f"Thumbnail URL: {thumbnail_url}")
        print(f"Thumbnail File Name: {thumbnail_file_name}")
        print(f"Description: {description}")
        print(f"Genre: {genre}")
        print("=" * 80)

def convert_rating_to_number(rating_text):
    rating_dict = {
        'One': 1,
        'Two': 2,
        'Three': 3,
        'Four': 4,
        'Five': 5
    }
    return rating_dict.get(rating_text, 0)

def save_thumbnail_image(url, title):
    response = requests.get(url)
    sanitized_title = "".join([c if c.isalnum() else "_" for c in title])
    image_path = os.path.join('images', f"{sanitized_title}.jpg")
    with open(image_path, 'wb') as file:
        file.write(response.content)
    return image_path

def extract_book_details(product_url):
    response = requests.get(product_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Get description
    description = "No description available."
    meta_description = soup.find("meta", attrs={"name": "description"})
    if meta_description and meta_description.get("content"):
        description = meta_description["content"].strip()
    else:
        description_section = soup.select_one("#product_description ~ p")
        if description_section:
            description = description_section.text.strip()
    
    # Get genre from breadcrumb
    genre = "Unknown"
    breadcrumb = soup.select('ul.breadcrumb li a')
    if len(breadcrumb) >= 3:
        genre = breadcrumb[2].text.strip()

    return description, genre

# Loop through pages
for page in range(1, 51):
    url = base_url.format(page)
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    extract_data_from_page(soup, page)

    # testing
    print(f"Total books scraped: {len(books)}")

# Save to CSV
df = pd.DataFrame(books)
df = df.head()
df.to_csv('data_sheet/books_data.csv', index=False)
print("Data saved to data_sheet/books_data.csv")

# ✅ Generate XML
from generate_xml import generate_xml_from_csv
generate_xml_from_csv("data_sheet/books_data.csv")
