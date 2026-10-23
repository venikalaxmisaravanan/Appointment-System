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
        }
    }

    stage('Diagnose DockerHub Login') {
        steps {
            withCredentials([
                usernamePassword(
                    credentialsId: 'dockerhub-credentials',
                    usernameVariable: 'DOCKERHUB_USER',
                    passwordVariable: 'DOCKERHUB_TOKEN'
                )
            ]) {
                powershell '''
                    if ([string]::IsNullOrWhiteSpace($env:DOCKERHUB_USER)) {
                        Write-Output "DIAGNOSTIC: DockerHub username is empty."
                        exit 1
                    }

                    if ([string]::IsNullOrWhiteSpace($env:DOCKERHUB_TOKEN)) {
                        Write-Output "DIAGNOSTIC: DockerHub token is empty."
                        exit 1
                    }

                    Write-Output "DIAGNOSTIC: DockerHub username is $env:DOCKERHUB_USER"
                    Write-Output "DIAGNOSTIC: DockerHub token is present (length: $($env:DOCKERHUB_TOKEN.Length))."

                    $env:DOCKERHUB_TOKEN | & $env:DOCKER_CLI login -u $env:DOCKERHUB_USER --password-stdin

                    if ($LASTEXITCODE -ne 0) {
                        Write-Output "DIAGNOSTIC: DockerHub login failed."
                        exit 1
                    }

                    Write-Output "DIAGNOSTIC: DockerHub login succeeded."

                    & $env:DOCKER_CLI logout
                '''
            }
        }
    }
}

post {
    success {
        echo 'DockerHub authentication diagnostic completed successfully.'
    }

    failure {
        echo 'Diagnostic failed. Check Console Output for details.'
    }
}

}
