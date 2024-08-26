FROM python:3.12-slim

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt
RUN python populate_db.py

CMD [ "./run-task.sh" ]
