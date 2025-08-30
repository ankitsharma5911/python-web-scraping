import psycopg2
from dotenv import load_dotenv
import os
load_dotenv()

# load envs
Host = os.getenv("Host")
password = os.getenv("Password")

# Connection setup
conn = psycopg2.connect(
    host=Host,
    # host="localhost",
    port="5432",
    database="internship_assessment",
    user="ankit",
    password=password
)

# Create a cursor
# cur = conn.cursor()

# # Run a query
# cur.execute("SELECT version();")
# print(cur.fetchone())

# # Close
# cur.close()
# conn.close()

