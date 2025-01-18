# Use a lightweight Python image as the base 
#FROM python:3.11-slim-buster

#Use minimal node.js image
FROM registry.redhat.io/ubi8/nodejs-20-minimal
# Set the working directory in the container 
USER root
WORKDIR /frontend

# Copy the application code 
COPY . . 

#run front end
RUN npm install

# Expose the port your application listens on (if necessary) 
EXPOSE 3000 
# Command to run the application when the container starts 
CMD ["npm", "run", "start"]