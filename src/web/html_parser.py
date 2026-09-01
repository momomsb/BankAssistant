from urllib.parse import urlparse

from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

urls = ["https://www.attijariwafabank.com/fr/profil/particulier/ouvrir-un-compte-bancaire-en-ligne",
       "https://www.attijariwafabank.com/fr/profil/tpe/ouvrir-un-compte-bancaire-en-ligne",
       "https://www.attijariwafabank.com/fr/profil/mre/ouvrir-un-compte-bancaire-en-ligne"]

NOISE_TAGS = ["script", "style", "noscript", "nav", "header", "footer", "svg", "form", "iframe"]


def output_path_for_url(url):
    segments = [s for s in urlparse(url).path.split("/") if s]
    profil = segments[2] if len(segments) > 2 else "page"
    return f"documents/ouvrir-compte-{profil}.txt"


def extract_main_text(html):
    soup = BeautifulSoup(html, "html.parser")

    for tag in soup.find_all(NOISE_TAGS):
        tag.decompose()

    content = soup.find("main") or soup.body or soup

    lines = [line for line in content.get_text(separator="\n", strip=True).split("\n") if line]

    deduped_lines = []
    for line in lines:
        if not deduped_lines or deduped_lines[-1] != line:
            deduped_lines.append(line)

    return "\n".join(deduped_lines)


with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)

    for url in urls:
        page = browser.new_page()
        try:
            page.goto(url, timeout=60000, wait_until="domcontentloaded")

            html = page.content()
            text = extract_main_text(html)

            out_path = output_path_for_url(url)
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(text)
            print(f"{url} -> {out_path} ({len(text)} caracteres)")
        except Exception as e:
            print(f"Echec sur {url}: {e}")
        finally:
            page.close()

    browser.close()


print("OK")