FROM python:3.9.14
WORKDIR /usr/src/app

## Install packages
COPY . .
RUN pip install pipenv
RUN pipenv install --system --deploy --ignore-pipfile

## Copy all src files

## Run the application on the port 8080
EXPOSE 8000

# gunicorn 배포 명령어
# CMD ["gunicorn", "--bind", "허용하는 IP:열어줄 포트", "project.wsgi:application"]
CMD python manage.py runserver 0.0.0.0:8000 --settings=config.settings.production