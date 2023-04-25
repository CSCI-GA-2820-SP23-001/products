# This image has selenium and chrome driver already installed
FROM rofrano/pipeline-selenium:lastest

# Set up the Python development environment
WORKDIR /app
COPY requirements.txt .
RUN sudo python -m pip install --upgrade pip wheel && \
    sudo pip install -r requirements.txt

# Install user mode tools
COPY .devcontainer/scripts/install-tools.sh /tmp/
RUN cd /tmp; bash ./install-tools.sh
