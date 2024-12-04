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
                cd backend
                python -m venv .venv
                .venv\\Scripts\\activate
                pip install --upgrade pip
                pip install -r backend/requirements.txt
                echo 'Finished setting up Python environment...'
                '''
            }
        }

        stage('Build') {
            steps {
                echo 'Validating application setup...'
                bat '''
                cd backend
                .venv\\Scripts\\activate
                echo "Application ready to build/run."
                '''
            }
        }

        stage('Test') {
            steps {
                echo 'Running tests and generating code coverage report...'
                bat '''
                cd backend
                .venv\\Scripts\\activate
                pytest --cov=backend --cov-report=xml --cov-report=term --junitxml=backend/results.xml
                '''
            }
        }

        stage('Prepare Coverage Report') {
            steps {
                echo 'Preparing coverage report...'
                bat '''
                mkdir backend\\reports
                move coverage.xml backend\\reports\\
                '''
            }
        }

        stage('Publish Test Results') {
            steps {
                echo 'Publishing JUnit test results...'
                junit '**/backend/results.xml'
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
                        -Dsonar.python.coverage.reportPaths=backend/reports/coverage.xml ^
                        -Dsonar.sourceEncoding=UTF-8
                        """
                    }
                }
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
                cd backend
                .venv\\Scripts\\activate
                echo "Starting uvicorn server..."
                start /B uvicorn main:app --host 127.0.0.1 --port 8000 --reload > uvicorn.log 2>&1
                timeout /t 10 /nobreak
                type uvicorn.log
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

    post {
        always {
            echo 'Pipeline execution complete. Publishing final results...'
            junit '**/backend/results.xml'
        }
    }
}
