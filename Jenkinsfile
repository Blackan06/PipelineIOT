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
        stage('Setup') {
            steps {
                script {
                    // Kiểm tra và cài đặt Astro CLI
                    sh '''
                        curl -fsSL https://install.astronomer.io | bash
                        astro version
                    '''
                }
            }
        }
        stage('Start Astro Development Environment') {
            steps {
                script {
                    sh '''
                        echo "Starting Astro Development Environment..."
                        astro dev start --wait 4m
                    '''
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
                        sh "docker build -t ${DOCKER_REPO}/iot_stream_analysis ./spark/notebooks/"
                        sh "docker build -t ${DOCKER_REPO}/kafka_producer ./kafka/producer/"
                        sh "docker build -t ${DOCKER_REPO}/kafka_consumer ./kafka/consumer/"
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
                       
                        sh "docker push ${DOCKER_REPO}/iot_stream_analysis"
                        sh "docker push ${DOCKER_REPO}/kafka_producer"
                        sh "docker push ${DOCKER_REPO}/kafka_consumer"
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
