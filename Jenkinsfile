pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = credentials('d4506f04-b98c-47db-95ce-018ceac27ba6')
        SCANNER_HOME= tool 'sonar-scanner'
        IMAGE_NAME = 'idrisniyi94/personal-site'
        IMAGE_TAG = "${env.BUILD_NUMBER}"
        RECAPTCHA_SITE_KEY = "${env.RECAPTCHA_SITE_KEY}"
        RECAPTCHA_SECRET_KEY = "${env.RECAPTCHA_SECRET_KEY}"
        SENDGRID_API_KEY = "${env.SENDGRID_API_KEY}"
        SNYK_API_TOKEN = credentials('SNYK-TOKEN')
    }

    stages {
        stage('Clean workspace') {
            steps {
                cleanWs()
            }
        }
        stage('Checkout') {
            steps {
                git branch: 'master', url: 'https://github.com/stwins60/personal-site.git'
            }
        }
        stage('Install Dependencies') {
            steps {
                script {
                    sh "pip install -r requirements.txt --no-cache-dir"
                }
            }
        }
        stage('Sonarqube Analysis') {
            steps {
                script {
                    withSonarQubeEnv('sonar-server') {
                        sh "$SCANNER_HOME/bin/sonar-scanner -Dsonar.projectKey=personal-site -Dsonar.projectName=personal-site"
                    }
                }
            }
        }
        stage('Quality Gate') {
            steps {
                script {
                    withSonarQubeEnv('sonar-server') {
                        waitForQualityGate abortPipeline: false, credentialsId: 'sonar-token'
                    }
                }
            }
        }
        // stage('Pytest') {
        //     steps {
        //         script {
        //             sh "pip install -r requirements.txt --no-cache-dir"
        //             sh "python3 -m pytest --cov=app --cov-report=xml --cov-report=html"
        //         }
        //     }
        // }
        stage('OWASP') {
            steps {
                dependencyCheck additionalArguments: '--scan ./ --disableYarnAudit --disableNodeAudit --nvdApiKey 4bdf4acc-8eae-45c1-bfc4-844d549be812', odcInstallation: 'DP-Check'
                dependencyCheckPublisher pattern: '**/dependency-check-report.xml'
            }
        }
        stage('Trivy FS Scan') {
            steps {
                script {
                    sh "trivy fs ."
                }
            }
        }
        // stage('Test') {
        //     steps {
        //         echo 'Testing...'
        //         sh "snyk auth $SNYK_API_TOKEN"
        //         sh "snyk monitor --org=37a4a89a-0342-47ab-9298-9f05eaae71f9 --file=requirements.txt --package-manager=pip"
        //         sh "snyk monitor --org=37a4a89a-0342-47ab-9298-9f05eaae71f9 --file=Dockerfile"
        //     }
        // }
        stage("Login to DockerHub") {
            steps {
                sh "echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin"
                echo "Login Successful"
            }
        }
        stage("Docker Build") {
            steps {
                script {
                    sh "docker build -t $IMAGE_NAME:$IMAGE_TAG --build-arg RECAPTCHA_SITE_KEY=$RECAPTCHA_SITE_KEY --build-arg RECAPTCHA_SECRET_KEY=$RECAPTCHA_SECRET_KEY --build-arg SENDGRID_API_KEY=$SENDGRID_API_KEY ."
                    echo "Image built successful"
                }
            }
        }
        stage("Trivy Image Scan") {
            steps {
                script {
                    sh "trivy image $IMAGE_NAME:$IMAGE_TAG"
                }
            }
        }
        stage("Docker Push") {
            steps {
                script {
                    sh "docker push $IMAGE_NAME:$IMAGE_TAG"
                }
            }
        }
        stage("Deploy") {
            steps {
                script {
                    def containerName = 'personal-site'
                    def isRunning = sh(script: "docker ps -a | grep ${containerName}", returnStatus: true)
                    if(isRunning == 0) {
                        sh "docker rm -f ${containerName}"
                        dir("terraform") {
                            sh "terraform init"
                            sh "terraform apply -auto-approve -var 'image_name=$IMAGE_NAME' -var 'image_tag=$IMAGE_TAG' -var 'container_name=$containerName' -var 'external_port=5489'"
                        }
                    }
                    else {
                        // sh "docker run -d --name ${containerName} -p 5489:5001 --restart unless-stopped $IMAGE_NAME:$IMAGE_TAG"
                        dir("terraform") {
                            sh "terraform init"
                            sh "terraform apply -auto-approve -var 'image_name=$IMAGE_NAME' -var 'image_tag=$IMAGE_TAG' -var 'container_name=$containerName' -var 'external_port=5489'"
                        }
                        
                    }
                }
            }
        }
    }
    post {
        success {
           
            slackSend channel: '#alerts', color: 'good', message: "${currentBuild.currentResult}: \nJOB_NAME: ${env.JOB_NAME} \nBUILD_NUMBER: ${env.BUILD_NUMBER} \nBRANCH_NAME: ${env.BRANCH_NAME}. \n More Info ${env.BUILD_URL}"
        }
        failure {

            slackSend channel: '#alerts', color: 'danger', message: "${currentBuild.currentResult}: \nJOB_NAME: ${env.JOB_NAME} \nBUILD_NUMBER: ${env.BUILD_NUMBER} \nBRANCH_NAME: ${env.BRANCH_NAME}. \n More Info ${env.BUILD_URL}"
        }
    }
}