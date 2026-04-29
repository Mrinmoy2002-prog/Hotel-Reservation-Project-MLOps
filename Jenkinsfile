pipeline {
    agent any

    environment {
        VENV_DIR = 'venv'
        GCP_PROJECT = "plasma-bison-458014-d0"
        GCLOUD_PATH = "/var/jenkins_home/google-cloud-sdk/bin"
    }

    stages {
        stage('Cloning Github repo to Jenkins') {
            steps {
                script {
                    echo 'Cloning Github repo to Jenkins............'
                    
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token', url: 'https://github.com/Mrinmoy2002-prog/Hotel-Reservation-Project-MLOps.git']])
                }
            }
        }

        stage('Setting up our Virtual Environment and Installing dependancies') {
            steps {
                script {
                    echo 'Setting up our Virtual Environment and Installing dependancies............'
                    
                    sh """
                    python -m venv ${VENV_DIR}
                    ${VENV_DIR}/bin/python -m pip install --upgrade pip
                    ${VENV_DIR}/bin/pip install -e .
                    """
                }
            }
        }

        stage('Building and Pushing Docker Image to GCR') {
            steps {
                withCredentials([file(credentialsId: 'gcp-key' , variable : 'GOOGLE_APPLICATION_CREDENTIALS')]) {
                    script {
                        echo 'Building and Pushing Docker Image to GCR.............'
                        
                        sh """
                        export PATH=\$PATH:${GCLOUD_PATH}

                        gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}
                        gcloud config set project ${GCP_PROJECT}
                        gcloud auth configure-docker --quiet

                        docker build -t gcr.io/${GCP_PROJECT}/ml-project:latest .
                        docker push gcr.io/${GCP_PROJECT}/ml-project:latest
                        """
                    }
                }
            }
        }

        stage('Deploy to Google Cloud Run') {
            steps {
                withCredentials([file(credentialsId: 'gcp-key' , variable : 'GOOGLE_APPLICATION_CREDENTIALS')]) {
                    script {
                        echo 'Deploy to Google Cloud Run.............'
                        
                        sh """
                        export PATH=\$PATH:${GCLOUD_PATH}

                        gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}
                        gcloud config set project ${GCP_PROJECT}

                        gcloud run deploy ml-project \\
                            --image=gcr.io/${GCP_PROJECT}/ml-project:latest \\
                            --platform=managed \\
                            --region=us-central1 \\
                            --port=5000 \\
                            --allow-unauthenticated
                        """
                    }
                }
            }
        }
    }
}