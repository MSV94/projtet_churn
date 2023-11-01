FROM debian:latest
RUN apt-get update && apt-get install python3-pip -y && pip3 install requests && pip3 install python-time
ADD get.py /home/get.py
WORKDIR /home
CMD python3 get.py