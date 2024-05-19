import re
import io
import os
import fitz
import pytesseract
from PIL import Image
from logutils import get_logger
from ..utils.consts import APP_NAME

rgx_question = re.compile(r"\s*(\d{1,2})\s*[\.\)](.+)")
rgx_answer_a = re.compile(r"\s*([aA])\s*[\.\)](.+)")
rgx_answer_b = re.compile(r"\s*([bB])\s*[\.\)](.+)")
rgx_answer_c = re.compile(r"\s*([cC])\s*[\.\)](.+)")
rgx_answer_d = re.compile(r"\s*([dD])\s*[\.\)](.+)")

logger = get_logger(APP_NAME)


def get_textpage_ocr(page):
    pix = page.get_pixmap()  # render page to an image
    img = Image.open(io.BytesIO(pix.tobytes()))  # convert the image for PIL
    text = pytesseract.image_to_string(img, lang="spa")
    return text


def extract_questions_from_doc(doc):
    doc_lines = [l for l in doc.split("\n") if l.strip() != ""]
    problems = []
    number = ""
    question = ""
    a = ""
    b = ""
    c = ""
    d = ""
    for i, l in enumerate(doc_lines):
        if len(d) > 0:
            if (m := rgx_question.match(l)) and (len(m.groups()) >=2):
                logger.info(f"Appending to Question")
                problems.append({"number": number, "question": question, "a": a, "b": b, "c": c, "d": d})
               
                number = m.groups()[1]
                question = m.groups()[2]
                a = ""
                b = ""
                c = ""
                d = ""
            else:
                logger.info(f"Appending to D")
                d += l
        elif len(c) > 0:
            if rgx_answer_d.match(l):
                logger.info(f"Appending to D")
                d = l
            else:
                logger.info(f"Appending to C")
                c += l
        elif len(b) > 0:
            if rgx_answer_c.match(l):
                logger.info(f"Appending to C")
                c = l
            else:
                logger.info(f"Appending to B")
                b += l
        elif len(a) > 0:
            if rgx_answer_b.match(l):
                logger.info(f"Appending to B")
                b = l
            else:
                logger.info(f"Appending to A")
                a += l
        elif len(question) > 0:
            if rgx_answer_a.match(l):
                logger.info(f"Appending to A")
                a = l
            else:
                logger.info(f"Appending to Question")
                question += l
        else:
            if rgx_question.match(l):
                logger.info(f"Appending to Question")
                question = l
            else:
                continue
    return problems

def get_text_docs_from_dir(doc_dir):
    text_docs = []
    for i, f in enumerate(doc_dir.iterdir()):
        if not f.is_file():
            continue
        logger.info(f"File {f}")
        if f.suffix == ".pdf":
            doc = fitz.open(f)
            text_doc = ""
            for page in doc:
                page_text = ""
                page_text = page.get_text()
                # If no text, try with OCR
                if page_text.strip() == "":
                    logger.info(f"OCR for {f}!")
                    break
                    # page_text = get_textpage_ocr(page)
                else:
                    text_doc += page_text
        else:
            text_doc = f.read_text()
        text_docs.append((f.name, text_doc))
    return text_docs