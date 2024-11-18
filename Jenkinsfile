pipeline {
    agent any

    environment {
        KUBECONFIG_CREDENTIALS = credentials('kubeconfig-file')
        DOCKER_REPO = 'kiet020898'
        DOCKER_HOST = 'tcp://docker-proxy:2375' // Kết nối Docker qua proxy
    }

    stages {
        stage('Checkout') {
            steps {
                script {
                    deleteDir() // Xóa toàn bộ thư mục trước khi checkout
                    checkout scm // Sử dụng scm checkout để lấy mã nguồn từ Git repository
                }
            }
        }

        stage('Check Docker') {
            steps {
                script {
                    sh 'docker info' // Kiểm tra Docker daemon có sẵn
                }
            }
        }

        stage('Build Docker Images with Docker Compose') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'docker-hub-credentials', usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]) {
                    script {
                        // Đăng nhập vào Docker Hub an toàn
                        sh '''
                            echo $DOCKER_PASSWORD | docker login -u $DOCKER_USERNAME --password-stdin
                        '''
                        
                        // Build tất cả các images từ Docker Compose
                        sh "docker-compose -f docker-compose.override.yml build"
                        sh "docker build -t ${DOCKER_REPO}/iot_stream_analysis ./spark/notebooks/"
                    }
                }
            }
        }

        stage('Push Docker Images') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'docker-hub-credentials', usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]) {
                    script {
                        // Đăng nhập vào Docker Hub để đẩy images
                        sh '''
                            echo $DOCKER_PASSWORD | docker login -u $DOCKER_USERNAME --password-stdin
                        '''
                        
                        // Push tất cả các images lên Docker Hub
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
                    // Triển khai các file YAML lên Kubernetes
                    sh 'kubectl --kubeconfig=$KUBECONFIG apply -f k8s/'
                }
            }
        }
    }

    post {
        always {
            cleanWs() // Dọn dẹp workspace của Jenkins
        }
    }
}
