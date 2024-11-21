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
