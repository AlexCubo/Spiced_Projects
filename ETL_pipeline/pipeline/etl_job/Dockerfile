FROM python:3.8-slim 

WORKDIR /etl_code

COPY requirements.txt /etl_code

RUN pip install --trusted-host pypi.python.org -r requirements.txt

CMD ["python", "script_etl.py"]

