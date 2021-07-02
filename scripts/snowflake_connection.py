# Importing the required packages for all your data framing needs.
import pandas as pd

# The Snowflake Connector library.
import snowflake.connector as snow
from snowflake.connector.pandas_tools import write_pandas

conn = snow.connect(
    user='FIRST_USER',
    password='Apenguin120609_!@#',
    account='DHA63769',
    warehouse='SPOTIFY_TEST',
    database='SPOTIFY_VIRAL_HITS',
    schema='PUBLIC'
)

# Create a cursor object
cur = conn.cursor()

# Now let's define all of the setup properties that we want to pass
# to Snowflake for each of these properties.
# Remember there are properties for each of these that you can alter
# by checking the documentation and defining those settings.

# Starting with the Role.
sql = "USE ROLE SYSADMIN"
cur.execute(sql)

# And moving on to define and select the warehouse we want to use.
# We do want to specify a size with the warehouse, but feel free
# to change the warehouse size.
sql = """CREATE WAREHOUSE IF NOT EXISTS SPOTIFY_TEST 
         WITH WAREHOUSE_SIZE = XSMALL"""
cur.execute(sql)

# And then select it.
sql = "USE WAREHOUSE SPOTIFY_TEST"
cur.execute(sql)

# See if the desired database exists.
sql = "CREATE DATABASE IF NOT EXISTS SPOTIFY_VIRAL_HITS"
cur.execute(sql)

# And then use it.
sql = "USE DATABASE SPOTIFY_VIRAL_HITS"
cur.execute(sql)

# Do the same with the Schema.
sql = "CREATE SCHEMA IF NOT EXISTS PUBLIC"
cur.execute(sql)

# And then use it.
sql = "USE SCHEMA PUBLIC"
cur.execute(sql)

cur.close()

# And finally, the table.
# sql = "CREATE TABLE IF NOT EXISTS VIRAL_HIT_TEST"
# cur.execute(sql)

# Create a cursor object.
cur = conn.cursor()

# Phase II: Upload from the Exported Data File.
# Let's import a new dataframe so that we can test this.
original = r"C:\Users\ardeshir.beheshti\PycharmProjects\GlobalTracks\TestData\ar_top200_daily_20210702.csv"  # <- Replace with your path.
delimiter = ","  # Replace if you're using a different delimiter.

# Get it as a pandas dataframe.
total = pd.read_csv(original, sep=delimiter)

# Drop any columns you may not need (optional).
# total.drop(columns = ['A_ColumnName',
#                       'B_ColumnName'],
#                        inplace = True)

# Rename the columns in the dataframe if they don't match your existing table.
# This is optional, but ESSENTIAL if you already have created the table format
# in Snowflake.
# total.rename(columns={"A_ColumnName": "A_COLUMN",
#                       "B_ColumnName": "B_COLUMN"},
#                        inplace=True)

# Actually write to the table in snowflake.
write_pandas(conn, total, "Test_ViralCountry_Hit")

# (Optionally, you can check to see if what you loaded is identical
# to what you have in your pandas dataframe. Perhaps... a topic for a future
# blog post.

# Phase III: Turn off the warehouse.
# Create a cursor object.
cur = conn.cursor()

# Execute a statement that will turn the warehouse off.
sql = "ALTER WAREHOUSE SPOTIFY_TEST SUSPEND"
cur.execute(sql)

# Close your cursor and your connection.
cur.close()
conn.close()

# And that's it. Much easier than using the load data utility, but maybe
# not as user friendly.
