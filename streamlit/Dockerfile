FROM python:3.10.6

WORKDIR /app

# Steamlit
COPY /streamlit/Home.py /app/

COPY /streamlit/requirements.txt /app/

COPY /streamlit/components/ /app/components/

COPY /streamlit/Util/ /app/Util/

COPY /streamlit/.streamlit/ /app/.streamlit/

RUN pip install -r requirements.txt

EXPOSE 8501

CMD ["streamlit", "run", "Home.py"]