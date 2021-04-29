FROM python:3.7.10-slim-buster
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
RUN pip install /app
EXPOSE 8000
CMD python -m users 
