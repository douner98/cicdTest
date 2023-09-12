pipeline {
    agent any
    
    stages {

        environment {
            GIT_URL = "https://github.com/douner98/cicdTest.git"
            GIT_CREDENTIAL = 'gitHubDouner98'
            P_PROFILE = "${env.BRANCH_NAME == "develop" ? "dev" : env.BRANCH_NAME == "main" ? "stg" : "prd"}"
            SERVER_LIST = "${env.BRANCH_NAME == "develop" ? "jenkins_test_ec2" : "env.BRANCH_NAME == "main" ? "jenkins_test_ec2" : "prd"}"
        }

         stage('Checkout AAA') {
            steps {
                script {
                    def gitUrl = env.GIT_URL
                    def gitCredential = env.GIT_CREDENTIAL
                    checkout([$class: 'GitSCM', branches: "{$env.BRANCH_NAME}", userRemoteConfigs: [[url: gitUrl, credentialsId: gitCredential]]])
                }
            }
        }
        
        stage('Deploy') {
            steps {
                // "Publish Over SSH" 플러그인을 사용하여 파일을 원격 서버로 업로드

                script {
                    switch("{$env.BRANCH_NAME}") {
                        case "develop":
                            echo "develop"
                            break
                        case "main":
                            echo "prod"
                            break
                    }

                    SERVER_LIST.tokenize(',').each{
                        echo "SERVER: ${it}"

                        
                        sshPublisher(
                            publishers: [
                                sshPublisherDesc(
                                    configName: '${it}',
                                    transfers: [
                                        sshTransfer(
                                            execCommand: '',
                                            execTimeout: 120000,
                                            flatten: false,
                                            makeEmptyDirs: false,
                                            noDefaultExcludes: false,
                                            patternSeparator: '[, ]+',
                                            remoteDirectory: remoteDir,
                                            removePrefix: 'source',
                                            sourceFiles: '**/*'
                                        )
                                    ],
                                    usePromotionTimestamp: false,
                                    useWorkspaceInPromotion: false,
                                    verbose: false
                                )
                            ]
                        )
                    }
                }
            }
        }
    }
}