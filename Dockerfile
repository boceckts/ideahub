FROM python:3.7.3-alpine3.8

COPY app /ideahub/app
COPY config.py /ideahub/config.py
COPY requirements.txt /ideahub/requirements.txt

WORKDIR /ideahub

RUN pip install virtualenv
RUN python -m venv flask
RUN source flask/bin/activate

RUN pip install -r requirements.txt

ENV FLASK_APP=app
ENV FLASK_ENV=production

RUN flask db init
RUN flask db migrate
RUN flask db upgrade
RUN flask initdb

ENTRYPOINT [ "flask", "run" ]
CMD ["--host=0.0.0.0"]
