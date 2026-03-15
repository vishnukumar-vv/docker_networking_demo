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
        sh '''
        echo "===== Creating Docker Network ====="
        docker network create app_network || true

        echo "===== Listing Docker Networks ====="
        docker network ls

        echo "===== Removing old containers ====="
        docker rm -f mysql_db || true
        docker rm -f web_app || true

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
        $IMAGE:$TAG

        echo "===== Running Containers ====="
        docker ps
        '''
    }
}
    
    post {
        always {
            // Good practice to clean up local images to save disk space
            sh "docker rmi ${IMAGE}:${TAG} || true"
        }
    }
}
