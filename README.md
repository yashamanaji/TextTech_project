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
