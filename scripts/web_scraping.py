import json
from typing import Dict
from parsel import Selector
from nested_lookup import nested_lookup
from playwright.sync_api import sync_playwright
import jmespath

def parse_thread(donnee: Dict) -> Dict:
    """
    Extrait le texte du post Thread à partir d'un dictionnaire de données JSON.

    Args:
        donnee (Dict): Dictionnaire de données JSON contenant les informations sur le post Thread.

    Returns:
        Dict: Dictionnaire contenant le texte du post Thread.
    """

    resultat = jmespath.search(
        """{
        text: post.caption.text
    }""",
        donnee,
    )
    return resultat

def scrape_thread(url: str, max_pages: int) -> dict:
    """
    Scrape les posts et les réponses sur Threads à partir d'une URL.
    """

    threads = []
    for page_num in range(1, max_pages + 1):
        with sync_playwright() as pw:
            navigateur = pw.chromium.launch()
            contexte = navigateur.new_context(viewport={"width": 1920, "height": 1080})
            page = contexte.new_page()

            page.goto(f"{url}?page={page_num}")
            page.wait_for_selector("[data-pressable-container=true]")
            selector = Selector(page.content())
            datasets_caches = selector.css('script[type="application/json"][data-sjs]::text').getall()

            for dataset_cache in datasets_caches:
                if '"ScheduledServerJS"' not in dataset_cache:
                    continue
                if "thread_items" not in dataset_cache:
                    continue
                donnee = json.loads(dataset_cache)

                thread_items = nested_lookup("thread_items", donnee)
                if not thread_items:
                    continue
                parsed_threads = [parse_thread(t) for thread in thread_items for t in thread]
                threads.extend(parsed_threads)
    return {
        "thread": threads[0]["text"],
        "reply": [reponse["text"] for reponse in threads[1:]],
    }
