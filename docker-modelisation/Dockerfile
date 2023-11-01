FROM debian:latest
RUN apt-get update && apt-get install python3-pip -y && pip3 install requests && pip3 install python-time
ADD modelisation.py /home/modelisation.py
WORKDIR /home
CMD python3 modelisation.py