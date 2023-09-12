pipeline {
    agent any

    stages {

        environment{
            P_PROFILE = "${env.BRANCH_NAME == "develop" ? "dev" : env.BRANCH_NAME == "main" ? "stg" : "prd"}"
            SERVER_LIST = "${env.BRANCH_NAME == "develop" ? "jenkins_test_ec2" : env.BRANCH_NAME == "main" ? "jenkins_test_ec2" : "prd"}"
        } 

        stage('Checkout') {
            steps {
                // Git 리포지토리에서 소스 코드 체크아웃
                checkout scm
            }
        }
        
        stage('DEPLOY') {
            steps {
                
                sh "echo 'start deploy'"

                script {

                    echo "SERVER_LIST: ${SERVER_LIST}"

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