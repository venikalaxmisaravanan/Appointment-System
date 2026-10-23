
pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'venikalaxmi/appointment-system'
        IMAGE_TAG = 'v1'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Verify Project Files') {
            steps {
                bat 'dir'
                bat 'if not exist app.py exit /b 1'
                bat 'if not exist Dockerfile exit /b 1'
                bat 'if not exist requirements.txt exit /b 1'
                echo 'Project files verified successfully.'
            }
        }

        stage('Check Docker') {
            steps {
                bat 'docker version'
            }
        }

        stage('Build Docker Image') {
            steps {
                bat 'docker build -t %DOCKER_IMAGE%:%IMAGE_TAG% .'
            }
        }

        stage('Login to DockerHub and Push') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub-credentials',
                        usernameVariable: 'DOCKERHUB_USER',
                        passwordVariable: 'DOCKERHUB_TOKEN'
                    )
                ]) {
                    bat '''
                        @echo off
                        echo %DOCKERHUB_TOKEN% | docker login -u %DOCKERHUB_USER% --password-stdin
                        if errorlevel 1 exit /b 1
                        docker push %DOCKER_IMAGE%:%IMAGE_TAG%
                        if errorlevel 1 exit /b 1
                        docker logout
                    '''
                }
            }
        }
    }

    post {
        success {
            echo 'Appointment System v1 image built and pushed successfully.'
        }
        failure {
            echo 'Pipeline failed. Check the Console Output for the failing stage.'
        }
    }
}
