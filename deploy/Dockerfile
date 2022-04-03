FROM python:3.10.1

RUN apt-get update && \
    apt-get install -y tesseract-ocr libtesseract-dev  &&  \
    pip3 install pillow pytesseract APScheduler werkzeug Flask requests click gunicorn lxml \
    redis scrapy beautifulsoup4



RUN wget https://chromedriver.storage.googleapis.com/99.0.4844.51/chromedriver_linux64.zip && \
    unzip chromedriver_linux64.zip && mv chromedriver /usr/bin/chromedriver && rm chromedriver_linux64.zip

RUN pip install  selenium

RUN apt-get install -y libnss3 fonts-liberation libasound2 libatk-bridge2.0-0 libatk1.0-0 libatspi2.0-0 libcups2 \
    libdbus-1-3 libdrm2 libgbm1 libgtk-3-0 libxcomposite1 libxdamage1 libxfixes3 libxkbcommon0 libxrandr2 xdg-utils

RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    dpkg -i google-chrome-stable_current_amd64.deb && \
    apt-get -f install && rm google-chrome-stable_current_amd64.deb

RUN pip install  pymysql

WORKDIR /app

EXPOSE 8010:8010

CMD ["top", "-b"]

