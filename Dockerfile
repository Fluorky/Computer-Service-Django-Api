# Use the official Python 3.9 base image
FROM python:3.9

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file to the /app directory inside the container
COPY requirements.txt /app/

# Install the required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the contents of the Django project directory to the /app directory inside the container
COPY . /app/

# Define environment variables for Django settings (optional)
# ENV DJANGO_SETTINGS_MODULE=myproject.settings.production

# Run migrations and collect static files (if needed)
# RUN python manage.py migrate
# RUN python manage.py collectstatic --noinput

# Open port 8000 on the container
EXPOSE 8000
