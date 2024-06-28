import textwrap

def format_question(q):
    ANCHO=120
    result=f"{textwrap.fill(q.question, width=ANCHO)}\n  a) {textwrap.fill(q.a, width=ANCHO)}\n  b) {textwrap.fill(q.b, width=ANCHO)}\n  c) {textwrap.fill(q.c, width=ANCHO)}\n  d) {textwrap.fill(q.d, width=ANCHO)}"
    return result

def format_questions(questions):
    result=""
    for q in questions.itertuples(index=True, name='Pandas'):
        result=result + format_question(q) + "\n\n"
    return result