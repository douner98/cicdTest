pipeline {
    agent any

    environment{
        P_PROFILE = "${env.BRANCH_NAME == "develop" ? "dev" : env.BRANCH_NAME == "main" ? "stg" : "prd"}"
        SERVER_LIST = "${env.BRANCH_NAME == "develop" ? "jenkins_test_ec2" : env.BRANCH_NAME == "main" ? "jenkins_test_ec2" : "prd"}"
        REMOTE_ROOT_DIR = "/sorc001/BATCH"
//        REMOTE_SUB_DIR = "COM/SH,COM/PY,COM/SH/AA1" // 디렉토리 목록을 쉼표로 구분하여 환경 변수에 저장
        REMOTE_BATCH_COM_DIR = """
                        COM/SH
                        COM/PY
                    """
        REMOTE_BATCH_ORG_DIR = """
                        ORG/AAA
                        ORG/AAA/AA1
                        ORG/BBB
                    """
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
        
        stage('DEPLOY BATCH COM') {
            steps {
                
                echo "Start DEPLOY ${REMOTE_ROOT_DIR}/BATCH/COM"

                script {
                    echo "P_PROFILE: ${P_PROFILE}"
                    echo "SERVER_LIST: ${SERVER_LIST}"

                    switch("{$env.BRANCH_NAME}") {
                        case "develop":
                            echo "develop DEPLOY"
                            break
                        case "main":
                            echo "prod DEPLOY"
                            break
                    }

                    // REMOTE_BATCH_COM_DIR 목록 분리하여 배열 저장.
                    def directorys = env.REMOTE_BATCH_COM_DIR.split('\n')

                    SERVER_LIST.tokenize(',').each{
                        echo "DEPLOY J-JOBS SERVER: ${it}"

                        // 각 디렉토리별 루프 수행
                        for (def dir in directorys) {
                            def trimmedDir = dir.trim() // 공백 제거
                            echo "DEPLOY Start ${REMOTE_ROOT_DIR}/${trimmedDir}"
                            sshPublisher(
                                publishers: [
                                    sshPublisherDesc(
                                        configName: "${it}",
                                        transfers: [
                                            sshTransfer(
                                                execCommand: "mkdir -p /${REMOTE_ROOT_DIR}/${trimmedDir}" // 디렉토리 생성
                                            ),
                                            sshTransfer(
                                                execCommand: '',
                                                execTimeout: 120000,
                                                flatten: false,
                                                makeEmptyDirs: false,
                                                noDefaultExcludes: false,
                                                patternSeparator: '[, ]+',
                                                remoteDirectory: "${REMOTE_ROOT_DIR}/${trimmedDir}",
                                                removePrefix: "${trimmedDir}/", // 복사할 파일의 기본 경로를 설정
                                                sourceFiles: "${trimmedDir}/*.sh, ${trimmedDir}/*.py, ${trimmedDir}/*.sql"
                                            )
                                        ],
                                        usePromotionTimestamp: false,
                                        useWorkspaceInPromotion: false,
                                        verbose: false
                                    )
                                ]
                            )
                            echo "DEPLOY Done ${REMOTE_ROOT_DIR}/${trimmedDir}"
                        }
                    }
                }

                echo "Finish DEPLOY ${REMOTE_ROOT_DIR}/BATCH/COM"
            }
        }

        stage('DEPLOY BATCH ORG') {
            steps {
                
                echo "Start DEPLOY ${REMOTE_ROOT_DIR}/BATCH/ORG"

                script {
                    echo "P_PROFILE: ${P_PROFILE}"
                    echo "SERVER_LIST: ${SERVER_LIST}"

                    switch("{$env.BRANCH_NAME}") {
                        case "develop":
                            echo "develop DEPLOY"
                            break
                        case "main":
                            echo "prod DEPLOY"
                            break
                    }

                    // REMOTE_BATCH_ORG_DIR 목록 분리하여 배열 저장.
                    def directorys = env.REMOTE_BATCH_ORG_DIR.split('\n')

                    SERVER_LIST.tokenize(',').each{
                        echo "DEPLOY J-JOBS SERVER: ${it}"

                        // 각 디렉토리별 루프 수행
                        for (def dir in directorys) {
                            def trimmedDir = dir.trim() // 공백 제거
                            echo "DEPLOY Start ${REMOTE_ROOT_DIR}/${trimmedDir}"
                            sshPublisher(
                                publishers: [
                                    sshPublisherDesc(
                                        configName: "${it}",
                                        transfers: [
                                            sshTransfer(
                                                execCommand: "mkdir -p /${REMOTE_ROOT_DIR}/${trimmedDir}" // 디렉토리 생성
                                            ),
                                            sshTransfer(
                                                execCommand: '',
                                                execTimeout: 120000,
                                                flatten: false,
                                                makeEmptyDirs: false,
                                                noDefaultExcludes: false,
                                                patternSeparator: '[, ]+',
                                                remoteDirectory: "${REMOTE_ROOT_DIR}/${trimmedDir}",
                                                removePrefix: "${trimmedDir}/", // 복사할 파일의 기본 경로를 설정
                                                sourceFiles: "${trimmedDir}/*.sh, ${trimmedDir}/*.py, ${trimmedDir}/*.sql"
                                            )
                                        ],
                                        usePromotionTimestamp: false,
                                        useWorkspaceInPromotion: false,
                                        verbose: false
                                    )
                                ]
                            )
                            echo "DEPLOY Done ${REMOTE_ROOT_DIR}/${trimmedDir}"
                        }
                    }
                }

                echo "Finish DEPLOY ${REMOTE_ROOT_DIR}/BATCH/ORG"
            }
        }
    }
}