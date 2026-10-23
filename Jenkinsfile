pipeline {
agent any

environment {
    DOCKER_CLI = 'C:\\Users\\venik\\AppData\\Local\\Programs\\DockerDesktop\\resources\\bin\\docker.exe'
    DOCKER_IMAGE = 'venikalaxmi/appointment-system'
    IMAGE_TAG = 'v1'
}

stages {
    stage('Verify Project Files') {
        steps {
            bat 'if not exist app.py exit /b 1'
            bat 'if not exist Dockerfile exit /b 1'
            bat 'if not exist requirements.txt exit /b 1'

            echo 'Project files verified successfully.'
        }
    }

    stage('Check Docker') {
        steps {
            bat '"%DOCKER_CLI%" version'
        }
    }

    stage('Build Docker Image') {
        steps {
            bat '"%DOCKER_CLI%" build -t %DOCKER_IMAGE%:%IMAGE_TAG% .'

            echo 'Appointment System Docker image built successfully.'
        }
    }

    stage('Verify Docker Image') {
        steps {
            bat '"%DOCKER_CLI%" image inspect %DOCKER_IMAGE%:%IMAGE_TAG%'

            echo 'Docker image verification completed successfully.'
        }
    }
}

post {
    success {
        echo 'SUCCESS: Appointment System Version 1 pipeline completed successfully.'
        echo 'The Docker image is available locally.'
        echo 'DockerHub publishing is temporarily skipped.'
    }

    failure {
        echo 'Pipeline failed. Check Console Output for the error.'
    }
}

}
