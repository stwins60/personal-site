pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = credentials('1686a704-e66e-40f8-ac04-771a33b6256d')
        SCANNER_HOME= tool 'sonar-scanner'
        IMAGE_TAG = "v.0.${env.BUILD_NUMBER}"
        IMAGE_NAME = "idrisniyi94/personal-site:${IMAGE_TAG}"
        BRANCH_NAME = "${GIT_BRANCH.split('/')[1]}"
        // RECAPTCHA_SITE_KEY = "${env.RECAPTCHA_SITE_KEY}"
        // RECAPTCHA_SECRET_KEY = "${env.RECAPTCHA_SECRET_KEY}"
        // SENDGRID_API_KEY = "${env.SENDGRID_API_KEY}"
        // SNYK_API_TOKEN = credentials('SNYK-TOKEN')
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
        stage('Pytest') {
            steps {
                script {
                    sh "python3 -m pip install -r requirements.txt --no-cache-dir --break-system-packages"
                    sh "pytest --cov=app --cov-report=xml:test-reports/coverage.xml --junitxml=test-reports/pytest.xml"
                    sh "ls -la test-reports"
                    junit testResults: 'test-reports/*.xml'
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
                    sh "docker build -t $IMAGE_NAME ."
                    echo "Image built successful"
                }
            }
        }
        stage("Trivy Image Scan") {
            steps {
                script {
                    sh "trivy image $IMAGE_NAME"
                }
            }
        }
        stage("Docker Push") {
            steps {
                script {
                    sh "docker push $IMAGE_NAME"
                }
            }
        }
        stage('Deploy to K8S') {
            steps {
                script {
                    dir('./k8s') {
                        withKubeCredentials(kubectlCredentials: [[caCertificate: '', clusterName: '', contextName: '', credentialsId: 'fff8a37d-0976-4787-a985-a82f34d8db40', namespace: '', serverUrl: '']]) {
                            sh "sed -i 's|IMAGE_NAME|${IMAGE_NAME}|g' deployment.yaml"
                            sh "kubectl apply -f deployment.yaml"
                            sh "kubectl apply -f service.yaml"

                            def rolloutStatus = sh(script: "kubectl rollout status deployment personal-site -n personal-site", returnStatus: true)
                            def deploymentCondition = sh(script: "kubectl get deploy personal-site -n personal-site -o jsonpath='{.status.conditions[?(@.type==\"Available\")].status}'", returnStdout: true).trim()
                            def podName = sh(script: "kubectl get pods -n personal-site -l app=personal-site -o jsonpath='{.items[-1:].metadata.name}'", returnStdout: true).trim()
                            def lastErrorLogs = sh(script: "kubectl logs ${podName} -n personal-site --tail=50", returnStdout: true).trim()


                            if (rolloutStatus != 0) {
                                // Send the Slack message with rollout status and last error logs
                                slackSend channel: '#alerts', color: 'danger', message: """Deployment to Kubernetes failed. Check the logs for more information. 
                                More Info: ${env.BUILD_URL} 
                                Rollout Status: ${deploymentRolloutStatus} 
                                Last Error Logs: ${lastErrorLogs}"""
                            }
                            else {
                                slackSend channel: '#alerts', color: 'good', message: "Deployment to Kubernetes successful. More Info: ${env.BUILD_URL}"
                            }
                        }
                    }
                }
            }
        }
        // stage("Deploy") {
        //     steps {
        //         script {
        //             def containerName = 'personal-site'
        //             def isRunning = sh(script: "docker ps -a | grep ${containerName}", returnStatus: true)
        //             if(isRunning == 0) {
        //                 sh "docker rm -f ${containerName}"
        //                 dir("terraform") {
        //                     sh "terraform init"
        //                     sh "terraform apply -auto-approve -var 'image_name=$IMAGE_NAME' -var 'image_tag=$IMAGE_TAG' -var 'container_name=$containerName' -var 'external_port=5489'"
        //                 }
        //             }
        //             else {
        //                 // sh "docker run -d --name ${containerName} -p 5489:5001 --restart unless-stopped $IMAGE_NAME:$IMAGE_TAG"
        //                 dir("terraform") {
        //                     sh "terraform init"
        //                     sh "terraform apply -auto-approve -var 'image_name=$IMAGE_NAME' -var 'image_tag=$IMAGE_TAG' -var 'container_name=$containerName' -var 'external_port=5489'"
        //                 }
                        
        //             }
        //         }
        //     }
        // }
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