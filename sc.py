from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import pandas as pd

chrome_options = Options()
chrome_options.add_argument("--headless") 
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

url = "https://www.example.com/pages/stores"
driver.get(url)

try:
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "store-card"))
    )
    print("Contenu chargé avec succès !")
except:
    print("Temps d'attente dépassé, les magasins ne sont pas visibles.")

html_content = driver.page_source
soup = BeautifulSoup(html_content, "html.parser")

stores = soup.find_all("div", class_="store-card")

print(f"Nombre de magasins trouvés : {len(stores)}")

for store in stores:
    name = store.find("h3").text.strip() if store.find("h3") else "N/A"
    address = [span.text.strip() for span in store.find_all("span") if span.text.strip()]
    latitude = store.get("data-lat", "N/A")
    longitude = store.get("data-lng", "N/A")
    
    print("\n // Magasin trouvé :")
    print(f"Nom       : {name}")
    print(f"Adresse   : {', '.join(address)}")
    print(f"Latitude  : {latitude}")
    print(f"Longitude : {longitude}")

driver.quit()

store_data = []

for store in stores:
    name = store.find("h3").text.strip() if store.find("h3") else "N/A"
    address = [span.text.strip() for span in store.find_all("span") if span.text.strip()]
    latitude = store.get("data-lat", "N/A")
    longitude = store.get("data-lng", "N/A")
    
    store_data.append({
        "Nom": name,
        "Adresse": ", ".join(address),
        "Latitude": latitude,
        "Longitude": longitude
    })

df = pd.DataFrame(store_data)

df.to_excel("magasins.xlsx", index=False)

print("Fichier Excel généré : magasins.xlsx")