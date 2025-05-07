FROM python:3.11-slim

# I have Setup the working directory
WORKDIR /app

# i have Copied all project files into the container
COPY . /app

# Upgraded pip and installed the dependencies
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

#i have  Exposed the port to my FastAPI app will run on
EXPOSE 8000

# Started the FastAPI app using Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]