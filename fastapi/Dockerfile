FROM python:3.10.6
# Base docker image of python 3.x

# RUN pip install --upgrade pip
# Upgrade pip package

WORKDIR /app
# Change working dir to app

COPY /fastapi/apis.py /fastapi/schemas.py /fastapi/requirements.txt /app/

COPY /fastapi/Authentication/ /app/Authentication/

COPY /fastapi/Util/ /app/Util/

RUN pip install -r requirements.txt

#EXPOSE 8000
## Expose a port inside the container on which services run
#
#CMD ["gunicorn" ,"-w", "4", "-k", "uvicorn.workers.UvicornWorker" , "--bind", "0.0.0.0:8000", "apis:app"]
CMD ["uvicorn", "apis:app", "--host", "0.0.0.0"]
# gunicorn command to run the service with 4 worker nodes binding localhost/0.0.0.0 on port 8000 refering app inside the main.py