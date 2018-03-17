FROM python:3
WORKDIR /yeebot
ADD . /yeebot
RUN touch /yeebot/secrets.py
RUN pip install -r requirements.txt
CMD ["python", "bot.py"] 
