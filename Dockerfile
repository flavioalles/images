FROM python:3.12.4

ADD . /images/
WORKDIR /images
RUN pip install poetry==1.8.2
RUN make install-app
ENV PYTHONPATH="${PYTHONPATH}:/images"

CMD ["make", "run-app"]