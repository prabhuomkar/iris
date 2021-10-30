FROM pytorch/torchserve
ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
RUN scripts/download_model_weights.sh
RUN scripts/generate_model_archives.sh
EXPOSE 5002
CMD ["scripts/start.sh"]