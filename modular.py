import requests
from  bs4 import BeautifulSoup
import mysql.connector

s = requests.session()
headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
    }

def get_general (url:str):
    res = s.get(url, headers=headers)
    if res.status_code == 200:
        soup = BeautifulSoup(res.text, 'html.parser')
        generals = soup.findAll('li', 's-item s-item--large')
        data_general = []
        for general in generals:
            link = general.find('div', 's-item__info clearfix').find('a')['href']
            try:
                title = general.find('h3', 's-item__title s-item__title--has-tags').text
            except:
                title = general.find('h3', 's-item__title').text
            try:
                rating = general.find('div', 'star-rating b-rating__rating-star')['data-stars']
            except:
                rating = "no rating"
            price = general.find('span', 's-item__price').text
            shipping = general.find('span', 's-item__shipping s-item__logisticsCost').text
            try:
                info = general.find('span', 'NEGATIVE').text
            except:
                info = ""
            dict = {
                'Link': link,
                'Title': title,
                'Rating': rating,
                'Price': price,
                'Shipping Cost': shipping,
                'Info': info
            }
            data_general.append(dict)
        return data_general

def get_detail (url_detail:str):
    res = s.get(url_detail, headers=headers)
    if res.status_code == 200:
        detail = BeautifulSoup(res.text, "html.parser")
        try:
            image1 = detail.find('div', 'ux-image-carousel-item active image').find('img')['src']
        except:
            image1 = "no image"
        try:
            image2 = detail.find('img', 'vi-image-gallery__image vi-image-gallery__image--absolute-center')['src']
        except:
            image2 = "no image"
        try:
            image3 = detail.find('div', 'ux-image-carousel-item image').find('img')['src']
        except:
            image3 = "no image"
        if image2 != "no image":
            image = image2
        elif image1 != "no image":
            image = image1
        elif image3 != "no image":
            image = image3
        else:
            image = "no image"
        try:
            condition = detail.find('div',
                                    'ux-layout-section ux-layout-section--condition ux-layout-section--SECTION_WITH_BACKGROUND').text
        except:
            condition = "none"
        try:
            about1 = detail.find('div', 'ux-layout-section__item ux-layout-section__item--table-view').text
        except:
            about1 = 'none'
        try:
            about2 = detail.find('section', 'product-spectification').text
        except:
            about2 = 'none'
        if about1 != "none":
            about = about1
        elif about2 != "none":
            about = about2
        else:
            about = "none"
        dict = {
            'Image': image,
            'Condition': condition,
            'About': about
        }
    return dict

def scraping():
    data_all = []
    for page in range (1,11):
        url = "https://www.ebay.com/b/Cell-Phones-Smartphones/9355/bn_320094?_pgn={}".format(page)
        results = get_general(url)
        for result in results:
            detail = get_detail(result['Link'])
            result.update(detail)
            data_all.append(result)
    return data_all

def connect ():
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        database='scraping_results',
        password=''
    )
    return conn

def making_table ():
    conn = connect()
    querybox = conn.cursor()
    querybox.execute("create table if not exists scraping_ebay(id int AUTO_INCREMENT PRIMARY KEY,"
                     "Image varchar(1000),"
                     "Title varchar(1000),"
                     "Price varchar(100),"
                     "Shipping_cost varchar(100),"
                     "Rating varchar(10),"
                     "Info varchar(100),"
                     "Link varchar(2000),"
                     "Note_From_Seller varchar(5000),"
                     "Detail varchar(5000))")
    conn.commit()

def push_to_database ():
    conn = connect()
    querybox = conn.cursor()
    data_all = scraping()
    for data in data_all:
        query = "INSERT INTO scraping_ebay(Image,Title,Price,Shipping_cost,Rating,Info,Link,Note_From_Seller,Detail) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        value = (
            data['Image'],
            data['Title'],
            data['Price'],
            data['Shipping Cost'],
            data['Rating'],
            data['Info'],
            data['Link'],
            data['Condition'],
            data['About']
        )
        querybox.execute(query, value)
        conn.commit()

if __name__ == "__main__":
    making_table()
    push_to_database()