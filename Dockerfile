FROM python:3
WORKDIR /yeebot
ADD . /yeebot
ENV TZ=America/Los_Angeles
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN touch /yeebot/secrets.py
RUN pip install -r requirements.txt
CMD ["python", "bot.py"] 
