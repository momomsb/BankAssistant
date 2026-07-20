from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

urls = ["https://www.attijariwafabank.com/fr/profil/mre/ouvrir-un-compte-bancaire-en-ligne",
       "https://www.attijariwafabank.com/fr/profil/tpe/ouvrir-un-compte-bancaire-en-ligne",
       "https://www.attijariwafabank.com/fr/profil/mre/ouvrir-un-compte-bancaire-en-ligne"]
#url=[,,]
with sync_playwright() as p:
    
    browser = p.chromium.launch(headless=True)

    for url in urls:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto(url)
        page.wait_for_load_state("networkidle")

        html = page.content()
        soup = BeautifulSoup(html, "html.parser")
        text = soup.get_text(separator="\n", strip=True)
        print(text)
        with open("documents/ouvrir-un-compte-bancaire-en-ligne.txt","a",encoding="utf-8") as f:
            f.write(text)
            f.write("\n\n")
    
    browser.close()


print("OK")