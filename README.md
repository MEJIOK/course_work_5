# Проект по БД
В рамках проекта вам необходимо получить данные о компаниях и вакансиях с сайта hh.ru,
спроектировать таблицы в БД PostgreSQL и загрузить полученные данные в созданные таблицы.
# Для работы потребуется:
1. Установить PostgresSQL https://www.postgresql.org/download/
2. Установить Pycharm https://www.jetbrains.com/pycharm/download/?section=windows

- В терминале введите команду 
```ini
git clone https://github.com/MEJIOK/course_work_5
```
- Создайте виртуальное окружение:
```ini
python3 -m venv venv
```
- Активируйте виртуальное окружение:
```ini
source venv/Scripts/activate
```
- Установите модули из файла ___requirements.txt___ :
```ini
pip install -r requirements.txt
```
- В папке проекта ___src___ cоздайте ___database.ini___ конфигурационный файл с вашими параметрами подключения к БД.

Пример файла:
```ini
[postgresql]
host=localhost
user=postgres
password=862486248
port=5432
```