import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

def get_soup(url):
    page = requests.get(url)
    return BeautifulSoup(page.content, 'html.parser')

def get_ebay_listings(search):
    search = search.replace(' ', '+')
    url = f'https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2334524.m570.l1313.TR12.TRC2.A0.H0.X{search}.TRS0&_nkw={search}'
    soup = get_soup(url)
    results = soup.find(id='mainContent')
    return results.find_all('li', class_='s-item')

def get_amazon_listings(search):
    url = f'https://www.amazon.com/s?k={search}'
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    return soup.findAll('span', attrs={'class': 'a-size-medium a-color-base a-text-normal'})

def get_bestbuy_listings(search):
    url = f'https://www.bestbuy.com/site/searchpage.jsp?st={search}'
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    return soup.findAll('h4', attrs={'class': 'sku-header'})

def get_price(element):
    return element.get_text().strip().replace('$', '')

def gather_listings_and_prices(get_listings_function, search):
    print(f'Gathering {get_listings_function.__name__.replace("get_", "").capitalize()} listings...')
    listings = get_listings_function(search)
    
    runs = 0
    for listing in listings:
        if runs >= 1:
            break
        item_element = listing.find('h3', class_='s-item__title') if 'ebay' in get_listings_function.__name__ else listing
        item_price = listing.find('span', class_='s-item__price') if 'ebay' in get_listings_function.__name__ else listing

        if None in (item_element, item_price):
            continue

        print(item_element.text.strip())
        print(item_price.text.strip())
        print()
        print()
        runs += 1

    return get_price(item_price)

def compare_prices(ebay_price, amazon_price, bestbuy_price):
    prices = {'ebay': float(ebay_price), 'amazon': float(amazon_price), 'bestbuy': float(bestbuy_price)}
    min_price = min(prices.values())
    min_site = [site for site, price in prices.items() if price == min_price][0]
    return min_site, min_price

def main():
    try:
        search = input('Enter the item you want to search for: ')
        print(f'\nSearching for {search}\n')

        ebay_price = gather_listings_and_prices(get_ebay_listings, search)
        amazon_price = gather_listings_and_prices(get_amazon_listings, search)
        bestbuy_price = gather_listings_and_prices(get_bestbuy_listings, search)

        print('Comparing the three prices...')
        site, price = compare_prices(ebay_price, amazon_price, bestbuy_price)

        print(f'Here\'s the link to the lowest price on {site.capitalize()}. Have fun!')
        print(price)

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    binary = FirefoxBinary('C:\\Program Files\\Mozilla Firefox\\firefox.exe')
    options = webdriver.FirefoxOptions()
    options.add_argument('-headless')
    driver = webdriver.Firefox(firefox_binary=binary, executable_path=r'C:\\BrowserDriver\\geckodriver.exe', firefox_options=options)
    
    main()
    driver.quit()
