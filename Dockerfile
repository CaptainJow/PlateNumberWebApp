FROM python:3.11.2
WORKDIR /app


RUN apt-get update \
     && apt-get install -y libgl1-mesa-glx \
     && apt-get -y install tesseract-ocr 
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt


COPY . .
CMD ["gunicorn","--bind","0.0.0.0:80","app:create_app()"]