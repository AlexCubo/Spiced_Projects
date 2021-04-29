FROM python:3.8-slim
WORKDIR /slack
COPY requirements.txt /slack
RUN pip install --trusted-host pypi.python.org -r requirements.txt
CMD ["python", "slack_bot.py"]
