FROM python:3.6

# Create root directory in the container
RUN mkdir /youtube_fetch_api

# Working directory to /youtube
WORKDIR /youtube

# Copy the current directory contents into the container
ADD . /youtube/

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt