import os
import pandas as pd
import xml.etree.ElementTree as ET

def generate_individual_xmls(csv_path, output_dir="xml_output"):
    os.makedirs(output_dir, exist_ok=True)
    df = pd.read_csv(csv_path)

    for idx, row in df.iterrows():
        try:
            book = ET.Element("book")
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

            # Save file
            book_id = f"book_{idx+1:04d}.xml"
            output_path = os.path.join(output_dir, book_id)
            tree = ET.ElementTree(book)
            tree.write(output_path, encoding="utf-8", xml_declaration=True)

        except Exception as e:
            print(f"❌ Skipped book_{idx+1:04d}.xml due to error: {e}")

if __name__ == "__main__":
    csv_path = "books_with_prediction_confidence_score.csv"  # adjust path as needed
    generate_individual_xmls(csv_path, output_dir="xml_output")
