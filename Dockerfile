FROM python:3.10-alpine
ADD . /
WORKDIR /
RUN pip3 install -r requirements.txt
CMD ["python3", "-u", "main.py"]
