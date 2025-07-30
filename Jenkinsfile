pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'saiif/securebugtracker-backend'
        DOCKER_TAG = 'latest'
        DOCKER_CREDENTIALS_ID = 'dockerhub-creds'
    }

    stages {
        stage('Checkout Code') {
            steps {
                echo ' Cloning GitHub repository...'
                
            }
        }

        stage('Build Docker Image') {
            steps {
                echo ' Building Docker image...'
                sh 'docker build -t $DOCKER_IMAGE:$DOCKER_TAG ./backend'
            }
        }

        stage('Push to Docker Hub') {
            steps {
                echo ' Pushing image to Docker Hub...'
                withCredentials([usernamePassword(credentialsId: "${DOCKER_CREDENTIALS_ID}", usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh '''
                        echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                        docker push $DOCKER_IMAGE:$DOCKER_TAG
                        docker logout
                    '''
                }
            }
        }
    }

    post {
        always {
            echo ' Jenkins pipeline execution completed.'
        }
    }
}

