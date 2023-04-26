FROM python:3.10.6

WORKDIR /app

# Steamlit
COPY Home.py /app/

COPY requirements.txt /app/

COPY /components/ /app/components/

COPY /Util/ /app/Util/

COPY /.streamlit/ /app/.streamlit/

RUN pip install -r requirements.txt

EXPOSE 8501

CMD ["streamlit", "run", "Home.py"]