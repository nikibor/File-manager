FROM python:3

ENV PYTHONBUFFERED 1
RUN mkdir /code
WORKDIR /code
RUN ls
COPY . /code
RUN pip install -r requirements.txt
RUN ls
CMD python app/manage.py migrate
CMD python app/manage.py runserver localhost:8000