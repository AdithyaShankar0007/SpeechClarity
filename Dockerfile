FROM streamlit/streamlit:latest
RUN apt-get update && apt-get install -y portaudio19-dev
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
docker build -t streamlit-app .
docker run -p 8501:8501 streamlit-app
