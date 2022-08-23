FROM python:3-alpine

RUN pip install --upgrade pip

RUN adduser -D pyapp
USER pyapp:pyapp

WORKDIR /app
COPY --chown=pyapp:pyapp requirements.txt requirements.txt
RUN pip3 install --user -r requirements.txt
COPY --chown=pyapp:pyapp app.py app.py

EXPOSE 8080

CMD [ "python3", "app.py"]