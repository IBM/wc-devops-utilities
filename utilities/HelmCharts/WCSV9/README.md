1. Create RBAC for new namespace
If you want to use WCSV9 Helm Charts to deploy on a new namespace, please create the rbac for that namespace by edit rbac.yaml and change the namespace name with your target one.

2. Support Commerce 9.0.0.1
If you want to deploy Commerce 9.0.0.1, you must specify the value "CommerceVersion: 9.0.0.1 and OVERRIDE_PRECONFIG: true" in vaules.yaml, for 9.0.0.2 or higher, you can ignore this step

3. Helm Chart Version 0.1.2 + support session affinity config. But you need to manually create secret which should be issue from same CA which issue certification for backend service on ingress
IF enable session affinity, the ssl-passthrough can not work.

4. The ingress.yaml definition use nginx.ingress.kubernetes.io as the annotation prefix to match the latest ingress-lb-controller <br>

   ```
   changes in 0.13.0

   Image: quay.io/kubernetes-ingress-controller/nginx-ingress-controller:0.13.0

   New Features:

      NGINX 1.13.12
      Support for gRPC:
      The annotation nginx.ingress.kubernetes.io/grpc-backend: "true" enable this feature
      If the gRPC service requires TLS nginx.ingress.kubernetes.io/secure-backends: "true"
   ```


  IF you deploy this Helm Charts on ICP, Before you run the helm install, please manually change the ingress.yaml first as below, Otherwise you may meet 502 or 503 when you access with exposed hostname.
  Becaused the prefix annotation for embedded ingress-lb-controller be specified as  ingress.kubernetes.io/* for better backwards compatible

   * Open WCSV9/Template/ingress.yaml
   * Change ‘nginx.ingress.kubernetes.io/secure-backends: “true”‘ to ‘ingress.kubernetes.io/secure-backends: “true”‘
   * Save WCSV9/Template/ingress.yaml

