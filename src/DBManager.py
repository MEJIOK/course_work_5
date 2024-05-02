import re
import psycopg2


class DatabaseManager:
    """
    Class for interacting with the database
    """

    def __init__(self, params, db_name):
        self.params = params
        self.db_name = db_name.lower()

    def create_database(self):
        """
        Create a database
        """

        if not re.match(r'^[a-zA-Z0-9_]+$', self.db_name):
            raise ValueError("Database name should only contain letters, numbers, and underscores.")
        else:
            conn = psycopg2.connect(dbname='postgres', **self.params)
            conn.autocommit = True
            cur = conn.cursor()

            try:
                cur.execute(f"DROP DATABASE IF EXISTS {self.db_name}")
                cur.execute(f"CREATE DATABASE {self.db_name}")
                conn.close()

            except (psycopg2.DatabaseError, psycopg2.OperationalError, psycopg2.errors.InvalidCatalogName) as e:
                print(f"Error creating database: {e}")

    def create_db_tables(self):
        """
        Create 'companies' and 'vacancies' tables in the created database
        """

        try:
            with psycopg2.connect(dbname=self.db_name, **self.params) as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT true FROM pg_catalog.pg_database WHERE datname = %s", (self.db_name,))
                    if not cur.fetchone():
                        raise Exception(f"Database {self.db_name} not found.")

                    cur.execute("""
                        CREATE TABLE employers (
                        employer_id SERIAL PRIMARY KEY,
                        employer_name VARCHAR(100) UNIQUE,
                        employer_url VARCHAR(250)
                        )
                        """)

                    cur.execute("""
                        CREATE TABLE jobs (
                        job_id SERIAL PRIMARY KEY,
                        job_title VARCHAR(100) not null,
                        city VARCHAR(255),
                        salary INT,
                        currency VARCHAR(10),
                        description TEXT,
                        publish_date DATE,
                        experience TEXT,
                        job_url VARCHAR(250),
                        employer_name VARCHAR(100) REFERENCES employers(employer_name) NOT NULL,
                        foreign key(employer_name) REFERENCES employers(employer_name)
                        )
                        """)
            conn.close()

        except psycopg2.Error as e:
            print(f"Error creating tables: {e}")

    def save_data_to_db(self, employers_data, jobs_data):
        """
        Save information to the database tables
        """

        try:
            with psycopg2.connect(dbname=self.db_name, **self.params) as conn:
                with conn.cursor() as cur:
                    for employer in employers_data:
                        cur.execute(
                            f"INSERT INTO employers(employer_name, employer_url) VALUES (%s, %s)",
                            (employer['employer'], employer['url'])
                        )
                    for job in jobs_data:
                        cur.execute(
                            f"INSERT INTO jobs(job_title, city, salary, currency, description, "
                            f"publish_date, experience, job_url, employer_name) "
                            f"VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                            (
                                job['job_title'],
                                job['city'],
                                int(job['salary']),
                                job['currency'],
                                job['description'],
                                job['publish_date'],
                                job['experience'],
                                job['job_url'],
                                job['employer_name']
                            )
                        )
                    conn.commit()
        except psycopg2.Error as e:
            print(f"Error filling tables: {e}")
            conn.rollback()
        finally:
            if conn is not None:
                conn.close()

    def get_employers_and_jobs_count(self):
        """
        Get a list of all employers and
        the number of jobs at each company
        """

        try:
            with psycopg2.connect(dbname=self.db_name, **self.params) as conn:
                with conn.cursor() as cur:
                    cur.execute('SELECT employer_name, COUNT(job_title) from jobs GROUP BY employer_name')
                    result = cur.fetchall()
            conn.close()
            return result

        except psycopg2.Error as e:
            print(f"Error getting a list of all employers and the number of jobs at each company: {e}")

    def get_all_jobs(self):
        """
        Get a list of all jobs
        """

        try:
            with psycopg2.connect(dbname=self.db_name, **self.params) as conn:
                with conn.cursor() as cur:
                    cur.execute('SELECT * from jobs')
                    result = cur.fetchall()
            conn.close()
            return result

        except psycopg2.Error as e:
            print(f"Error getting a list of all jobs: {e}")

    def get_avg_salary(self):
        """
        Get the average salary for jobs
        """

        try:
            with psycopg2.connect(dbname=self.db_name, **self.params) as conn:
                with conn.cursor() as cur:
                    cur.execute('SELECT avg(salary) FROM jobs ')
                    result = cur.fetchall()
            conn.close()
            return result

        except psycopg2.Error as e:
            print(f"Error getting the average salary for jobs: {e}")

    def get_jobs_with_higher_salary(self):
        """
        Get a list of all jobs with a salary higher
        than the average salary for all jobs
        """

        try:
            with psycopg2.connect(dbname=self.db_name, **self.params) as conn:
                with conn.cursor() as cur:
                    cur.execute('SELECT job_title, salary, currency, job_url, experience  FROM jobs '
                                'WHERE salary > (SELECT AVG(salary) FROM jobs)'
                                'ORDER BY job_title DESC')
                    result = cur.fetchall()
            conn.close()
            return result

        except psycopg2.Error as e:
            print(f"Error getting a list of all jobs with a salary higher than the average salary: {e}")

    def get_jobs_with_keyword(self, keyword):
        """
        Get a list of all jobs with the given keyword in the job title
        """

        try:
            with psycopg2.connect(dbname=self.db_name, **self.params) as conn:
                with conn.cursor() as cur:
                    cur.execute(f"SELECT job_title, salary, currency, job_url, experience FROM jobs "
                                f"WHERE job_title LIKE '%{keyword.capitalize()}%'")
                    result = cur.fetchall()
                    if len(result) == 0:
                        return ["No jobs found"]
            conn.close()
            return result

        except psycopg2.Error as e:
            print(f"Error getting a list of all jobs by keyword: {e}")
