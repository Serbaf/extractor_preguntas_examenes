import json
import typer
import pandas as pd
from typing import Annotated
from datetime import datetime
from sqlalchemy import text
from sqlalchemy.orm import Session


from logutils import get_logger
from exam_question_downloader.scraping.tools import (
    initialize_webdriver,
)
from exam_question_downloader.utils.consts import (
    APP_NAME,
    CONFIG_F,
)
from exam_question_downloader.db.db_tools import DatabaseClient
from exam_question_downloader.mail.mail import send_email
from exam_question_downloader.scraping.navigation import scrape_course_weeks
from exam_question_downloader.scraping.tools import normalize_string


logger = get_logger(APP_NAME)
db_client = DatabaseClient(CONFIG_F)
config = json.loads(CONFIG_F.read_text())
app = typer.Typer()


@app.command()
def main(
    color_logs: Annotated[
        bool,
        typer.Option(help="Color the logs. Good for stdout but not so much for mail."),
    ] = True,
):
    global logger
    if color_logs is False:
        for h in logger.handlers:
            logger.removeHandler(h)
    logger = get_logger(APP_NAME, colored=False)

    # Scrape data about course weeks
    with initialize_webdriver(use_browser=False) as browser:
        df = scrape_course_weeks(browser)

    # Check which courses should be fixed
    now = datetime.now()
    edx_cursos = pd.read_sql(
        "SELECT * FROM EDX_CURSOS", con=db_client.dbs["DBHIST"]["engine"]
    )
    cursos_actuales = edx_cursos[
        (edx_cursos["end_date"] >= now) & (edx_cursos["platform_id"] == "EDXORG")
    ]
    cursos_actuales = cursos_actuales.sort_values("end_date").drop_duplicates(
        "title", keep="last"
    )
    cursos_actuales = cursos_actuales[["course_id", "title", "weeks"]].rename(
        {"weeks": "num_modules"}, axis=1
    )
    cursos_actuales["normalized_title"] = cursos_actuales["title"].apply(
        lambda x: normalize_string(x)
    )

    aux_df = df.copy(deep=True)
    course_title_correspondence = pd.read_sql(
        "SELECT * FROM course_title_correspondence",
        con=db_client.dbs["DBHIST"]["engine"],
    )
    aux_df = pd.merge(
        aux_df,
        course_title_correspondence,
        left_on="index",
        right_on="edx_title",
        how="left",
    )
    aux_df["title"] = aux_df.apply(
        lambda x: x["db_title"] if not pd.isna(x["db_title"]) else x["title"], axis=1
    )
    aux_df["normalized_title"] = aux_df["title"].apply(lambda x: normalize_string(x))
    merge_df = aux_df.merge(cursos_actuales, on="normalized_title", how="left")
    merge_df["weeks"] = merge_df["weeks"].astype(int)
    merge_df = merge_df[~(merge_df["weeks"] == merge_df["num_modules"])]
    fixable_courses = merge_df[~merge_df["course_id"].isna()]

    # Fix everything fixable
    fixable_courses_html = ""
    with Session(db_client.dbs["DBHIST"]["engine"]) as session:
        for _, row in fixable_courses.iterrows():
            logger.info(
                f"Changing number of weeks for course {row['index']}: {row['num_modules']}->{row['weeks']}"
            )
            cmd = text(
                f"""UPDATE EDX_CURSOS SET weeks={row["weeks"]} WHERE COURSE_ID='{row["course_id"]}'"""
            )
            fixable_courses_html += (
                f"<li><b>{row['index']} ({row['num_modules']}->{row['weeks']})</b></li>"
            )
            session.execute(cmd)
        session.commit()

    # Check which courses are unfixable
    merge_df = aux_df.merge(cursos_actuales, on="normalized_title", how="left")
    merge_df["weeks"] = merge_df["weeks"].astype(int)
    unfixable_courses = merge_df[merge_df["course_id"].isna()]

    # Send email asking to fix the broken courses
    if len(unfixable_courses) > 0 or len(fixable_courses) > 0:
        unfixable_courses_html = ""
        for _, row in unfixable_courses.iterrows():
            unfixable_courses_html += f"""<li><b>{row["index"]}</b></li>"""
        mail_html = f"""
        <div>
            <p>Saludos, mi señor,</p>
            <p>Los siguientes cursos han sido actualizados en su número de horas:
                <ul>
                    {fixable_courses_html}
                </ul>
            </p>
        
            <p>Los siguientes cursos afectados no han podido ser corregidos, probablemente debido a que no coincide el título de su ficha en edx.org con el registro en BD:
                <ul>
                    {unfixable_courses_html}
                </ul>
            </p>
            <p>Necesitarás encontrar la correspondencia real entre los títulos e introducirla en la tabla COURSE_TITLE_CORRESPONDENCE siguiendo este ejemplo:<p>
            <p><i>INSERT INTO COURSE_TITLE_CORRESPONDENCE (EDX_TITLE, DB_TITLE) VALUES ('UPValenciaX: Math Fundamentals: Algebra', 'Basic Maths: Algebra');</i></p>
        """
        logger.info("Sending email asking for manual fixing of some courses")
        send_email(
            sender_header=config["mailing"]["sender"],
            real_sender=config["mailing"]["real_sender"],
            recipients=[config["maintainer"]["email"]],
            subject="Revisión manual de semanas de cursos",
            bodytxt="",
            bodyhtml=mail_html,
            replyto=config["mailing"]["reply_address"],
        )
    else:
        logger.info("No need to fix anything, not sending email")


if __name__ == "__main__":
    app()
