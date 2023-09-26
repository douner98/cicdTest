pipeline {
    agent any

    // 환경변수 설정
    environment{
        // 개발배포 or 운영배포 여부
        P_PROFILE = "${env.BRANCH_NAME == "develop" ? "dev" : env.BRANCH_NAME == "main" ? "stg" : "prd"}"

        // 타겟서버 정보 (Jenkins SSH Server에 등록된 정보 : Jenkins 관리자 권한)
        SERVER_LIST = "${env.BRANCH_NAME == "develop" ? "jenkins_test_ec2" : env.BRANCH_NAME == "main" ? "jenkins_test_ec2" : "prd"}"

        // 타겟서버 배포 경로
        REMOTE_ROOT_DIR = "/sorc001/BATCH"

        REMOTE_BATCH_ENV_DIR = "COM/ENV"

        // Jenkins은 Git에 등록된 폴더는 자동으로 생성 해주는 기능이 없음
        // 배포 해야할 디렉토리가 추가될 경우 아래와 같이 추가할 것!
        // $REMOTE_ROOT_DIR/BATCH/COM 배포 경로
        REMOTE_BATCH_COM_DIR = """
                        COM/SH
                        COM/PY
                    """
        // $REMOTE_ROOT_DIR/BATCH/ORG 배포 경로
        REMOTE_BATCH_ORG_DIR = """
                        ORG/AAA
                        ORG/AAA/AA1
                        ORG/BBB
                    """
    } 

    parameters {
        booleanParam(name: 'DEPLOY_BATCH_COM_ENV', defaultValue: true, description: "deploy files to the /BATCH/COM/ENV path?")
        booleanParam(name: 'DEPLOY_BATCH_COM', defaultValue: true, description: "deploy files to the /BATCH/COM path?")
        booleanParam(name: 'DEPLOY_BATCH_ORG', defaultValue: true, description: "deploy files to the /BATCH/ORG path?")
    }

    stages {

        stage('Checkout') {
            steps {
                // Git 리포지토리에서 소스 코드 체크아웃
                checkout scm
            }
        }

        stage('DEPLOY BATCH COM ENV') {
            when {
                expression {
                    def isRun = params.DEPLOY_BATCH_COM_ENV == true
                    if (!isRun) {
                        echo 'Skipping Stage A because DEPLOY_BATCH_COM_ENV is set to false'
                    }
                    return isRun
                }
            }
            steps {
                echo "Start DEPLOY ${REMOTE_ROOT_DIR}/BATCH/COM/ENV"
                script {
                    echo "P_PROFILE: ${P_PROFILE}"
                    echo "SERVER_LIST: ${SERVER_LIST}"
                    def sourceEnvFile = ''
                    def targetEnvFile = 'anenv.ini'

                    switch("{$P_PROFILE}") {
                        case "dev":
                            echo "develop DEPLOY"
                            sourceEnvFile = 'env_dev.ini'
                            break
                        case "prd":
                            echo "prod DEPLOY"
                            sourceEnvFile = 'env_prd.ini'
                            break
                    }

                    // REMOTE_BATCH_COM_DIR 목록 분리하여 배열 저장.
                    def dir = env.REMOTE_BATCH_ENV_DIR

                    SERVER_LIST.tokenize(',').each{
                        echo "DEPLOY J-JOBS SERVER: ${it}"

                        echo "sourceEnvFile: ${sourceEnvFile}"
                        echo "targetEnvFile: ${targetEnvFile}"
                        
                        def trimmedDir = dir.trim() // 공백 제거
                        echo "DEPLOY Start ${REMOTE_ROOT_DIR}/${trimmedDir}"

                        echo "cp /${REMOTE_ROOT_DIR}/${trimmedDir}/${sourceEnvFile} /${REMOTE_ROOT_DIR}/${trimmedDir}/${targetEnvFile}"

                        sshPublisher(
                            publishers: [
                                sshPublisherDesc(
                                    configName: "${it}",
                                    transfers: [
                                        sshTransfer(
                                            execCommand: "mkdir -p /${REMOTE_ROOT_DIR}/${trimmedDir}" // 디렉토리 생성
                                        ),
                                        sshTransfer(
                                            execCommand: "cp /${REMOTE_ROOT_DIR}/${trimmedDir}/${sourceEnvFile} /${REMOTE_ROOT_DIR}/${trimmedDir}/${targetEnvFile}",
                                            execTimeout: 120000,
                                            flatten: false,
                                            makeEmptyDirs: false,
                                            noDefaultExcludes: false,
                                            patternSeparator: '[, ]+',
                                            remoteDirectory: "${REMOTE_ROOT_DIR}/${trimmedDir}",
                                            removePrefix: "${trimmedDir}/", // 복사할 파일의 기본 경로를 설정
                                            sourceFiles: "${trimmedDir}/*.ini"
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

                echo "Finish DEPLOY ${REMOTE_ROOT_DIR}/BATCH/COM"
            }
        }
        
        stage('DEPLOY BATCH COM') {
            when {
                expression {
                    def isRun = params.DEPLOY_BATCH_COM == true
                    if (!isRun) {
                        echo 'Skipping Stage A because DEPLOY_BATCH_COM is set to false'
                    }
                    return isRun
                }
            }
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
            when {
                expression {
                    def isRun = params.DEPLOY_BATCH_ORG == true
                    if (!isRun) {
                        echo 'Skipping Stage A because DEPLOY_BATCH_ORG is set to false'
                    }
                    return isRun
                }
            }
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