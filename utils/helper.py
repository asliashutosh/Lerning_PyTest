import os
import time
import requests
from PIL import Image
from io import BytesIO
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


def get_top_trending_topic(driver):
    driver.get("https://trends.google.com/trending?geo=IN")
    time.sleep(2)
    topic = driver.find_element(By.CSS_SELECTOR, ".feed-item-header a").text
    print(f"Top Trending Topics: {topic}")
    return topic


def fetch_image(driver, topic, download_dir):
    driver.get("https://www.google.com/imghp")
    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys(topic)
    search_box.send_keys(Keys.RETURN)
    time.sleep(2)

    # Fetch image URL

    images = driver.find_element(By.CSS_SELECTOR, "img.rg_i")
    img_urls = []
    for img in images[:10]:
        try:
            img.click()
            time.sleep(1)
            large_img = driver.find_element(By.CSS_SELECTOR, "img.n3VNCb")
            img_url = large_img.get_attribute("src")
            if img_url.startswith("http"):
                img_urls.append(img_url)
        except Exception as e:
            print(f"Error fetching image: {e}")

    # Download Images

    os.makedirs(download_dir,exist_ok=True)
    for idx, img_url in enumerate(img_urls):
        response = requests.get(img_url)
        img = Image.open(BytesIO(response.content))
        img_path = os.path.join(download_dir, f"{topic.replace(' ', '_')}_{idx+1}.jpg")
        img.save(img_path)
        print(f"Saved: {img_path}")