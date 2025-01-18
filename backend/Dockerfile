# Dockerfile
FROM registry.redhat.io/ubi8/python-312:latest

# Set working directory
USER root
WORKDIR /backend

COPY . .

# Install dependencies

RUN pip install --no-cache-dir -r requirements.txt \
    && chmod 775 /backend

#ENV MODEL_URL="instructlab-deployment.ilab.svc.cluster.local/v1"

# Expose port
EXPOSE 8000

#  Run the app with Gunicorn (WSGI server)
#CMD ["gunicorn"  , "-b", "0.0.0.0:8080", "app:app"]
#  Run the app with uvicorn (WSGI server)
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]