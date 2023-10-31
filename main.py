# Importing BeautifulSoup class from the bs4 module 
from bs4 import BeautifulSoup 
import sqlite3
import requests 
from dotenv import load_dotenv # for reading the .env file 
import os # for getting the environment variable


load_dotenv() 
URL = os.getenv("URL")
r = requests.get(URL) 
  
# Creating a BeautifulSoup object and specifying the parser 
page = BeautifulSoup(r.content, 'html.parser') 

# This function retries all the urls from the pages and filters for the ones ending with .pdf
def get_urls():
    urls = page.findAll("a")
    printed = []
    for url in urls:
        url = url.get("href") # filter out the url from the tag
        if (not url == None) and url.endswith(".pdf") and url not in printed: # filters to urls ending with .pdf and make sure they are unique
            printed.append(url)
    return printed

urls = get_urls()

db = sqlite3.connect("main.db", isolation_level=None) # we will store the urls and find any new ones
cursor = db.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS `data` (
`existing` VARCHAR(255) UNIQUE NOT NULL
)""")   

cursor.execute("SELECT `existing` FROM `data`")
existing = cursor.fetchall()
existing = [item[0] for item in existing]
new = []
for url in urls:
    if not url in existing:
        print(url)
        cursor.execute("INSERT INTO `data` (`existing`) VALUES (?)",(url,)) # inserts the new url to the `existing` column in the `data` table 
        new.append(url)

if len(new) > 0: # only run this if there is a new url
    # import all the modules required
    from discord_webhook import DiscordWebhook # for sending data through the discord webhook

    
    new_line = "\n" # python doesn't support backslashes in the f-string
    WEBHOOK_URL = os.getenv("WEBHOOK_URL")
    USER_ID = 640773439115886642

    webhook = DiscordWebhook(url=WEBHOOK_URL, content=f"""
New files found
{new_line.join(new)}
<@!{USER_ID}>""") # THIS IS SUPPOSED TO GIVE ERROR AFTER 2000 CHARACTERS so that it doesn't send around stuff when first run
    # honestly, it's mostly because I'm lazy and this works
    # Edit this bit to send multiple msgs if there are more than 2000 characters.
    
    response = webhook.execute() # send the data through the webhook