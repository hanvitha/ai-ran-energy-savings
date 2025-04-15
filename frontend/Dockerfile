# Use a lightweight Python image as the base 
#FROM python:3.11-slim-buster

#Use minimal node.js image
FROM registry.redhat.io/ubi8/nodejs-20-minimal
WORKDIR /frontend

# Copy application code
COPY . .

# Install dependencies
RUN npm install

RUN chmod -R g+rwX /frontend && \
    chown -R 1001:0 /frontend

# Switch to non-root user (compatible with OpenShift)
USER 1001

# Expose app port
EXPOSE 3000

# Start the app
CMD ["npm", "run", "start"]
