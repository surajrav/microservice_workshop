FROM python:3.12

COPY ./requirements.txt /code/app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/app/requirements.txt

COPY . /code/app/

WORKDIR /code

CMD ["./app/app_init.sh"]
