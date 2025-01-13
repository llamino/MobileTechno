# mobile/tasks.py

import requests
from bs4 import BeautifulSoup
import re
import time
from django.utils import timezone
from celery import shared_task
from .models import Mobile
from decimal import Decimal
import logging
from django.db import transaction
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

logger = logging.getLogger(__name__)

@shared_task
def scrape_and_update_mobiles():
    """
    Celery task to scrape mobile data from the website and update the database.
    This task deletes existing mobiles and adds new ones.
    """

    base_url = "https://www.technolife.ir"
    url = f"{base_url}/product/list/69_800_801/تمامی-گوشی‌ها"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    products = []

    def extract_data(html_content, headers, base_url):
        '''
            function for extracting data from html page
        '''

        soup = BeautifulSoup(html_content, 'html.parser')
        product_blocks = soup.find_all('section', class_=re.compile(r'.+'))  # پیدا کردن بلوک محصولات
        extracted_products = []

        for block in product_blocks:
            name_tag = block.find('h2', class_=re.compile(r'.+'))
            if name_tag:
                product_name = name_tag.get_text(strip=True)
            else:
                product_name = "نامشخص"

            price_tag = block.find('p', class_=re.compile(r'text-\[22px\]'))
            if price_tag:
                product_price = re.sub(r'\D', '', price_tag.get_text())
            else:
                product_price = "نامشخص"

            img_tag = block.find('img', attrs={"src": True})
            if img_tag:
                product_image = base_url + img_tag['src']
            else:
                product_image = "تصویر موجود نیست"

            # extracting product_id from image_url
            pattern = r"TLP-(\d+)"
            match = re.search(pattern, product_image)
            if match:
                product_id = match.group(1)  # استخراج عدد
            else:
                print("عدد بعد از TLP- پیدا نشد.")

# ===================================== extracting product detail =============================================

            detail_url = f"{base_url}/product-{product_id}/{product_name}"
            detail_response = requests.get(detail_url, headers=headers)
            detail_html_content = detail_response.text
            detail_soup = BeautifulSoup(detail_html_content, 'html.parser')
            product_detail_section = detail_soup.find('div', class_=re.compile(r'^rounded-md'))
            product_detail_blocks = product_detail_section.find_all('div', class_=re.compile(r'^flex'))
            product_detail = []
            for detail_block in product_detail_blocks:
                #  extracting cpu-memory-ram-monitor_size-back_camera-battery
                detail_tag = detail_block.find('p', class_=re.compile(r'^ml-1'))
                if detail_tag:
                    product_detail.append(detail_tag.get_text())

            cpu = product_detail[0] if len(product_detail) > 0 else None
            memory = product_detail[1] if len(product_detail) > 1 else None
            ram = product_detail[2] if len(product_detail) > 2 else None
            monitor_size = product_detail[2] if len(product_detail) > 3 else None
            back_camera = product_detail[3] if len(product_detail) > 4 else None
            battery = product_detail[4] if len(product_detail) > 5 else None

            extracted_products.append({
                'name': product_name,
                'price': product_price,
                'image': product_image,
                'product_id': product_id,
                'cpu': cpu,
                'memory': memory,
                'ram': ram,
                'monitor_size': monitor_size,
                'back_camera': back_camera,
                'battery': battery,
            })
        return extracted_products
# ===================================== end of extracting ===========================================

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        html_content = response.text
        products.extend(extract_data(html_content, headers, base_url))
    else:
        print(f"خطا در دریافت صفحه: {response.status_code}")
        exit()


    for page in range(1, 3):
        next_url = f"{url}?page={page}"
        print(f"در حال پردازش صفحه: {page}...")
        response = requests.get(next_url, headers=headers)
        if response.status_code == 200:
            html_content = response.text
            new_products = extract_data(html_content, headers, base_url)
            if not new_products:
                break
            products.extend(new_products)
        else:
            print(f"خطا در دریافت صفحه {page}: {response.status_code}")
            break
        time.sleep(1)

    Mobile.objects.all().delete()
    for product in products:
        if Mobile.objects.filter(product_id=product['product_id']).exists():
            continue
        Mobile.objects.create(
            product_id = product['product_id'],
            name = product['name'],
            image_url= product['image'],
            price= product['price'],
            cpu= product['cpu'],
            memory= product['memory'],
            ram= product['ram'],
            monitor_size= product['monitor_size'],
            back_camera= product['back_camera'],
            battery=product['battery']
    )
    return f"Scraped and updated {len(products)} mobiles."
