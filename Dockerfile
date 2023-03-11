FROM python:3.11.2
EXPOSE 5000
WORKDIR /app


RUN apt-get update \
     && apt-get install -y libgl1-mesa-glx \
     && apt-get -y install tesseract-ocr 
RUN pip install --upgrade pip
RUN pip install flask
RUN pip install pytesseract
RUN pip install matplotlib
RUN pip install opencv-python
RUN pip install numpy
RUN pip install flask-smorest
RUN pip install python-dotenv
RUN pip install flask-sqlalchemy
RUN pip install marshmallow
RUN pip install flask-migrate
RUN pip install flask-jwt-extended
RUN pip install passlib

COPY . .
CMD ["flask","run","--host","0.0.0.0"]