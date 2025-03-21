pipeline {
    agent any

    environment {
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
                    docker.withRegistry('https://index.docker.io/v1/', 'docker-hub-credentials') {
                        sh '''
                            docker build -t ${DOCKER_REPO}:latest .
                            docker push $DOCKER_IMAGE
                        '''
                    }
                }
            }
        }

        stage('Deploy to AWS EC2') {
            steps {
                script {
                    withCredentials([sshUserPrivateKey(credentialsId: 'ec2-ssh-key', keyFileVariable: 'SSH_KEY')]) {
                        sh '''
                            chmod 600 $SSH_KEY
                            ssh -o StrictHostKeyChecking=no -i $SSH_KEY $EC2_USER@$EC2_HOST << 'EOF'
                                docker pull $DOCKER_IMAGE
                                docker rm -f calculator-app || true
                                docker run -d -p 80:5000 --name calculator-app $DOCKER_IMAGE
                            EOF
                        '''
                    }
                }
            }
        }
    }
}
