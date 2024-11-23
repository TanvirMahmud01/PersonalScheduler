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

        stage('SonarQube Analysis') {
            steps {
                echo 'Running SonarQube analysis...'
                withSonarQubeEnv('SonarQube Server') {
                    def scannerHome = tool name: 'SonarScanner', type: 'hudson.plugins.sonar.SonarRunnerInstallation'
                    bat """
                    "${scannerHome}\\bin\\sonar-scanner.bat" ^
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
}
