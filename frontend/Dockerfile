#Use minimal node.js image
FROM registry.redhat.io/ubi8/nodejs-20-minimal
# Set the working directory in the container 
USER root
WORKDIR /frontend

COPY package.json .
RUN npm install

RUN mkdir node_modules/.cache && chmod -R 777 node_modules/.cache

# Copy the application code
COPY . .

# Expose the port your application listens on (if necessary) 
EXPOSE 3000 
# Command to run the application when the container starts 
CMD ["npm", "run", "start"]
