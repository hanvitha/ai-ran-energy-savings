# Use a lightweight Python image as the base 
#FROM python:3.11-slim-buster

#Use minimal node.js image
FROM registry.redhat.io/ubi8/nodejs-20-minimal
WORKDIR /frontend

# Copy package files first for better caching
COPY package*.json ./

# Install dependencies in a writable temp dir
RUN npm config set cache /tmp/npm-cache --global && \
    npm install

# Copy rest of your app
COPY . .

# Expose app port
EXPOSE 3000

# Disable ESLint from running during build
ENV DISABLE_ESLINT_PLUGIN=true


# Start app
CMD ["npm", "start"]
