# Use a lightweight Python image as the base 
#FROM python:3.11-slim-buster

#Use minimal node.js image
FROM registry.redhat.io/ubi8/nodejs-20-minimal

# Create and set working directory
WORKDIR /frontend

# Copy package files first
COPY package*.json ./

# Create node_modules as root and fix permissions
RUN mkdir -p /frontend/node_modules \
    && chown -R node:node /frontend

# Switch to the non-root node user
USER node

# Install dependencies
RUN npm install

# Copy the rest of the app with proper ownership
COPY --chown=node:node . .

# Environment variable to disable ESLint cache writes
ENV DISABLE_ESLINT_PLUGIN=true

EXPOSE 3000
CMD ["npm", "start"]
