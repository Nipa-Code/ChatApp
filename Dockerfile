FROM python:3.9-alpine
WORKDIR /chatapp
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt
EXPOSE 5001
COPY . .
CMD ["python3", "-m", "chatapp"]