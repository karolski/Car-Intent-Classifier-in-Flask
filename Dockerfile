FROM python:3.6
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN pip install -r requirements.txt
COPY . /code/
ENV PORT=8080
EXPOSE $PORT
CMD gunicorn -w 1 -b 0.0.0.0:$PORT --timeout 90 app:app
