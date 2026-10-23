pipeline {
agent any

```
environment {
    DOCKER_IMAGE = 'venikalaxmi/appointment-system'
    IMAGE_TAG = 'v1'
    DOCKER_CLI = 'C:\\Users\\venik\\AppData\\Local\\Programs\\DockerDesktop\\resources\\bin\\docker.exe'
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
                powershell '''
                    $env:DOCKERHUB_TOKEN | & $env:DOCKER_CLI login -u $env:DOCKERHUB_USER --password-stdin
                    if ($LASTEXITCODE -ne 0) { exit 1 }

                    & $env:DOCKER_CLI push "$env:DOCKER_IMAGE`:$env:IMAGE_TAG"
                    if ($LASTEXITCODE -ne 0) { exit 1 }

                    & $env:DOCKER_CLI logout
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
        echo 'Pipeline failed. Check Console Output for the error.'
    }
}
}



