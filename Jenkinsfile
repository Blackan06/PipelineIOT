pipeline {
    agent any

    environment {
        // Docker Hub credentials
        DOCKER_HUB_CREDENTIALS = credentials('docker-hub-credentials') // Thay 'docker-hub-credentials' bằng ID Jenkins credentials của bạn
        KUBECONFIG_CREDENTIALS = credentials('kubeconfig-file') // Thay 'kubeconfig-file' bằng ID của kubeconfig
        DOCKER_REPO = 'kiet020898' // Repository trên Docker Hub của bạn
    }

    stages {
        stage('Checkout') {
            steps {
                // Lấy mã nguồn từ Git repository
                git branch: 'main', url: 'https://github.com/Blackan06/PipelineIOT.git' // Thay URL bằng repository của bạn
            }
        }

        stage('Build Docker Images with Docker Compose') {
            steps {
                script {
                    docker.withRegistry('', DOCKER_HUB_CREDENTIALS) {
                        // Build tất cả các images trong Docker Compose
                        sh "docker-compose -f docker-compose.override.yml build"
                        sh "docker build -t ${DOCKER_REPO}/iot_stream_analysis ./spark/notebooks/"

                    }
                }
            }
        }

        stage('Push Docker Images') {
            steps {
                script {
                    docker.withRegistry('https://registry.hub.docker.com', DOCKER_HUB_CREDENTIALS) {
                        // Push tất cả các images lên Docker Hub
                        // Thay thế các tên service theo các images đã định nghĩa trong docker-compose.override.yml
                        sh "docker push ${DOCKER_REPO}/webserver"
                        sh "docker push ${DOCKER_REPO}/scheduler"
                        sh "docker push ${DOCKER_REPO}/spark-master"
                        sh "docker push ${DOCKER_REPO}/spark-worker"
                        sh "docker push ${DOCKER_REPO}/iot_stream_analysis"
                    }
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                withCredentials([file(credentialsId: 'kubeconfig-file', variable: 'KUBECONFIG')]) {
                    // Triển khai tất cả các file YAML trong thư mục k8s lên Kubernetes
                    sh 'kubectl --kubeconfig=$KUBECONFIG apply -f k8s/'
                }
            }
        }
    }

    post {
        always {
            cleanWs() // Clean workspace của Jenkins để tiết kiệm dung lượng
        }
    }
}
