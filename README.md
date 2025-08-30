# Python Web Scraper Internship Assignment

This project is a Python-based web scraper for collecting job listings and descriptions from **naukri.com** and **jobleads.com**, storing them in a PostgreSQL database. Selenium and BeautifulSoup are used for scraping, and psycopg2 for database operations.

---

## Features

- Scrapes job summary data (title, company, location, salary, URL, source) from multiple pages.
- Scrapes detailed job descriptions using Selenium.
- Stores all data in a PostgreSQL database.
- Handles duplicate job URLs.
- Uses environment variables for secure database connection.

---

## Requirements

- Python 3.8+
- PostgreSQL database (cloud or local)
- Chrome browser
- ChromeDriver (matching your Chrome version)

### Python Packages

Install dependencies with:

```shell
pip install selenium beautifulsoup4 psycopg2-binary python-dotenv requests
```
*In this project i used uv Package manager
---

## Setup

1. **Clone the repository**  
   Place all files in a working directory.

2. **Configure Environment Variables**  
   Edit `.env` with your database credentials:

   ```
   Host="your-db-host"
   Port=5432
   Database="internship_assessment"
   Username="your-username"
   Password="your-password"
   ```

3. **Install ChromeDriver**  
   Download [ChromeDriver](https://chromedriver.chromium.org/downloads) and add it to your PATH.

---

## Usage

Run the main script:

```shell
python main.py
```

This will:
- Create the `job_listings` table if it doesn't exist.
- Scrape job summaries from naukri.com and jobleads.com.
- Scrape job descriptions for jobs missing them.
- Store all results in the database.

---

## Database

The table schema:

| Column         | Type         | Description                |
|----------------|--------------|----------------------------|
| id             | SERIAL       | Primary key                |
| job_title      | VARCHAR(255) | Job title                  |
| company_name   | VARCHAR(255) | Company name               |
| location       | VARCHAR(255) | Job location               |
| job_url        | VARCHAR(512) | Unique job URL             |
| salary_info    | TEXT         | Salary information         |
| job_description| TEXT         | Full job description       |
| source_site    | VARCHAR(100) | Source website             |
| scraped_at     | TIMESTAMPTZ  | Scrape timestamp           |

---

## Troubleshooting

- **No data in database:**  
  Check for errors in the terminal. Make sure your database credentials are correct and ChromeDriver is installed.
- **PGPASSWORD not recognized:**  
  On Windows, use the `-W` flag with `psql` to enter your password interactively.

---

## License

This project is for educational and internship assessment purposes.

---

## Author

Ankit sharma