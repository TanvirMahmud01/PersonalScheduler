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
                pytest --cov=backend --cov-report=term --junitxml=results.xml
                dir
                '''
            }
        }

        stage('Publish Test Results') {
            steps {
                echo 'Publishing JUnit test results...'
                junit '**/backend/results.xml'
               
            }
        }

        stage('Deliver') {
            steps {
                echo 'Delivering build artifact...'
                bat '''
                .venv\\Scripts\\activate
                echo "Mocking artifact delivery..."
                '''
            }
        }

        stage('Deploy to Dev Env') {
            steps {
                echo 'Deploying to Dev environment...'
                bat '''
                .venv\\Scripts\\activate
                uvicorn main:app --host 127.0.0.1 --port 8000 --reload &
                timeout /T 5 >nul
                taskkill /IM "python.exe" /F
                echo "Mocked Dev environment deployment completed."
                '''
            }
        }

        stage('Deploy to QAT Env') {
            steps {
                echo 'Deploying to QAT environment...'
                bat '''
                echo "Mocking deployment to QAT environment."
                '''
            }
        }

        stage('Deploy to Staging Env') {
            steps {
                echo 'Deploying to Staging environment...'
                bat '''
                echo "Mocking deployment to Staging environment."
                '''
            }
        }

        stage('Deploy to Production Env') {
            steps {
                echo 'Deploying to Production environment...'
                bat '''
                echo "Mocking deployment to Production environment."
                '''
            }
        }
    }
}
