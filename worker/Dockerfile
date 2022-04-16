FROM python:3.9-slim
RUN apt update && \
    apt install --no-install-recommends -y build-essential gcc
ADD ./requirements.txt /requirements.txt
RUN pip install torch==1.9.0+cpu torchvision==0.10.0+cpu \
    -f https://download.pytorch.org/whl/torch_stable.html
RUN pip install --no-cache-dir -r /requirements.txt
COPY ./src /src
CMD ["python", "-u", "/src/app.py"]