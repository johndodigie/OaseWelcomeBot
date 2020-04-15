FROM python:latest

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY jennybot.py .

ENV JENNYBOT_CONFIG_LOCATION="/config/config.ini"

CMD [ "python", "./jennybot.py" ]