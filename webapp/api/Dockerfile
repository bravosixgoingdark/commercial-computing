FROM python:3.13.3-slim

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt 

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt 

COPY . .

EXPOSE 5000

CMD ["python3", "api.py"]
