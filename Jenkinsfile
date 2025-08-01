pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'saiif/securebugtracker-backend'
        DOCKER_TAG = 'latest'
        DOCKER_CREDENTIALS_ID = 'dockerhub-creds'
        SONAR_SCANNER = 'SonarScanner'
        SONAR_PROJECT_KEY = 'securebugtracker'
        SONAR_HOST_URL = 'http://3.110.120.167:9000'
        SONAR_AUTH_TOKEN = credentials('sonar-token')
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

        stage('Trivy Scan') {
            steps {
                echo 'Running Trivy vulnerability scan...'
                sh '''
                    trivy image --format json --output trivy-report.json $DOCKER_IMAGE:$DOCKER_TAG || true
                '''
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

        stage('Archive Reports') {
            steps {
                echo 'Archiving Trivy scan report...'
                archiveArtifacts artifacts: 'trivy-report.json', allowEmptyArchive: true
            }
        }
    }

    post {
        success {
            emailext (
                subject: "Jenkins Build Success: ${env.JOB_NAME} [#${env.BUILD_NUMBER}]",
                body: """
                    <p>Hi Team,</p>
                    <p>The Jenkins job <strong>${env.JOB_NAME}</strong> build <strong>#${env.BUILD_NUMBER}</strong> completed <span style='color:green;'>successfully</span>.</p>
                    <p>Check the job console <a href="${env.BUILD_URL}">here</a>.</p>
                    <br>
                    <p>Regards,<br>Jenkins CI</p>
                """,
                mimeType: 'text/html',
                to: "saiifhashmii000@gmail.com"
            )
        }
        failure {
            emailext (
                subject: "Jenkins Build Failed: ${env.JOB_NAME} [#${env.BUILD_NUMBER}]",
                body: """
                    <p>Hi Team,</p>
                    <p>The Jenkins job <strong>${env.JOB_NAME}</strong> build <strong>#${env.BUILD_NUMBER}</strong> has <span style='color:red;'>FAILED</span>.</p>
                    <p>Check the job console <a href="${env.BUILD_URL}">here</a> for details.</p>
                    <br>
                    <p>Regards,<br>Jenkins CI</p>
                """,
                mimeType: 'text/html',
                to: "saiifhashmii000@gmail.com"
            )
        }
        always {
            echo 'Jenkins pipeline execution completed.'
        }
    }
}

