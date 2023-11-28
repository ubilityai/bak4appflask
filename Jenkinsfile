pipeline {
    agent any
    environment {
        AZURE_TENANT_ID='bf4473ba-64c9-406a-8b83-bfeb911ef947'
        CONTAINER_REGISTRY='openopsacr'
        RESOURCE_GROUP='openopstest'
        CLUSTER_NAME='openopstestcluster'
        IMAGE_NAME='flaskapptest'
    }
    parameters {
        gitParameter name: 'REVISION',
                     type: 'PT_REVISION',
                     defaultValue: 'master'
    }
    stages{
        stage('Get the revision to download') {
            steps {
                checkout([$class: 'GitSCM',
                          branches: [[name: "${params.REVISION}"]],
                          doGenerateSubmoduleConfigurations: false,
                          extensions: [],
                          gitTool: 'Default',
                          submoduleCfg: [],
                          userRemoteConfigs: [[credentialsId: 'ibrahimnasri24-githubssh', url: 'git@github.com:ibrahimnasri24/FlaskAppTest.git']]
                        ])
            }
        }
        stage ('login to azure and build the image and push to acr') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'azure', passwordVariable: 'AZURE_CLIENT_SECRET', usernameVariable: 'AZURE_CLIENT_ID')]) {
                    sh 'az login --service-principal -u $AZURE_CLIENT_ID -p $AZURE_CLIENT_SECRET -t $AZURE_TENANT_ID'
                    sh 'az acr login --name $CONTAINER_REGISTRY --resource-group $RESOURCE_GROUP --expose-token'
                    sh 'az acr build --image $IMAGE_NAME:V$BUILD_NUMBER --registry $CONTAINER_REGISTRY --file Dockerfile . '
                }
            }
        }
        stage('Deploy the Artifact on Kubernetes') {
            steps {
                sh 'az aks get-credentials --resource-group $RESOURCE_GROUP --name $CLUSTER_NAME'
                sh 'originalfile="manifests/deployment.yaml";tmpfile=$(mktemp);cp --attributes-only --preserve $originalfile $tmpfile;export BUILD_NUMBER="$BUILD_NUMBER";echo "[INFO] Build Number $BUILD_NUMBER are deploying now"; cat $originalfile | envsubst > $tmpfile && mv $tmpfile $originalfile'
                sh 'kubectl delete -R -f manifests --ignore-not-found=true'
                sh 'sleep 30s'
                sh 'kubectl apply -R -f manifests'
            }
        }
    }
}
