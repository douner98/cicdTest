pipeline {
    agent any
    
    stages {
        
        stage('Deploy') {
            steps {
                // "Publish Over SSH" 플러그인을 사용하여 파일을 원격 서버로 업로드
                script {
                    def server = getServer('jenkins_test_ec2')
                    if (server) {
                        def remoteDir = server.getRemoteDirectory()
                        sshPublisher(
                            publishers: [
                                sshPublisherDesc(
                                    configName: 'jenkins_test_ec2',
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