FROM python:3.12-alpine

COPY requirements.txt /srv/requirements.txt
COPY entrypoint.sh /srv/entrypoint.sh
COPY schedulr /srv/schedulr

RUN pip install --upgrade pip
RUN pip install -r /srv/requirements.txt
RUN chmod +x /srv/entrypoint.sh

WORKDIR /srv

CMD ["/srv/entrypoint.sh"]
