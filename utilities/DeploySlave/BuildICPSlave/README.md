If use deployslave on ICP enviornment, please download helm client from ICP UI.

If the version can not match current helm server, you will get below error when do deployment

```
Error: transport is closing
panic: runtime error: invalid memory address or nil pointer dereference
[signal SIGSEGV: segmentation violation code=0x1 addr=0x0 pc=0x88b17b]

goroutine 1 [running]:
k8s.io/helm/pkg/tlsutil.ClientConfig(0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x1, 0x0, 0x1d, 0xc4202fa370, ...)
	/home/ubuntu/.go_workspace/src/k8s.io/helm/pkg/tlsutil/cfg.go:59 +0xeb
main.newClient(0x1, 0x1)
	/home/ubuntu/.go_workspace/src/k8s.io/helm/cmd/helm/helm.go:270 +0x129
main.ensureHelmClient(0x0, 0x0, 0x7ffe13bb2eb1, 0x1d)
	/home/ubuntu/.go_workspace/src/k8s.io/helm/cmd/helm/helm.go:258 +0x45
main.newInstallCmd.func1(0xc420353680, 0xc4201f3680, 0x1, 0x8, 0x0, 0x0)
	/home/ubuntu/.go_workspace/src/k8s.io/helm/cmd/helm/install.go:172 +0x285
k8s.io/helm/vendor/github.com/spf13/cobra.(*Command).execute(0xc420353680, 0xc4201f3600, 0x8, 0x8, 0xc420353680, 0xc4201f3600)
	/home/ubuntu/.go_workspace/src/k8s.io/helm/vendor/github.com/spf13/cobra/command.go:599 +0x3e9
k8s.io/helm/vendor/github.com/spf13/cobra.(*Command).ExecuteC(0xc4203befc0, 0xc4201da6c0, 0xc420519200, 0xc420529200)
	/home/ubuntu/.go_workspace/src/k8s.io/helm/vendor/github.com/spf13/cobra/command.go:689 +0x339
k8s.io/helm/vendor/github.com/spf13/cobra.(*Command).Execute(0xc4203befc0, 0x9, 0x9)
	/home/ubuntu/.go_workspace/src/k8s.io/helm/vendor/github.com/spf13/cobra/command.go:648 +0x2b
main.main()
	/home/ubuntu/.go_workspace/src/k8s.io/helm/cmd/helm/helm.go:154 +0x77
```
