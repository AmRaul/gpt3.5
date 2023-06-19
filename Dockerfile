FROM python:3
COPY . /gpt

WORKDIR /gpt

RUN pip install -r requirements.txt

CMD [ "python", "main.py" ]