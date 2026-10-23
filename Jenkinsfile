
pipeline {
    agent any

    options {
        timestamps()
    }

    environment {
        DOCKER_CLI = 'C:\\Users\\venik\\AppData\\Local\\Programs\\DockerDesktop\\resources\\bin\\docker.exe'
        DOCKER_IMAGE = 'venikalaxmi/appointment-system'
        IMAGE_TAG = 'v2'
    }

    stages {
        stage('Verify Project Files') {
            steps {
                echo 'Verifying Appointment System Version 2 project files.'

                bat 'if not exist app.py exit /b 1'
                bat 'if not exist templates\\index.html exit /b 1'
                bat 'if not exist static\\style.css exit /b 1'
                bat 'if not exist requirements.txt exit /b 1'
                bat 'if not exist Dockerfile exit /b 1'

                echo 'All required application files are present.'
            }
        }

        stage('Check Docker') {
            steps {
                bat '"%DOCKER_CLI%" --version'
                bat '"%DOCKER_CLI%" info'

                echo 'Docker is available.'
            }
        }

        stage('Build Docker Image') {
            steps {
                bat '"%DOCKER_CLI%" build -t %DOCKER_IMAGE%:%IMAGE_TAG% .'

                echo 'Version 2 Docker image build completed.'
            }
        }

        stage('Verify Docker Image') {
            steps {
                bat '"%DOCKER_CLI%" image inspect %DOCKER_IMAGE%:%IMAGE_TAG%'

                echo 'Version 2 Docker image is available locally.'
            }
        }

        stage('Publish to Docker Hub') {
            steps {
                echo 'Docker Hub publishing is temporarily skipped.'
                echo 'The image can be published manually through Docker Desktop.'
            }
        }
    }

    post {
        success {
            echo 'SUCCESS: Appointment System Version 2 pipeline completed successfully.'
            echo 'The Version 2 Docker image is available locally.'
            echo 'Docker Hub publishing is temporarily skipped.'
        }

        failure {
            echo 'FAILURE: Check the Jenkins Console Output for details.'
        }
    }
}

