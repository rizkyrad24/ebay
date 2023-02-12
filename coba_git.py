import requests
from bs4 import BeautifulSoup

url = "https://www.tokopedia.com/search?st=product&q=laptop%20core%20i7&srp_component_id=02.01.00.00&srp_page_id=&srp_page_title=&navsource="
headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"}
res = requests.get(url, headers=headers)
soup = BeautifulSoup(res.text, "html.parser")
print(soup)

