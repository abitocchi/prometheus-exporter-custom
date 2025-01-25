pipeline {
    agent none
    stages {
        stage("Main"){
            agent {
                kubernetes {
                    yaml '''
    apiVersion: v1
    kind: Pod
    spec:

        securityContext:
            runAsUser: 1000

        containers:
          - name: buildah
            image: quay.io/buildah/stable:latest
            imagePullPolicy: IfNotPresent
            tty: true
            command:
            - sleep
            - infinity
            resources:
            limits:
                cpu: 100m
                memory: 50Mi
            requests:
                cpu: 50m
                memory: 32Mi
                    '''
                    cloud 'kube-helm'
                    }
                }
            stages {
                stage('Build Image'){
                    steps{
                        container('buildah'){
                            script {
                                sh "buildah --storage-driver vfs bud --isolation chroot -t quay.io/abitocchi/pipeline-image:1.0.0"
                            }
                        }
                    }
                }
            }
        }
    }
}