import textwrap
import pandas

def format_question(q):
    ANCHO=120
    question='' if pandas.isna(q.question) else textwrap.fill(q.question, width=ANCHO)
    opcion_a='' if pandas.isna(q.a) else textwrap.fill(q.a, width=ANCHO)
    opcion_b='' if pandas.isna(q.b) else textwrap.fill(q.b, width=ANCHO)
    opcion_c='' if pandas.isna(q.c) else textwrap.fill(q.c, width=ANCHO)
    opcion_d='' if pandas.isna(q.d) else textwrap.fill(q.d, width=ANCHO)
    result=f"{question}\n  a) {opcion_a}\n  b) {opcion_b}\n  c) {opcion_c}\n  d) {opcion_d}"
    return result

def format_questions(questions):
    result=""
    for q in questions.itertuples(index=True, name='Pandas'):
        result=result + format_question(q) + "\n\n"
    return result