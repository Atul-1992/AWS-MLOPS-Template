FROM python:3.12

COPY ./app /src
RUN pip install -r requirements.txt

ENTRYPOINT [ "python3", "/src/run.py" ]