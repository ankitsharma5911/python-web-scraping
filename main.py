import time
from datetime import datetime
import requests 
import selenium as sm
from selenium import webdriver
from bs4 import BeautifulSoup as bs
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from config import conn
conn.set_session(autocommit=True)

# -----create table in database
def setup_database():
    cur = conn.cursor()
    # create table job_listing

    cur.execute("""
    CREATE TABLE IF NOT EXISTS job_listings (
        id SERIAL PRIMARY KEY,
        job_title VARCHAR(255),
        company_name VARCHAR(255),
        location VARCHAR(255),
        job_url VARCHAR(512) UNIQUE,
        salary_info TEXT,
        job_description TEXT,
        source_site VARCHAR(100),
        scraped_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
    );
    """)

    conn.commit()
    print("Table created successfully")

    # Close
    cur.close()


def insert_job(job):
    """Insert job summary data into PostgreSQL"""

    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO job_listings (job_title, company_name, location, job_url, salary_info, source_site,scraped_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (job_url) DO NOTHING;
        """, (job["title"], job["company"], job["location"], job["url"], job["salary"], job["source"]), datetime.now())
        conn.commit()
    except Exception as e:
        print("Insert error:", e)
    finally:
        cur.close()

def update_job_description(url, description):
    """Update job description for given URL"""
    cur = conn.cursor()
    try:
        cur.execute("""
            UPDATE job_listings
            SET job_description = %s
            WHERE job_url = %s;
        """, (description, url))
        conn.commit()
    except Exception as e:
        print("Update error:", e)
    finally:
        cur.close()

# --------------------------
# Static Scraping Functions
# --------------------------

def scrap_naukri():
    print("scraping naukri.com jobs....")
    base = "https://www.naukri.com/data-jobs-in-united-kingdom-uk-{}"

    # scraping first 2 pages
    try:
        for i in range(1,3):
            url=base.format(i)
            print(url)
            driver = webdriver.Chrome()
            driver.get(url)

            html=driver.page_source

            text_html=bs(html,"html.parser")

            job_list=text_html.find_all("div",{"class":"srp-jobtuple-wrapper"})

            print(f"Found {len(job_list)} jobs on page {i}")
            for job in job_list:

                job_url=job.find("a")["href"]
                
                # job_title
                job_title = job.find("a").text
                print(job_title)
                
                # company name
                company_name=job.find("a",{"class":"comp-name"}).text

                # location
                location=job.find("span",{"class":"loc"}).text

                # salary
                salary=job.find("span",{"class":"sal"}).text

                insert_job({
                "title": job_title,
                "company": company_name,
                "location": location,
                "url": job_url,
                "salary": salary,
                "source": "naukri.com"
            })


    except Exception as e:
        print("error occured while scraping naukri.com")


def scrap_jobleads():
    print("scraping jobleads.com jobs....")
    base = "https://www.jobleads.com/search/jobs?keywords=Data+Analyst&location=&location_country=GBR&filter_by_remote=in_person&minSalary=40000&maxSalary=-1&page={}"
    try:
        for i in range(1,3):
            url=base.format(i)
            print(url)

            driver = webdriver.Chrome()
            driver.get(url)
            html=driver.page_source

            text_html=bs(html,"html.parser")
            job_list=text_html.find_all("div",{"data-testid":"search-job-card"})
            
            print(f"Found {len(job_list)} jobs on page {i}")

            for job in job_list:

                job_url="https://www.jobleads.com"+job.a["href"]
                # job_title
                job_title = job.div.h2.span.text
                print(job_title)
                
                # location
                location=job.find_all("div",{"class":"jlui-bg-neutral-95"})[0].span.span.span.text
                # salary
                salary=job.find_all("div",{"class":"jlui-bg-neutral-95"})[2].span.span.span.text

                insert_job({
                "title": job_title,
                "company": None,
                "location": location,
                "url": job_url,
                "salary": salary,
                "source": "jobleads.com"
            })

    except Exception as e:
        print("error occured while scraping naukri.com")


# --------------------------
# Dynamic Scraping using Selenium
# --------------------------

def scrape_job_descriptions():
    print("Scraping job descriptions with Selenium...")
    cur = conn.cursor()
    cur.execute("SELECT job_url,source_site FROM job_listings WHERE job_description IS NULL;")
    urls = cur.fetchall()
    cur.close()

    driver = webdriver.Chrome()  
    wait = WebDriverWait(driver, 10)
    print("updating job description..")
    
    for (url,source) in urls:
        print(url,source)
        if source=="naukri.com":
            try:
                driver.get(url)
                desc_elem = wait.until(EC.presence_of_element_located(
                    (By.CLASS_NAME,"styles_JDC__dang-inner-html__h0K4t")))
                description = desc_elem.text
                update_job_description(url, description)
                time.sleep(2)
            except Exception as e:
                print(f"Failed to scrape naukri.com: {url} - {e}")

        if source=="jobleads.com":
            try:
                driver.get(url)
                desc_elem = wait.until(EC.presence_of_element_located(
                    (By.CSS_SELECTOR, 'div.mt-6[data-testid="job-card-summary"] p')))
                description = desc_elem.text
                update_job_description(url, description)
                time.sleep(2)

            except Exception as e:
                print(f"Failed to scrape naukri.com: {url} - {e}")

        else:
            print(f"Unknown source: {source} for url: {url}")

    driver.quit()


# --------------------------
# Main
# --------------------------

if __name__=="__main__":

    setup_database()
    scrap_naukri()
    scrap_jobleads()
    scrape_job_descriptions()
    conn.close()