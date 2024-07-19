FROM python
WORKDIR /usr/src/app
COPY . .
RUN pip install -r requirements.txt