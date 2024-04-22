 
import json
from typing import Dict

import jmespath
from parsel import Selector
from nested_lookup import nested_lookup
from playwright.sync_api import sync_playwright


def parse_thread(data: Dict) -> Dict:
    """Parse Threads JSON dataset for the most important fields. """

    result = jmespath.search(
        """{
        text: post.caption.text,
        # username: post.user.username
    }""",
        data,
    )
    return result


def scrape_thread(url: str) -> dict:
    """Scrape Threads post and replies from a given URL. """

    with sync_playwright() as pw:
        # start Playwright browser
        browser = pw.firefox.launch()
        context = browser.new_context(viewport={"width": 1920, "height": 1080})
        page = context.new_page()

        # go to url and wait for the page to load
        page.goto(url)
        # wait for page to finish loading
        page.wait_for_selector("[data-pressable-container=true]")
        # find all hidden datasets
        selector = Selector(page.content())
        hidden_datasets = selector.css('script[type="application/json"][data-sjs]::text').getall()
        # find datasets that contain threads data
        for hidden_dataset in hidden_datasets:
            # skip loading datasets that clearly don't contain threads data
            if '"ScheduledServerJS"' not in hidden_dataset:
                continue
            if "thread_items" not in hidden_dataset:
                continue
            data = json.loads(hidden_dataset)
            # datasets are heavily nested, use nested_lookup to find 
            # the thread_items key for thread data
            thread_items = nested_lookup("thread_items", data)
            if not thread_items:
                continue
            # use our jmespath parser to reduce the dataset to the most important fields
            threads = [parse_thread(t) for thread in thread_items for t in thread]
            return {
                # the first parsed thread is the main post:
                "thread": threads[0],
                # other threads are replies:
                "replies": threads[1:]
            }
        raise ValueError("could not find thread data in page")


if __name__ == "__main__":
    print(scrape_thread("https://www.threads.net/"))