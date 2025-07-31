pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'saiif/securebugtracker-backend'
        DOCKER_TAG = 'latest'
        DOCKER_CREDENTIALS_ID = 'dockerhub-creds'
        SONAR_SCANNER = 'SonarScanner'             // name from Global Tool Config
        SONAR_PROJECT_KEY = 'securebugtracker'     // must match project key in SonarQube
        SONAR_HOST_URL = 'http://3.110.120.167/:9000' // update with your SonarQube URL
        SONAR_AUTH_TOKEN = credentials('sonar-token') // Jenkins credentials ID for SonarQube token
    }

    stages {
        stage('Checkout Code') {
            steps {
                echo 'Cloning GitHub repository...'
                checkout scm
            }
        }

        stage('SonarQube Analysis') {
            steps {
                echo 'Running SonarQube analysis...'
                withSonarQubeEnv('SonarQube') {
                    withEnv(["SONAR_TOKEN=$SONAR_AUTH_TOKEN"]) {
                        sh """
                            ${tool SONAR_SCANNER}/bin/sonar-scanner \
                            -Dsonar.projectKey=$SONAR_PROJECT_KEY \
                            -Dsonar.sources=./backend \
                            -Dsonar.host.url=$SONAR_HOST_URL \
                            -Dsonar.login=$SONAR_AUTH_TOKEN
                        """
                    }
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                echo 'Building Docker image...'
                sh 'docker build -t $DOCKER_IMAGE:$DOCKER_TAG ./backend'
            }
        }

        stage('Push to Docker Hub') {
            steps {
                echo 'Pushing image to Docker Hub...'
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
            echo 'Jenkins pipeline execution completed.'
        }
    }
}

