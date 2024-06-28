import re
import io
import os
import fitz
import pytesseract
import pandas as pd
from PIL import Image
from logutils import get_logger
from ..utils.consts import APP_NAME, SUBJECTS_PATTERNS
from ..scraping.tools import match_patterns

rgx_question = re.compile(r"^\s*(\d{1,2})\s*[\.\)]\s*(.*?)\s*$")
rgx_answer_a = re.compile(r"^\s*([aA])\s*[\.\)]\s*(.*?)\s*$")
rgx_answer_b = re.compile(r"^\s*([bB])\s*[\.\)]\s*(.*?)\s*$")
rgx_answer_c = re.compile(r"^\s*([cC])\s*[\.\)]\s*(.*?)\s*$")
rgx_answer_d = re.compile(r"^\s*([dD])\s*[\.\)]\s*(.*?)\s*$")

logger = get_logger(APP_NAME)


def get_textpage_ocr(page):
    pix = page.get_pixmap()  # render page to an image
    img = Image.open(io.BytesIO(pix.tobytes()))  # convert the image for PIL
    text = pytesseract.image_to_string(img, lang="spa")
    return text


def extract_questions_from_doc(doc):
    doc_lines = [l for l in doc.split("\n") if l.strip() != ""]
    problems = []
    number = None
    question = ""
    a = ""
    b = ""
    c = ""
    d = ""
    for i, l in enumerate(doc_lines):
        if len(d) > 0:
            if m := rgx_question.match(l):
                logger.info(f"Adding question:\nQuestion:{question}\na:{a}\nb:{b}\nc:{c}\nd:{d}")
                problems.append({
                    "number": rgx_question.match(question).groups()[0].strip(),
                    "question": rgx_question.match(question).groups()[1].strip(),
                    "a": rgx_answer_a.match(a).groups()[1],
                    "b": rgx_answer_b.match(b).groups()[1],
                    "c": rgx_answer_c.match(c).groups()[1],
                    "d": rgx_answer_d.match(d).groups()[1]
                })
               
                question = l
                logger.info(f"Question: {question}")
                a = ""
                b = ""
                c = ""
                d = ""
            else:
                d = f"{d} {l}"
                logger.info(f"Appending to D: {l}")
        elif len(c) > 0:
            if m := rgx_answer_d.match(l):
                d = l
                logger.info(f"D: {d}")
            else:
                c = f"{c} {l}"
                logger.info(f"Appending to C: {l}")
        elif len(b) > 0:
            if m := rgx_answer_c.match(l):
                c = l
                logger.info(f"C: {c}")
            else:
                b = f"{b} {l}"
                logger.info(f"Appending to B: {l}")
        elif len(a) > 0:
            if m := rgx_answer_b.match(l):
                b = l
                logger.info(f"B: {b}")
            else:
                a = f"{a} {l}"
                logger.info(f"Appending to A: {l}")
        elif len(question) > 0:
            if m := rgx_answer_a.match(l):
                a = l
                logger.info(f"A: {a}")
            else:
                question = f"{question} {l}"
                logger.info(f"Appending to question: {question}")
        else:
            if m := rgx_question.match(l):
                question = l
                logger.info(f"Question: {question}")
            else:
                continue
    return problems

def get_text_docs_from_dir(doc_dir):
    text_docs = []
    for i, f in enumerate(doc_dir.iterdir()):
        if not f.is_file():
            continue
        text_doc = get_text_docs_from_file(f)
        text_docs.append((f.name, text_doc))
    return text_docs

def get_text_docs_from_file(f):
    logger.info(f"File {f}")
    text_doc = ""
    if f.suffix == ".pdf":
        doc = fitz.open(f)
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
    return text_doc


def classify_questions_by_subject(questions):
    aux = []
    for name, qd in questions:
        if len(qd) > 0:
            for q in qd:
                for x in ("question", "a", "b", "c", "d"):
                    if subject := match_patterns(q["question"], SUBJECTS_PATTERNS):
                        break
                    elif subject:= match_patterns(q["a"], SUBJECTS_PATTERNS):   # Para las preguntas que no tienen nada en el enunciado, p.ej.; "Señale la respuesta correcta:"
                        break
                q["doc"] = name
                q["subject"] = subject
                aux.append(q)
        else:
            pass
    df = pd.DataFrame(aux)
    df = df[~df["subject"].isna()]
    df.reset_index(drop=True)
    return df

def get_questions_not_classified(questions):
    aux = []
    for name, qd in questions:
        if len(qd) > 0:
            for q in qd:
                has_match=False
                for x in ("question", "a", "b", "c", "d"):
                    if subject := match_patterns(q["question"], SUBJECTS_PATTERNS):
                        has_match=True
                        break
                if not has_match:
                    q["doc"] = name
                    aux.append(q)
        else:
            pass
    df = pd.DataFrame(aux)
    df = df[df["subject"].isna()]
    df.reset_index(drop=True)
    return df