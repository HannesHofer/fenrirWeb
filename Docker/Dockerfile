FROM tiangolo/uwsgi-nginx-flask:python3.11

COPY fenrirWeb /fenrirWeb/fenrirWeb
COPY setup.py MANIFEST.in /fenrirWeb/
COPY Docker /app
RUN apt update && apt install iptables openvpn -y
RUN pip3 install /fenrirWeb

ENV STATIC_PATH /fenrirWeb/fenrirWeb/static/