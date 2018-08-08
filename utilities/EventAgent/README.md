# EventAgent #

EventAgent support predefined Jenkins Job "KubeExec_Base" to exec shell command without connecting the terminal of containers. And you can run these command in multiple containers at the same time.

EventAgent could help you to run command within container of Kubernetes cluster, just like 'kubectl exec'. Better than 'kubectl exec', the agent will help you find all the container in all namespaces. And you can find the specific container by Pod label. Then, what else you need to do is just selecting these containers and inputing the command.

EventAgent only support single command once, it can execute multiple command in future.

## Build ##
To build EventAgent from source code, please run below shell script under EventAgent folder:

```
./Build.sh

```

## Push Docker Image ##
After you get EventAgent Docker image, you need to push it to your private Docker Image Repository which you configured in DeployController under "commerce" library with "latest" tag.

## Run KubeExec_Base ##

IF you already build and upload the EventAgent to Docker Image Repository, you can launch predefined Job "KubeExec_Base" by following the instruction on Job

This Job will start a temporary Pod with EventAgent which will call Kubernetes API to launch defined command on target Pod. When command finish on all target Pods,

This Pod will exit.

