FROM tiangolo/uwsgi-nginx-flask:python3.7

COPY ./requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt \
    && rm -rf /requirements.txt

COPY . /app
