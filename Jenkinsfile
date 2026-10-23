
pipeline {
    agent any

    options {
        timestamps()
    }

    stages {
        stage('Verify Version 2 Branch') {
            steps {
                echo 'Verifying Appointment System Version 2.'

                bat 'git branch --show-current'

                bat 'git log -1 --oneline'
            }
        }

        stage('Verify Project Files') {
            steps {
                bat 'if not exist app.py exit /b 1'
                bat 'if not exist templates\\index.html exit /b 1'
                bat 'if not exist static\\style.css exit /b 1'
                bat 'if not exist requirements.txt exit /b 1'
                bat 'if not exist Dockerfile exit /b 1'

                echo 'All required application files are present.'
            }
        }

        stage('Check Python Syntax') {
            steps {
                bat 'python --version'
                bat 'python -m py_compile app.py'

                echo 'Python syntax verification completed successfully.'
            }
        }
    }

    post {
        success {
            echo 'SUCCESS: Appointment System Version 2 verification completed.'
        }

        failure {
            echo 'FAILURE: Check the Jenkins console output for details.'
        }
    }
}
