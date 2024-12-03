pipeline {
    agent any

    environment {
        SONAR_HOST_URL = 'http://localhost:9000'
        SONAR_LOGIN = 'sqa_954c423859ee3d4618b2447072b15f3ed74953da'
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out code...'
                checkout scm
            }
        }

        stage('Setup Environment') {
            steps {
                echo 'Setting up Python environment...'
                bat '''
                python -m venv .venv
                .venv\\Scripts\\activate
                pip install --upgrade pip
                pip install -r backend/requirements.txt
                '''
            }
        }

        stage('Build') {
            steps {
                echo 'Validating application setup...'
                bat '''
                .venv\\Scripts\\activate
                echo "Application ready to build/run."
                '''
            }
        }

        stage('SonarQube Analysis') {
            steps {
                echo 'Running SonarQube analysis...'
                withSonarQubeEnv('SonarQube Server') {
                    script {
                        def scannerHome = tool 'SonarScanner'
                        bat """
                        ${scannerHome}\\bin\\sonar-scanner.bat ^
                        -Dsonar.projectKey=personal-scheduler ^
                        -Dsonar.sources=backend ^
                        -Dsonar.host.url=${SONAR_HOST_URL} ^
                        -Dsonar.login=${SONAR_LOGIN} ^
                        -Dsonar.sourceEncoding=UTF-8
                        """
                    }
                }
            }
        }

        stage('Test') {
            steps {
                echo 'Running tests and generating code coverage report...'
                bat '''
                .venv\\Scripts\\activate
                pytest --cov=backend tests/
                '''
            }
        }
    }
}
