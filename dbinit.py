import os
import sys

import psycopg2 as dbapi2


INIT_STATEMENTS = [
    """GRANT CONNECT ON DATABASE d41ek2217p7u99 TO kvwrgkebshegcf;""",
    """CREATE SCHEMA IF NOT EXISTS PUBLIC;""",
    """GRANT USAGE ON SCHEMA PUBLIC TO kvwrgkebshegcf;""",
    """GRANT SELECT,INSERT,UPDATE,DELETE ON ALL TABLES IN SCHEMA PUBLIC TO kvwrgkebshegcf;""",
    """GRANT USAGE ON ALL SEQUENCES IN SCHEMA PUBLIC TO kvwrgkebshegcf;""",
    """GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA PUBLIC TO kvwrgkebshegcf;""",
    """CREATE TABLE IF NOT EXISTS PUBLIC.STUDENT (
        "Student_Mail" varchar(200) NOT NULL,
        "Name_Surname" varchar(200) NOT NULL,
        "Password" varchar(200) NOT NULL,
        "University" varchar(200) NOT NULL,
        "Age" INT NOT NULL,
        PRIMARY KEY("Student_Mail")
        );""",
    """CREATE TABLE IF NOT EXISTS PUBLIC.AGENCY (
        "mersis_no" varchar(200) NOT NULL,
        "name" varchar(200) NOT NULL,
        "office_location" varchar(200) NOT NULL,
        "password" varchar(200) NOT NULL,
        PRIMARY KEY("mersis_no")
        );""",
    """CREATE TABLE IF NOT EXISTS PUBLIC.JOB (
        "job_ıd" serial NOT NULL,
        "job_location" varchar(200) NOT NULL,
        "work_date" varchar(200) NOT NULL,
        "number_of_students" INT NOT NULL,
        "nececity_language" varchar(50),
        "mersis_no" varchar(200) NOT NULL,
        "wage" INT NOT NULL,
        "work_time" varchar(50) NOT NULL,
        "work_days" varchar(200) NOT NULL,
        PRIMARY KEY("job_ıd"),
        FOREIGN KEY("mersis_no") REFERENCES AGENCY("mersis_no")
        );""",
    """CREATE TABLE IF NOT EXISTS PUBLIC.JOB_REQUEST (
        "request_ıd" serial NOT NULL,
        "Student_Mail" varchar(200) NOT NULL,
        "mersis_no" varchar(200) NOT NULL,
        "job_ıd" serial NOT NULL,
        "checks" varchar(200) NOT NULL,
        PRIMARY KEY("request_ıd"),
        FOREIGN KEY("Student_Mail") REFERENCES STUDENT("Student_Mail"),
        FOREIGN KEY("mersis_no") REFERENCES AGENCY("mersis_no"),
        FOREIGN KEY("job_ıd") REFERENCES JOB("job_ıd")
        );""",
    """CREATE TABLE IF NOT EXISTS PUBLIC.LAN_TABLE (
        "Lan_Id" serial NOT NULL,
        "Student_Mail" varchar(200) NOT NULL,
        "Ekstra_Language" varchar(50) NOT NULL,
        PRIMARY KEY("Lan_Id"),
        FOREIGN KEY("Student_Mail") REFERENCES STUDENT("Student_Mail")
        );"""
]


def initialize(url):
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        for statement in INIT_STATEMENTS:
            cursor.execute(statement)
        cursor.close()


if __name__ == "__main__":
    url = "postgres://kvwrgkebshegcf:aa87eb5072319ace108142f5e23255e66768ea1e77e76db8fbd9480de4fcf13a@ec2-34-202-5-87.compute-1.amazonaws.com:5432/d41ek2217p7u99"
    if url is None:
        print("Usage: DATABASE_URL=url python dbinit.py", file=sys.stderr)
        sys.exit(1)
    initialize(url)
