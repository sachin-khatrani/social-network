# Use the official Python image as a base
FROM python:3.10

# The enviroment variable ensures that the python output is set straight
# to the terminal with out buffering it first
ENV PYTHONUNBUFFERED 1

# create root directory for our project in the container
RUN mkdir /social-network

# Set the working directory to /social-network
WORKDIR /social-network

# Copy the current directory contents into the container at /music_service
ADD . /social-network/

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt