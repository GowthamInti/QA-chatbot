# Use the official Python 3.9 image as the base
FROM python:3.9

# Create a non-root user and switch to it
RUN useradd -m -u 1000 user
USER user
ENV PATH="/home/user/.local/bin:$PATH"

# Set the working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY --chown=user ./requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy the rest of the application code
COPY --chown=user . /app

# Set environment variables for Hugging Face authentication
# (You can also pass these at runtime using `docker run -e`)
ARG auth_token
ENV auth_token=$auth_token

# Expose the port the app runs on
EXPOSE 7860

# Command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]