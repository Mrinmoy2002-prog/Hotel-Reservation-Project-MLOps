pipeline {
    agent any

    environment {
        VENV_DIR = 'venv'
        GCP_PROJECT = "mlops-new-447207"
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
                    
                    // Creates the venv and installs dependencies directly using the venv's pip
                    sh """
                    python -m venv ${VENV_DIR}
                    ${VENV_DIR}/bin/python -m pip install --upgrade pip
                    ${VENV_DIR}/bin/pip install -e .
                    """
                }
            }
        }
    }
}