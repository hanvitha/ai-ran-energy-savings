# Use a lightweight Python image as the base 
#FROM python:3.11-slim-buster

#Use minimal node.js image
FROM registry.redhat.io/ubi8/nodejs-20-minimal
# Create a non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Set permissions for the directory
RUN mkdir -p /frontend/node_modules/.cache && \
    chown -R appuser:appuser /frontend/node_modules

# Switch to the non-root user
USER appuser

# Set the working directory
WORKDIR /frontend
# Copy the application code 
COPY . . 

#run front end
RUN npm install

# Expose the port your application listens on (if necessary) 
EXPOSE 3000 
# Command to run the application when the container starts 
CMD ["npm", "run", "start"]