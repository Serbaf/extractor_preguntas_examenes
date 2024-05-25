from uuid import uuid4
from selenium.webdriver.common.by import By
from logutils import get_logger
from .tools import do_with_delayed_retry, match_patterns, download_file
from ..utils.consts import (
    APP_NAME,
    DIR_PATTERNS,
    PDF_PATTERNS,
    OUTPUT_PATH
)


logger = get_logger(APP_NAME)


def magic_directories_journey(url, browser, output_path=OUTPUT_PATH):
    logger.info(f"Visiting {url}")
    browser.get(url)

    # Recorrer carpetas anidadas
    try:
        elems = do_with_delayed_retry(
            (browser.find_elements, 0.5, 15, False),
            By.XPATH,
            "//div[@class='mwc_ele_carpeta']"
        )
        elems = filter(lambda x: match_patterns(x, DIR_PATTERNS), elems)
        links = [e.find_element(By.XPATH, "./a").get_attribute("href") for e in elems]
        for link in links:
            browser.execute_script("window.open('');")
            browser.switch_to.window(browser.window_handles[-1])
            magic_directories_journey(link, browser)
            browser.close()
            browser.switch_to.window(browser.window_handles[0])
    except Exception:
        logger.exception(f"Something failed at URL {url}")

    
    # Recorrer PDFs
    elems = do_with_delayed_retry(
        (browser.find_elements, 0.5, 15, False),
        By.XPATH,
        "//a[contains(@href,'.pdf')]"
    )
    elems = filter(lambda x: match_patterns(x, PDF_PATTERNS), elems)
    links = [e.get_attribute("href") for e in elems]
    for link in links:
        download_file(link, output_path, f"{uuid4()}.pdf")