// executor project main.go
package main

import (
	"flag"
	"fmt"
	"io"
	"os"
	"path/filepath"

	"bytes"
	run "runtime"
	"strings"

	kubernetes "k8s.io/client-go/kubernetes"
	"k8s.io/client-go/tools/clientcmd"

	core_v1 "k8s.io/api/core/v1"
	"k8s.io/apimachinery/pkg/runtime"
	"k8s.io/client-go/rest"
	"k8s.io/client-go/tools/remotecommand"
)

type ExecCommander struct {
	namespace     string
	pod_list      []string
	command       []string
	mode          string
	containerName string

	result chan string
}

func NewExecCommander(command *string, containerName *string, pods *string, mode *string, namespace *string) *ExecCommander {

	pod_list := strings.Split(*pods, ",")
	command_list := strings.Split(*command, "\n")

	return &ExecCommander{
		namespace:     *namespace,
		pod_list:      pod_list,
		command:       command_list,
		mode:          *mode,
		containerName: *containerName,
		result:        make(chan string),
	}
}

func NewKubeClient(mode string) (*kubernetes.Clientset, *rest.Config) {
	// creates the in-cluster config
	var config *rest.Config
	var err error

	if mode == "inCluster" {
		config, err = rest.InClusterConfig()
		if err != nil {
			panic(err.Error())
		}
	} else if mode == "outCluster" {
		//test use out-cluster config
		var kubeconfig *string

		if home := homeDir(); home != "" {
			kubeconfig = flag.String("kubeconfig", filepath.Join(home, ".kube", "config"), "(optional) absolute path to the kubeconfig file")
		} else {
			kubeconfig = flag.String("kubeconfig", "", "absolute path to the kubeconfig file")
		}
		flag.Parse()

		// use the current context in kubeconfig
		config, err = clientcmd.BuildConfigFromFlags("", *kubeconfig)
		if err != nil {
			panic(err.Error())
		}
	} else {
		fmt.Print("error configuration in mode, use 'inCluster' or 'outCluster'.")
		os.Exit(1)
	}

	clientset, err := kubernetes.NewForConfig(config)
	if err != nil {

		panic(err.Error())
	}
	return clientset, config
}

func (e *ExecCommander) ExecCommand(index int, config *rest.Config, clientset *kubernetes.Clientset, stdin io.Reader) {
	for k := 0; k < len(e.command); k++ {
		req := clientset.Core().
			RESTClient().
			Post().
			Resource("pods").
			Name(e.pod_list[index]).
			Namespace(e.namespace).
			SubResource("exec")

		scheme := runtime.NewScheme()
		if err := core_v1.AddToScheme(scheme); err != nil {
			errs := e.pod_list[index] + "error adding to scheme: " + err.Error()
			e.result <- errs
		}
		parameterCodec := runtime.NewParameterCodec(scheme)

		req.VersionedParams(&core_v1.PodExecOptions{
			Command:   strings.Fields(e.command[k]),
			Container: e.containerName,
			Stdin:     stdin != nil,
			Stdout:    true,
			Stderr:    true,
			TTY:       false,
		}, parameterCodec)

		exec, err := remotecommand.NewSPDYExecutor(config, "POST", req.URL())
		if err != nil {
			errs := e.pod_list[index] + "error while creating Executor: " + err.Error()
			e.result <- errs
		}

		var stdout, stderr bytes.Buffer
		err = exec.Stream(remotecommand.StreamOptions{
			Stdin:  stdin,
			Stdout: &stdout,
			Stderr: &stderr,
			Tty:    false,
		})
		if err != nil {
			errs := e.pod_list[index] + "error in Stream: " + err.Error()
			e.result <- errs
		}

		if stderr.Len() != 0 {
			res := e.pod_list[index] + "STDERR: " + stderr.String()
			e.result <- res
		} else {
			res := "In Pod " + e.pod_list[index] + " with command " + "\"" + e.command[k] + "\"" + " OutPut\n" + stdout.String()
			e.result <- res
		}
	}
}

func homeDir() string {
	if h := os.Getenv("HOME"); h != "" {
		return h
	}
	return os.Getenv("USERPROFILE") // windows
}

func main() {
	var containerName string
	namespace := flag.String("namespace", "default", "namespace the pod is from")
	Pods := flag.String("Pods", "", "pod list")
	command := flag.String("command", "ls", "the command you wish to run")
	mode := flag.String("mode", "outCluster", "the mode inCLuster or outCluster")
	flag.Parse()

	run.GOMAXPROCS(4)
	commander := NewExecCommander(command, &containerName, Pods, mode, namespace)
	clientset, config := NewKubeClient(commander.mode)

	for i := 0; i < len(commander.pod_list); i++ {
		go commander.ExecCommand(i, config, clientset, nil)
	}

	for i := 1; i <= len(commander.pod_list)*len(commander.command); i++ {
		out := <-commander.result
		fmt.Println(out)
		
	}
}
