FROM tiangolo/uwsgi-nginx-flask:python3.11

COPY fenrirApp /fenrirApp/fenrirApp
COPY setup.py MANIFEST.in /fenrirApp/
COPY Docker /app
RUN apt update && apt install iptables openvpn -y
RUN pip3 install /fenrirApp

ENV STATIC_PATH /fenrirApp/fenrirApp/static/