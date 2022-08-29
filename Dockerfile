FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /home/python/app

COPY Pipfile Pipfile.lock /home/python/app/
RUN pip install importlib_metadata pandas psycopg2-binary debugpy
RUN pip install pipenv && pipenv install --system

COPY ./app /home/python/app/
# CMD [ "flask", "run", "-h", "0.0.0.0", "-p", "5000"]
CMD ["python", "-m", "debugpy", "--wait-for-client", "--listen", "0.0.0.0:5678", "-m", "flask", "run", "-h", "0.0.0.0", "-p", "5000"]
