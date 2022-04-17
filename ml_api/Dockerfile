FROM thespaghettidetective/ml_api:base-1.1
WORKDIR /app
EXPOSE 50051

ADD ./model/model.weights.url /app/model/model.weights.url
RUN wget --quiet -O model/model.weights $(cat model/model.weights.url | tr -d '\r')

ADD requirements.txt /app/requirements.txt

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ADD . /app

CMD ["python", "grpc_server.py"]