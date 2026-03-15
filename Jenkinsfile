pipeline {
    agent { label 'dockergit' }

    environment {
        // Use double quotes for string interpolation of BUILD_NUMBER
        IMAGE = "8105577060/docker_networking_demo"
        TAG   = "${env.BUILD_NUMBER}" 
    }

    stages {
        stage('Build Docker Image') {
            steps {
                // Use double quotes in sh to allow Groovy to pass the environment variables
                sh "docker build -t ${IMAGE}:${TAG} ."
            }
        }

        stage('Docker Login') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-creds',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS')]) {
                    
                    // Passing credentials via stdin is the secure way to go
                    sh "echo ${DOCKER_PASS} | docker login -u ${DOCKER_USER} --password-stdin"
                }
            }
        }

        stage('Push Image') {
            steps {
                sh "docker push ${IMAGE}:${TAG}"
            }
        }

        stage('Deploy Containers') {
            steps {
                sh """
                # Create network if it doesn't exist
                docker network create app_network || true

                # Remove existing containers to avoid name conflicts
                docker rm -f mysql_db || true
                docker rm -f web_app || true

                # Run MySQL
                docker run -d --name mysql_db \
                    --network app_network \
                    -e MYSQL_ROOT_PASSWORD=root \
                    -e MYSQL_DATABASE=testdb \
                    mysql:8

                # Wait for DB to initialize
                sleep 20

                # Run App
                docker run -d --name web_app \
                    --network app_network \
                    -p 8080:5000 \
                    ${IMAGE}:${TAG}
                """
            }
        }
    }
    
    post {
        always {
            // Good practice to clean up local images to save disk space
            sh "docker rmi ${IMAGE}:${TAG} || true"
        }
    }
}
