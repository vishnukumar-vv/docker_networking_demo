pipeline {
    agent any

    environment {
        IMAGE_NAME = "8105577060/docker_networking_demo"
        // Use env.BUILD_NUMBER to ensure it is resolved correctly in the environment block
        TAG = "${env.BUILD_NUMBER}"
    }

    stages {
        stage('Clone Code') {
            steps {
                // Fixed the git syntax (removed the comma and ensured proper spacing)
                git branch: 'main', url: 'https://github.com/vishnukumar-vv/docker_networking_demo.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                // Use double quotes to allow Groovy to interpolate the variables
                sh "docker build -t ${IMAGE_NAME}:${TAG} ."
            }
        }

        stage('DockerHub Login') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-creds',
                    usernameVariable: 'USER',
                    passwordVariable: 'PASS'
                )]) {
                    // Use double quotes so Jenkins can inject the credential variables
                    sh "echo ${PASS} | docker login -u ${USER} --password-stdin"
                }
            }
        }

        stage('Push Image') {
            steps {
                sh "docker push ${IMAGE_NAME}:${TAG}"
                sh "docker tag ${IMAGE_NAME}:${TAG} ${IMAGE_NAME}:latest"
                sh "docker push ${IMAGE_NAME}:latest"
            }
        }

        stage('Deploy Containers') {
            steps {
                // Using double quotes for the multi-line string to resolve ${IMAGE_NAME}
                sh """
                docker network create app_network || true

                docker rm -f mysql_db || true
                docker rm -f web_app || true

                docker run -d --name mysql_db \
                --network app_network \
                -e MYSQL_ROOT_PASSWORD=root \
                -e MYSQL_DATABASE=testdb \
                mysql:8

                sleep 25

                docker run -d --name web_app \
                --network app_network \
                -p 8080:5000 \
                ${IMAGE_NAME}:${TAG}
                """
            }
        }
    }
}
