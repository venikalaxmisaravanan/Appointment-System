pipeline {
    agent any

    environment {
        DOCKER_EXE = 'C:\\Users\\venik\\AppData\\Local\\Programs\\DockerDesktop\\resources\\bin\\docker.exe'
        IMAGE_NAME = 'venikalaxmi/appointment-system:v3'
    }

    stages {
        stage('Verify Project Files') {
            steps {
                echo 'Checking Appointment System Version 3 project files...'

                bat 'dir'

                bat 'if not exist app.py exit /b 1'
                bat 'if not exist requirements.txt exit /b 1'
                bat 'if not exist Dockerfile exit /b 1'
                bat 'if not exist templates\\index.html exit /b 1'
                bat 'if not exist static\\style.css exit /b 1'
            }
        }

        stage('Check Docker') {
            steps {
                echo 'Checking Docker availability...'

                bat '"%DOCKER_EXE%" --version'
                bat '"%DOCKER_EXE%" info'
            }
        }

        stage('Build Docker Image') {
            steps {
                echo 'Building Appointment System Version 3 Docker image...'

                bat '"%DOCKER_EXE%" build -t %IMAGE_NAME% .'
            }
        }

        stage('Verify Docker Image') {
            steps {
                echo 'Verifying the Version 3 Docker image...'

                bat '"%DOCKER_EXE%" image inspect %IMAGE_NAME%'

                bat '"%DOCKER_EXE%" images venikalaxmi/appointment-system'
            }
        }

        stage('Publish to Docker Hub') {
            steps {
                echo 'Docker Hub publishing is temporarily skipped.'
                echo 'The Version 3 image will be published separately after Jenkins verification.'
            }
        }
    }

    post {
        success {
            echo 'SUCCESS: Appointment System Version 3 pipeline completed successfully.'
            echo 'The Version 3 Docker image is available locally.'
            echo 'Docker Hub publishing is temporarily skipped.'
        }

        failure {
            echo 'FAILED: Appointment System Version 3 pipeline encountered an error.'
            echo 'Check the Jenkins Console Output for details.'
        }

        always {
            echo 'Version 3 Jenkins pipeline execution finished.'
        }
    }
}