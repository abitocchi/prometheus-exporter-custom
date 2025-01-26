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

    volumes:
    - name: buildah-storage
      emptyDir: {}

    serviceAccountName: jenkins

    containers:
    - name: helm
      image: docker.io/alpine/helm:3
      imagePullPolicy: IfNotPresent
      tty: true
      command:
      - sleep
      - infinity
      resources:
        limits:
          cpu: 250m
          memory: 128Mi
        requests:
          cpu: 50m
          memory: 32Mi

    - name: buildah
      image: quay.io/buildah/stable:latest
      imagePullPolicy: IfNotPresent
      securityContext:
        runAsUser: 1000
      envFrom:
      - secretRef:
          name: registry-credentials
      tty: true
      command:
      - sleep
      - infinity
      resources:
        limits:
          cpu: 500m
          memory: 500Mi
        requests:
          cpu: 50m
          memory: 50Mi

      volumeMounts:
      - name: buildah-storage
        mountPath: /usr/lib/containers/storage/overlay-images
                    '''
                    cloud 'kubernetes'
                    }
                }
            stages {
                stage('Detect image version'){
                    steps{
                        container('jnlp'){
                            script {
                                // Variables definition
                                env.IMAGE_REGISTRY = "quay.io/abitocchi"
                                env.IMAGE_NAME     = "pipeline-image"
                                if (fileExists("version")){
                                    env.IMAGE_VERSION = readFile("version").replaceAll("\n", "").replaceAll("\r", "")
                                }
                                else {
                                    env.IMAGE_VERSION = "latest"
                                }
                            }
                        }
                    }
                }
                stage('Build Image'){
                    steps{
                        container('buildah'){
                            script {
                                sh '''
                                buildah --storage-driver vfs bud --isolation chroot -t "$IMAGE_REGISTRY/$IMAGE_NAME:$IMAGE_VERSION"
                                '''
                            }
                        }
                    }
                }
                stage('Push Image'){
                    steps{
                        container('buildah'){
                            script {
                                sh '''
                                set +x
                                buildah login quay.io -u "$username" -p "$password"
                                set -x
                                buildah --storage-driver vfs push "$IMAGE_REGISTRY/$IMAGE_NAME:$IMAGE_VERSION"
                                '''
                            }
                        }
                    }
                }
                stage('Deploy'){
                    steps{
                        container('helm'){
                            script {
                                sh '''
                                helm upgrade \
                                    --install \
                                    --set image.tag="$IMAGE_VERSION" \
                                    --set image.repository="$IMAGE_REGISTRY/$IMAGE_NAME" \
                                    --namespace devops \
                                    --create-namespace \
                                    prom-exp \
                                    prometheus-exporter/ 
                                '''
                            }
                        }
                    }
                }
            }
        }
    }
}