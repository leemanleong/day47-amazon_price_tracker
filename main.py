from bs4 import BeautifulSoup
import requests
import certifi
import smtplib
import os 
import dotenv
# import lxml 
# Load environment variables from .env file
dotenv.load_dotenv()

practice_url = "https://appbrewery.github.io/instant_pot/"
live_url = "https://www.amazon.com/Instant-Pot-DUO60-Programmable-Multi-Cooker/dp/B00FLYWNYQ"
header = {
    "Accept-Language": "en-US,en;q=0.9", 
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0"
    }

response = requests.get(url=live_url, headers=header, verify=certifi.where())
print(f"Response code: {response.status_code}")

soup = BeautifulSoup(response.text, "html.parser") 
# soup = BeautifulSoup(response.text, "lxml")
#check you are getting the action amazon page back and not something else:
# print(soup.prettify())

# ====================== Get the Price ==========================

price = soup.select_one(selector="div span.aok-offscreen").getText()
price_without_dollar = price.split("$")[1].split(" ")[0]
print(type(price_without_dollar))
print(price_without_dollar)
price_as_float = float(price_without_dollar)
print(type(price_as_float))
print(price_as_float)

# ====================== Send an Email ===========================

# Get the product title 
product_title = soup.select_one(selector="div span#productTitle").getText().strip()
product_title = " ".join(product_title.split())
print(f"Product title: {product_title}")

# Set the price below which you would like to get a notification email 
BUY_PRICE = 80.00

# Send an email if the price is less than 100
if price_as_float < BUY_PRICE:
    print("Lower Price! Buy it now!")
    
    # use smtplib to send an email with gmail
    SMTP_ADDRESS = os.environ["SMTP_ADDRESS"]
    SMTP_PORT = os.environ["SMTP_PORT"]
    MY_EMAIL = os.environ["EMAIL_ADDRESS"]
    MY_PASSWORD = os.environ["EMAIL_PASSWORD"]
    TO_EMAIL = "email@gmail.com"
    
    subject = "Amazon Price Alert"
    message = f"{product_title} is on sale for {price_as_float}"
  
    with smtplib.SMTP(SMTP_ADDRESS, port=SMTP_PORT) as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=MY_PASSWORD)
        connection.sendmail(
            from_addr=MY_EMAIL, 
            to_addrs=TO_EMAIL, 
            msg=f"Subject:{subject}\n\n{message}\n{live_url}".encode("utf-8")
            )

