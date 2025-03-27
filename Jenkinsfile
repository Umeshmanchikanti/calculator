pipeline {
    agent any

    environment {
        EC2_USER = 'ec2-user'
        EC2_HOST = '54.234.110.2'
        DOCKERHUB_USERNAME = 'umesh1027'
        DOCKER_IMAGE = "$DOCKERHUB_USERNAME/calculator-app:latest"
        DOCKER_REPO = 'umesh1027/calculator-app'
    }

    stages {
        stage('Checkout Repository') {
            steps {
                checkout scm
            }
        }

        stage('Set up Python and Install Dependencies') {
            steps {
                sh '''
                    python3 -m venv venv
                    source venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                    source venv/bin/activate
                    pytest
                '''
            }
        }  

        stage('Build and Push Docker Image') {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: 'DOCKERHUB_CREDENTIALS', usernameVariable: 'DOCKERHUB_USERNAME', passwordVariable: 'DOCKERHUB_PASSWORD')]) {
                        sh '''
                            echo "${DOCKERHUB_PASSWORD}" | docker login -u "${DOCKERHUB_USERNAME}" --password-stdin
                            docker build -t ${DOCKER_REPO}:latest .
                            docker push ${DOCKER_REPO}:latest
                        '''
                    }
                }
            }
        }

        stage('Debugging') {
            steps {
                sh '''
                    echo "EC2 User: $EC2_USER"
                    echo "EC2 Host: $EC2_HOST"
                '''
            }
        }

        stage('Deploy to AWS EC2') {
            steps {
                script {
                    withCredentials([sshUserPrivateKey(credentialsId: 'ec2-ssh-private-key', keyFileVariable: 'SSH_KEY')]) {
                        sh '''
                            chmod 600 $SSH_KEY
                            ssh -t -o StrictHostKeyChecking=no -i $SSH_KEY $EC2_USER@$EC2_HOST <<EOF
                                echo "$DOCKERHUB_PASSWORD" | docker login -u "$DOCKERHUB_USERNAME" --password-stdin
                                docker pull ${DOCKER_IMAGE}
                                docker rm -f calculator-app || true
                                docker run -d -p 80:5000 --name calculator-app ${DOCKER_IMAGE}
                        EOF
                        '''
                    }
                }
            }
        }
    }
}
