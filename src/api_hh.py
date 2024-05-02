import requests


class ApiHH:
    def __init__(self):
        self.__base_url = "https://api.hh.ru/vacancies"
        self.__employers_dict = {'Северсталь': '6041',
                                 'Альфа-Банк': '80',
                                 'Тинькофф': '78638',
                                 'СБЕР': '3529',
                                 'Ozon': '2180',
                                 'Яндекс': '1740',
                                 'VK': '15478',
                                 'МТС': '3776',
                                 'СИНЕРГИЯ': '127256',
                                 '2ГИС': '64174'}

    def get_request(self, employer_id):
        try:
            params = {"per_page": 100,
                      "employer_id": employer_id,
                      "only_with_salary": True,
                      "only_with_vacancies": True}
            response = requests.get(self.__base_url, params=params)
            response.raise_for_status()
            return response.json()['items']

        except requests.exceptions.HTTPError as error:
            raise ConnectionError(f"Failed to access the site: {error}")

    def get_employers(self):
        employer_list = []
        for employer in self.__employers_dict:
            employer_info = self.get_request(self.__employers_dict[employer])
            for info in employer_info:
                employer_list.append({'employer': employer,
                                      'url': info['employer']['alternate_url']})
                break

        return employer_list

    def get_jobs(self):
        jobs_list = []
        for employer_id in self.__employers_dict:
            emp_jobs = self.get_request(self.__employers_dict[employer_id])
            for job in emp_jobs:
                if job['salary'] is None:
                    salary = 0
                elif job['salary']['from'] is None:
                    salary = job['salary']['to']
                elif job['salary']['to'] is None:
                    salary = job['salary']['from']
                else:
                    salary = (job['salary']['from'] + job['salary']['to']) / 2
                jobs_list.append({'job_title': job['name'],
                                  'city': job['area']['name'],
                                  'salary': salary,
                                  'currency': job['salary']['currency'],
                                  'description': job['snippet']['responsibility'],
                                  'publish_date': job['published_at'],
                                  'experience': job['experience']['name'],
                                  'job_url': job['alternate_url'],
                                  'employer_name': job['employer']['name']})
        return jobs_list
