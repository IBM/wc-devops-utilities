# EventAgent 

EventAgent is a tool based Jenkins Pipeline to exec shell command without connecting the terminal of containers. And you can run these command in multiple containers at the same time.

EventAgent could help you to run command within container of Kubernetes cluster, just like 'kubectl exec'. Better than 'kubectl exec', the agent will help you find all the container in all namespaces. And you can find the specific container by Pod label. Then, what else you need to do is just selecting these containers and inputing the command.

EventAgent only support single command once, it can execute multiple command in future.

================================================================================ </br>
### To build EventAgent from source code, you need:

```
cp -r <path to executor> $GOPATH/src

go get  k8s.io/client-go/...

go build -i $GOPATH/src/executor/main.go

```

or you could build from source code with the docker. run Build.sh, you will get the binary in folder 'EventAgent'