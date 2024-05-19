import requests
import re
import functools
import time
from pathlib import Path
from logutils import get_logger
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from ..utils.consts import APP_NAME

rgx_spaces = re.compile(r"\s+")
logger = get_logger(APP_NAME)

def match_patterns(html_elem, patterns):
    if isinstance(html_elem, str):
        text = html_elem
    else:
        text = html_elem.text
    for rgx in patterns:
        if rgx.match(text):
            return True
    return False

def do_with_delayed_retry(setup, *args):
    func, delay, retries, incremental = setup
    counter = 0
    while True:
        try:
            res = func(*args)
        except Exception as e:
            if counter > retries:
                raise Exception(e)
            counter += 1
            time.sleep(delay)
            if incremental:
                delay *= pow(delay, 2)
        else:
            break
    return res


def initialize_webdriver(use_browser=True):
    ff_opts = Options()
    if not use_browser:
        ff_opts.add_argument("--headless")
    browser = Firefox(options=ff_opts)
    return browser


def normalize_string(text: str) -> str:
    text = text.strip().lower()
    text = rgx_spaces.sub(" ", text)
    return text

def incremental_retry(exception, initial_delay=1, max_delay=30):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            args_repr = [repr(a) for a in args]
            kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
            signature = ", ".join(args_repr + kwargs_repr)
            delay = initial_delay
            while True:
                try:
                    return func(*args, **kwargs)
                except exception:
                    logger.info((
                        f"Function {func.__name__}({signature}) failed. "
                        f"Retrying after delay of {delay}s..."
                    ))
                    if delay > max_delay:
                        raise MaxDelayedRetriesReachedError(
                            f"Max delay ({max_delay}s) reached"
                        )
                    time.sleep(delay)
                    delay = delay * 2
                except Exception:
                    logger.exception("Unexpected exception")

        return wrapper

    return decorator


def download_file(url: str, directory: Path, filename: str):
    # Ensure the directory exists
    directory.mkdir(parents=True, exist_ok=True)

    # Create the full path for the file
    file_path = directory.joinpath(filename)

    # Send a GET request to the URL
    response = requests.get(url, stream=True)

    # Check if the request was successful
    if response.status_code == 200:
        # Open the file path for writing in binary mode
        with open(file_path, 'wb') as f:
            # Write the contents of the response to the file
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        logger.info(f"File downloaded successfully: {file_path}")
    else:
        logger.warning(f"Failed to download file: status code {response.status_code}")


class MaxDelayedRetriesReachedError(Exception):
    pass