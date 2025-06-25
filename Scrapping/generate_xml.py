import os
import pandas as pd
import xml.etree.ElementTree as ET

def generate_xml_from_csv(csv_path, output_dir="xml_output"):
    os.makedirs(output_dir, exist_ok=True)
    df = pd.read_csv(csv_path)

    root = ET.Element("books")

    for _, row in df.iterrows():
        book = ET.SubElement(root, "book")
        ET.SubElement(book, "title").text = str(row['Title'])
        ET.SubElement(book, "price").text = str(row['Price'])
        ET.SubElement(book, "availability").text = str(row['Availability'])
        ET.SubElement(book, "rating").text = str(int(row['Rating'])) if not pd.isna(row['Rating']) else "N/A"
        ET.SubElement(book, "description").text = str(row['Description'])
        ET.SubElement(book, "genre_actual").text = str(row['Genre'])
        ET.SubElement(book, "genre_predicted").text = str(row.get('Predicted_Genre', 'N/A'))
        ET.SubElement(book, "confidence").text = str(row.get('Prediction_Confidence', 'N/A'))
        ET.SubElement(book, "link").text = str(row['Link'])
        ET.SubElement(book, "thumbnail_url").text = str(row['Thumbnail URL'])

    tree = ET.ElementTree(root)
    output_file = os.path.join(output_dir, "books.xml")
    tree.write(output_file, encoding="utf-8", xml_declaration=True)
    print(f"✅ XML saved to {output_file}")



if __name__ == "__main__":
    generate_xml_from_csv("data_sheet/books_with_prediction_confidence_score.csv", "data_sheet/books_combined.xml")
