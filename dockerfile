FROM ubuntu
COPY prog.py .
RUN apt update
RUN apt-get install python3 -y
