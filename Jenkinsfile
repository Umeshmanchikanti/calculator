pipeline {
    agent any

    environment {
        EC2_USER = 'ec2-user'
        EC2_HOST = '54.234.110.2'
        DOCKERHUB_USERNAME = 'umesh1027'
        DOCKER_IMAGE = "$DOCKERHUB_USERNAME/calculator-app:latest"
        DOCKER_REPO = 'umesh1027/calculator-app'
        KUBE_NAMESPACE = "default"
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

        stage('Deploy to Minikube') {
            steps {
                script {
                    sh '''
                        kubectl config use-context minikube
                        kubectl delete deployment calculator-app --ignore-not-found=true
                        kubectl delete service calculator-service --ignore-not-found=true

                        cat <<EOF | kubectl apply -f -
                        apiVersion: apps/v1
                        kind: Deployment
                        metadata:
                          name: calculator-app
                          namespace: $KUBE_NAMESPACE
                        spec:
                          replicas: 1
                          selector:
                            matchLabels:
                              app: calculator-app
                          template:
                            metadata:
                              labels:
                                app: calculator-app
                            spec:
                              containers:
                              - name: calculator-app
                                image: ${DOCKER_IMAGE}
                                ports:
                                - containerPort: 5000
                        EOF

                        cat <<EOF | kubectl apply -f -
                        apiVersion: v1
                        kind: Service
                        metadata:
                          name: calculator-service
                          namespace: $KUBE_NAMESPACE
                        spec:
                          selector:
                            app: calculator-app
                          ports:
                            - protocol: TCP
                              port: 80
                              targetPort: 5000
                          type: NodePort
                        EOF
                    '''
                }
            }
        }
    }
}
