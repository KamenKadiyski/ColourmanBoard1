# Use an official Python runtime as a parent image
FROM python:3.14-alpine3.24

# Set the working directory in the container
WORKDIR /app

# Install any needed packages specified in requirements.txt
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app

# Expose port 8000 to the outside world
EXPOSE 8000

# Run Django migrations and collect static files
RUN DATABASE_URL=postgres://user:pass@localhost:5432/db python manage.py collectstatic --noinput


# Define environment variable
ENV DJANGO_SETTINGS_MODULE=ColourmanBoard.settings

# Run the Django development server
# Заменете стария CMD ред с този:
CMD ["gunicorn", "ColourmanBoard.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]

