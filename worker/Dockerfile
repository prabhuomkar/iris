FROM python:3.8
ADD requirements.txt /requirements.txt
RUN pip install -r requirements.txt
COPY . /app
CMD ["python", "-u", "app/worker.py"]
