FROM python:3.14
LABEL authors="sergi"

WORKDIR /bot-helper

COPY . .

EXPOSE 5000

ENTRYPOINT ["python", "bot.py"]