FROM python:3.10

#
WORKDIR /usr/src/app
RUN apt-get update
RUN apt-get -y install libgl1-mesa-glx
#
COPY ./requirements.txt .

#
RUN pip install --no-cache-dir --upgrade -r requirements.txt

#
COPY . .

#
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]