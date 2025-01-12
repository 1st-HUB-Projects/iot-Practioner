# .devcontainer/Dockerfile
FROM mcr.microsoft.com/devcontainers/universal:2

# Example for Alpine:
#  - iputils covers ping
#  - busybox-extras might provide netstat, telnet
#  - lsof is its own package
#  - for AWS CLI, you might need to install Python or download the CLI directly

RUN apk update && apk add --no-cache \
    iputils \
    busybox-extras \
    lsof \
    curl \
    unzip \
    && rm -rf /var/cache/apk/*

# Install AWS CLI v2
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" \
    && unzip awscliv2.zip \
    && ./aws/install \
    && rm -rf awscliv2.zip aws
