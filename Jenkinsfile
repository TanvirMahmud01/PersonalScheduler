pipeline {
    agent any

    environment {
        SONARQUBE_SERVER = 'SonarQube Server'
        PIPENV_VENV_IN_PROJECT = "true" // Ensures virtualenv compatibility
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
        stage('Static Code Analysis') {
            steps {
                echo 'Running SonarQube analysis...'
                withSonarQubeEnv('SonarQube Server') {
                    bat '''
                    .venv\\Scripts\\activate
                    sonar-scanner.bat
                    '''
                }
            }
        }
        stage('Unit Test') {
            steps {
                echo 'Running unit tests...'
                bat '''
                .venv\\Scripts\\activate
                pytest --cov=backend > test-results.log
                '''
                publishHTML(target: [
                    allowMissing: true,
                    alwaysLinkToLastBuild: true,
                    keepAll: true,
                    reportDir: '.',
                    reportFiles: 'test-results.log',
                    reportName: "Test Results"
                ])
            }
        }
        stage('Package') {
            steps {
                echo 'Packaging application...'
                bat '''
                tar -cvf scheduler.tar backend/
                '''
            }
        }
        stage('Deploy to Dev') {
            steps {
                echo 'Deploying to Dev Environment...'
                bat 'echo Deployment to Dev Mocked'
            }
        }
        stage('Deploy to Staging') {
            steps {
                echo 'Deploying to Staging Environment...'
                bat 'echo Deployment to Staging Mocked'
            }
        }
        stage('Deploy to Production') {
            steps {
                echo 'Deploying to Production Environment...'
                bat 'echo Deployment to Production Mocked'
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: '**/*.tar', allowEmptyArchive: true
        }
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed!'
        }
    }
}
