import requests
from bs4 import BeautifulSoup
import itertools
import time
start = time.time()
get_data = lambda url: BeautifulSoup(((requests.get(url)).text),"html.parser") 
product_url = "https://makromarket.uz/categories/sveci"
soup = get_data(product_url)   

get_product_urls = [link.get('href') for link in soup.find_all('a') if link.get('href').startswith("https://makromarket.uz/categories")]

with_pagination = []
without_pagination = []
filter_by_pagionation_or_not = [with_pagination.append(x) if get_data(x).find("ul", class_="pagination") else without_pagination.append((x,)) for x in get_product_urls ]

pagination_page_soup = [get_data(x).find("ul", class_="pagination") for x in with_pagination]

get_all_links = [[x["href"] for x in y.find_all("a")] for y in pagination_page_soup]

filter_links = [[x for x in get_all_links[number] if x.startswith("https://makromarket.uz/categories/")] for number in range(len(get_all_links ))]

duplicate_removed_links = [list(dict.fromkeys(filter_links[number])) for number in range(len(filter_links))]

largest_number_of_pagination = [x[-1][-6:].translate({ord(i): None for i in ':/N-?=QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm,.@йцукенгшщзхъфывапролджэячсмитьбюЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮСумкг"\n, '}) for x in duplicate_removed_links]

turn_into_integer = [int(number) for number in largest_number_of_pagination]

pagination_number_list = [[i for i in range(2,number+1)]for number in turn_into_integer]

add_link_and_paginatable_numbers=(list(zip(with_pagination,pagination_number_list)))

stick_link_paginatable_numbers= [tuple([f"{d[0]}?page={f}" for f in d[1]]) for d in add_link_and_paginatable_numbers]

paginated_list = [(with_pagination[x],)+stick_link_paginatable_numbers[x] for x in range(len(with_pagination))]

[paginated_list.append(parts) for parts in without_pagination ]

ready_list = paginated_list 

print(ready_list)

end = time.time()

print(end-start)#234 second
