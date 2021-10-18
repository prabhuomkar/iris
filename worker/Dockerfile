FROM python:3.8
ADD requirements.txt /requirements.txt
RUN pip install -r requirements.txt
RUN apt-get update && apt-get install -y
RUN apt-get install libimage-exiftool-perl exiftool -y
COPY . /app
CMD ["python", "-u", "app/worker.py"]
