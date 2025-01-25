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

    volumes:
    - name: buildah-storage
      emptyDir: {}

    containers:
    - name: buildah
      image: quay.io/buildah/stable:latest
      imagePullPolicy: IfNotPresent
      envFrom:
      - secretRef:
          name: registry-credentials
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

      volumeMounts:
      - name: buildah-storage
        mountPath: /usr/lib/containers/storage/overlay-images
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
                stage('Push Image'){
                    steps{
                        container('buildah'){
                            script {
                                sh """
                                buildah login quay.io -u \$username -p \$password
                                buildah push quay.io/abitocchi/pipeline-image:1.0.0
                                """
                            }
                        }
                    }
                }
                // stage('Deploy'){
                //     steps{
                //         container('jnlp'){
                //             script {
                //                 sh "helm install"
                //             }
                //         }
                //     }
                // }
            }
        }
    }
}