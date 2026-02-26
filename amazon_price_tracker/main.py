import os
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
import smtplib

load_dotenv()

URL = os.getenv("URL")

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "en-IN,en;q=0.9"
}

response = requests.get(url=URL,headers=headers)
soup = BeautifulSoup(response.text,"html.parser")

price_rupee = soup.find(name="span", class_="a-price-whole").getText()
price = float(price_rupee.replace(",",""))
print(soup.prettify())
product_title_name =soup.find(name="span",id="productTitle")
product_title = " ".join(product_title_name.getText().split())
target_price = 6000.0

if price <= target_price:
    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
         connection.starttls()
         connection.login(user= os.getenv("MY_ACC"),password=os.getenv("PASSWORD"))
         connection.sendmail(from_addr=os.getenv("MY_ACC"),
                             to_addrs=os.getenv("TO_MAIL"),
                             msg=f"subject:price Alert\n\n{product_title} is now RS{price}\nlink {URL}".encode("utf-8"))

