pipeline{
    agent any

    environment {
        VENV_DIR = 'venv'
    }

    stages{
        stage('Cloning GitHub repo to jenkins'){
            steps{
                script{
                    echo 'Cloning GitHub repo to Jenkins .........'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token', url: 'https://github.com/Mrinmoy2002-prog/Hotel-Reservation-Project-MLOps']])
                }
            }
        }

        stage('Setting up our Virtual Envioronment and Installing Dependencies'){
            steps{
                script{
                    echo 'Setting up our Virtual Envioronment and Installing Dependencies .........'
                    sh '''
                    python -m venv ${VENV_DIR}
                    .${VENV_DIR}/bin/activate
                    pip install --upgrade pip
                    pip install -e .
                    '''
                }
            }
        }
    }
}