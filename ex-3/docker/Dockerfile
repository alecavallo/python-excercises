# PostgreSQL Dockerfile
FROM postgres:16-alpine

# Set environment variables
ENV POSTGRES_DB=meeting_scheduler
ENV POSTGRES_USER=meeting_user
ENV POSTGRES_PASSWORD=meeting_password

# Create directory for custom initialization scripts
RUN mkdir -p /docker-entrypoint-initdb.d

# Copy initialization script if needed
# COPY init.sql /docker-entrypoint-initdb.d/

# Expose PostgreSQL port
EXPOSE 5432

# Use the default postgres entrypoint
CMD ["postgres"]
