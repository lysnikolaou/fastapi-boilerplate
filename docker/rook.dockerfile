FROM python:3.9

RUN pip install "uvicorn[standard]" gunicorn

COPY ./requirements.txt /requirements.txt
RUN pip install -r requirements.txt

COPY ./docker/start.sh /start.sh
RUN chmod +x /start.sh

COPY ./docker/gunicorn_conf.py /gunicorn_conf.py

COPY ./docker/start-reload.sh /start-reload.sh
RUN chmod +x /start-reload.sh

COPY ./rook /rook

EXPOSE 8000

# Run the start script, it will check for an /app/prestart.sh script (e.g. for migrations)
# And then will start Gunicorn with Uvicorn
CMD ["/start.sh"]
