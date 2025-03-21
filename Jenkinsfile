pipeline {
    agent any
    
    environment {
        DOCKERHUB_USERNAME = credentials('dockerhub-username')
        DOCKERHUB_PASSWORD = credentials('dockerhub-password')
        EC2_HOST = credentials('ec2-host')
        EC2_USER = credentials('ec2-user')
        EC2_SSH_PRIVATE_KEY = credentials('ec2-ssh-private-key')
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
                    python3 -m pip install --upgrade pip
                    pip3 install -r requirements.txt
                '''
            }
        }
        
        stage('Run Tests') {
            steps {
                sh 'pytest'
            }
        }
        
        stage('Build and Push Docker Image') {
            steps {
                script {
                    docker.withRegistry('https://index.docker.io/v1/', 'docker-hub-credentials') {
                        sh '''
                            docker build -t $DOCKERHUB_USERNAME/calculator-app:latest .
                            docker push $DOCKERHUB_USERNAME/calculator-app:latest
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
                                docker pull $DOCKERHUB_USERNAME/calculator-app:latest
                                docker rm -f calculator-app || true
                                docker run -d -p 80:5000 --name calculator-app $DOCKERHUB_USERNAME/calculator-app:latest
                            EOF
                        '''
                    }
                }
            }
        }
    }
}
