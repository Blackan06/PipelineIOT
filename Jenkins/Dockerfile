FROM jenkins/jenkins:lts

# Sử dụng quyền root
USER root

# Cài đặt Docker CLI
RUN apt-get update && apt-get install -y \
    apt-transport-https ca-certificates curl gnupg2 software-properties-common \
    && curl -fsSL https://download.docker.com/linux/debian/gpg | apt-key add - \
    && add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/debian $(lsb_release -cs) stable" \
    && apt-get update && apt-get install -y docker-ce-cli \
    && apt-get clean

# Tải và cài đặt Docker Compose
RUN curl -L "https://github.com/docker/compose/releases/download/2.30.0/docker-compose-linux-x86_64" \
  -o /usr/local/bin/docker-compose && chmod +x /usr/local/bin/docker-compose

RUN curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl" \
    && chmod +x kubectl \
    && mv kubectl /usr/local/bin/
# Thêm user Jenkins vào nhóm Docker
RUN groupadd docker && usermod -aG docker jenkins

USER jenkins
