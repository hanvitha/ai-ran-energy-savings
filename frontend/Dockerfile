# Use a lightweight Python image as the base 
#FROM python:3.11-slim-buster

#Use minimal node.js image
FROM registry.redhat.io/ubi8/nodejs-20-minimal
# Create app directory and set ownership
WORKDIR /frontend
COPY package*.json ./

# Ensure correct permissions
RUN mkdir -p /frontend/node_modules && chown -R node:node /frontend

# Switch to non-root user
USER node

# Install dependencies
RUN npm install

# Copy rest of the app
COPY --chown=node:node . .

ENV DISABLE_ESLINT_PLUGIN=true

EXPOSE 3000
CMD ["npm", "start"]
