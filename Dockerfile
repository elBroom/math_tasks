FROM ubuntu:16.04

RUN apt-get update && apt-get install -y python3-pip && \
    rm -rf /var/lib/apt/lists/* /var/cache/debconf && \
    apt-get clean

RUN mkdir /etc/app /var/log/app /var/run/app /usr/tmp

RUN pip3 install --upgrade \
	pip==9.0.1 \
	setuptools==36.5.0 \
	uwsgi==2.0.15

WORKDIR /usr/src/app
COPY . /usr/src/app

RUN pip3 install -r requirements.txt

EXPOSE 3040
ENTRYPOINT ["./deploy/entrypoint.sh"]
CMD ["uwsgi", "--ini","/etc/app/uwsgi.ini", "--http", ":3040"]

# docker build -t elbroom/math_tasks .
# docker push elbroom/math_tasks
# docker run --name math_tasks -d --rm -it --network host elbroom/math_tasks