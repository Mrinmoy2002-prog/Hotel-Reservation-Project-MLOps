pipeline{
    agent any

    stages{
        stage('Cloning GitHub repo to jenkins'){
            steps{
                script{
                    echo 'Cloning GitHub repo to Jenkins .........'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token', url: 'https://github.com/Mrinmoy2002-prog/Hotel-Reservation-Project-MLOps']])
                }
            }
        }
    }
}