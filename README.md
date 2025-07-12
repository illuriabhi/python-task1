# 🛠️ Alibaba RFQ Scraper (100 Pages)

This project is a web scraper built using **Playwright (Python)** to extract Request for Quotation (RFQ) data from Alibaba's RFQ listing pages.

## 📌 Features

- Scrapes up to **100 pages** of RFQs from the Alibaba website
- Extracts essential fields including:
  - RFQ ID
  - Title
  - Buyer Name
  - Country
  - Quantity Required
  - Quotes Left
  - Date Posted
  - Email Confirmed
  - Complete Order via RFQ
  - Experienced Buyer
  - Interactive User
  - RFQ URL
  - Scraping Date
- Saves data into a **CSV file** in the same format as provided

---

## 🔧 Technologies Used

- Python 3.8+
- Playwright (Python)
- pandas

---

## 🚀 How to Run

### 1. Install Dependencies

```bash
pip install playwright pandas
playwright install
