# TextTech_project
This project is part of the **Text Technology** course at the University of Stuttgart. We build an end-to-end pipeline that scrapes book data, classifies genres using machine learning, and encodes metadata in XML using RelaxNG — fulfilling the *collect–prepare–access* requirements and including a technical extension beyond lectures.

---

## 🚀 Project Overview

> A publishing platform wants to automatically classify new books by genre based on their descriptions. We help by scraping book data, training a genre classifier, and encoding the enriched metadata in structured XML format for archival, querying, and presentation.

---

## 🛠️ Workflow Summary

| Phase     | Description                                                                 |
|-----------|-----------------------------------------------------------------------------|
| ✅ Collect | Scrape book metadata from [books.toscrape.com](https://books.toscrape.com) |
| ✅ Prepare | Clean data, apply NLP preprocessing, and train a genre classification model |
| ✅ Access  | Output predictions as XML using a RelaxNG schema; store in a database       |

---

## 📦 Dataset

- Source: [https://books.toscrape.com](https://books.toscrape.com)
- Fields extracted: `Title`, `Price`, `Availability`, `Rating`, `Description`, `Genre`, `Thumbnail URL`
- Description and genre were scraped from each book’s individual product page.
- Genre was extracted from the breadcrumb section.

---

## Explanation
- `Scrapping\scrape_books.py`: scrapes book data from the publicly available website https://books.toscrape.com/
- `ML Pipeline.ipynb`: Pipeline that predicts genre label and probability/confidence score.
- `generate_xml_per_book.py`: Creates an individual XML file for each book.
- `RelaxNG Schema\book_schema.rng`: RelaxNG (RNG) schema to validate the structure of each generated XML file. 
- `validate_xml.py`: validate all the generated XML files using RelaxNG schema.
- `load_to_MongoDB_Atlas.py`: A MongoDB loader script to insert these XML files as documents (XML (book files) ➡️ Python dict ➡️ MongoDB document).
- `query.py`: MongoDB queries that can run on the books collection to explore the dataset further and fulfill the **Access** part of the project.
- `app.py` – Flask API server that handles frontend requests and queries MongoDB.
- `frontend\index.html`: UI for filtering/querying.
