pipeline {
    agent any

    environment{
        P_PROFILE = "${env.BRANCH_NAME == "develop" ? "dev" : env.BRANCH_NAME == "main" ? "stg" : "prd"}"
        SERVER_LIST = "${env.BRANCH_NAME == "develop" ? "jenkins_test_ec2" : env.BRANCH_NAME == "main" ? "jenkins_test_ec2" : "prd"}"
        REMOTE_DIR = "/sorc001/BATCH"
        DIR_LIST = "COM/SH,COM/PY,COM/SH/AA1" // 디렉토리 목록을 쉼표로 구분하여 환경 변수에 저장
    } 

    parameters{
        choice(name:'SONARQUBE' , choices: ['NO','YES'])
        choice(name:'TEST' , choices: ['NO','YES'])
    }

    stages {

        stage('Checkout') {
            steps {
                // Git 리포지토리에서 소스 코드 체크아웃
                checkout scm
            }
        }
        
        stage('DEPLOY') {
            steps {
                
                echo "start deploy"

                script {
                    echo "P_PROFILE: ${P_PROFILE}"
                    echo "SERVER_LIST: ${SERVER_LIST}"

                    switch("{$env.BRANCH_NAME}") {
                        case "develop":
                            echo "develop"
                            break
                        case "main":
                            echo "prod"
                            break
                    }

                    // 폴더 목록을 쉼표로 분리하여 배열로 만듭니다.
                    def folders = env.DIR_LIST.split(',')

                    SERVER_LIST.tokenize(',').each{
                        echo "SERVER: ${it}"

                        // 각 폴더에 대한 루프
                        for (def folder in folders) {
                            
                            sshPublisher(
                                publishers: [
                                    sshPublisherDesc(
                                        configName: "${it}",
                                        transfers: [
                                            sshTransfer(
                                                execCommand: "mkdir -p /sorc001/BATCH/${folder}" // 실행할 SSH 명령
                                            ),
                                            sshTransfer(
                                                execCommand: '',
                                                execTimeout: 120000,
                                                flatten: false,
                                                makeEmptyDirs: false,
                                                noDefaultExcludes: false,
                                                patternSeparator: '[, ]+',
                                                remoteDirectory: "${REMOTE_DIR}/${folder}",
                                                removePrefix: "${folder}/", // 복사할 파일의 기본 경로를 설정
                                                sourceFiles: "${folder}/*.sh, ${folder}/*.py, ${folder}/*.sql"
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
}