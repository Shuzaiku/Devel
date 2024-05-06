FROM docker.io/python:3
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
CMD [ "python", "discord_bot.py" ]