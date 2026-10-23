FROM python:3.12-slim

WORKDIR /projects/Postit!

COPY . .

RUN pip install -r requirements.txt

EXPOSE 8000

CMD [ "python", "app.py" ]