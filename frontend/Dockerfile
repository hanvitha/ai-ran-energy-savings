# Use a lightweight Python image as the base 
#FROM python:3.11-slim-buster

#Use minimal node.js image
FROM registry.redhat.io/ubi8/nodejs-20-minimal
WORKDIR /frontend

# Copy package files and install dependencies
COPY package*.json ./
RUN npm install

# Copy app code
COPY . .

# Disable eslint so it doesn't try to write to .cache
ENV DISABLE_ESLINT_PLUGIN=true

EXPOSE 3000

CMD ["npm", "start"]
