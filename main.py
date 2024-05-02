from src.config_settings import read_config
from src.api_hh import ApiHH
from src.DBManager import DatabaseManager


def main():

    # Create an object of the JobAPI class to get data via API
    job_api_response = ApiHH()

    # Get a list of available companies
    employers_data = job_api_response.get_employers()

    # Get a list of available jobs
    jobs_data = job_api_response.get_jobs()

    # Create an object of the DatabaseManager class to work with the PostgreSQL database
    db_manager = DatabaseManager(read_config(), 'CompanyJobs')

    # Create a database
    db_manager.create_database()

    # Create tables in the database
    db_manager.create_db_tables()

    # Fill tables in the database
    db_manager.save_data_to_db(employers_data, jobs_data)

    # Get a list of all employers and the number of jobs at each company
    all_employers_jobs = db_manager.get_employers_and_jobs_count()

    print("Getting a list of all employers and the number of jobs at each company: ")
    for value in all_employers_jobs:
        print(f"{value}")

    # Get a list of all jobs
    all_jobs = db_manager.get_all_jobs()

    print("\nGetting a list of all jobs: ")
    for value in all_jobs:
        print(f"{value}\n")

    # Get the average salary for jobs
    avg_salary = db_manager.get_avg_salary()

    print("\nGetting the average salary for jobs: ")
    for value in avg_salary:
        print(f"{value}\n")

    # Get a list of all jobs with a salary higher than the average salary
    higher_salary_jobs = db_manager.get_jobs_with_higher_salary()

    print("\nGetting a list of all jobs with a salary higher than the average salary: ")
    for value in higher_salary_jobs:
        print(f"{value}")

    # Get a list of all jobs with the given keyword in the job title
    keyword_jobs = db_manager.get_jobs_with_keyword('driver')
    print("\nGetting a list of all jobs by keyword: ")
    for value in keyword_jobs:
        print(f"{value}")


if __name__ == "__main__":
    main()
