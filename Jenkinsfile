pipeline {
    agent { label 'dockergit' }

    environment {
        IMAGE = "8105577060/docker_networking_demo"
        TAG   = "${env.BUILD_NUMBER}" 
    }

    stages {
        stage('Build Docker Image') {
            steps {
                sh "docker build -t ${IMAGE}:${TAG} ."
            }
        }

        stage('Docker Login') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-creds',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS')]) {
                    
                    // Securely login using stdin
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
                // Use triple-DOUBLE quotes (""" """) to allow string interpolation
                sh """
                echo "===== Creating Docker Network ====="
                docker network create app_network || true

                echo "===== Listing Docker Networks ====="
                docker network ls

                echo "===== Removing old containers ====="
                docker rm -f mysql_db web_app || true

                echo "===== Starting MySQL Container ====="
                docker run -d --name mysql_db \
                    --network app_network \
                    -e MYSQL_ROOT_PASSWORD=root \
                    -e MYSQL_DATABASE=testdb \
                    mysql:8

                echo "Waiting for DB to start..."
                sleep 25

                echo "===== Starting Web Container ====="
                docker run -d --name web_app \
                    --network app_network \
                    -p 8090:5000 \
                    ${IMAGE}:${TAG}

                echo "===== Running Containers ====="
                docker ps
                """
            }
        }
    }
    
    post {
        always {
            // Cleanup local image to save agent disk space
            sh "docker rmi ${IMAGE}:${TAG} || true"
        }
    }
}
