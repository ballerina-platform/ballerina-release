## Service Load Balancer Customizations
### Unhandled Services
By default, the Service Load Balancer binary will collect Pod information for all the listed Services in K8S. We can exclude certain Services being added to HAProxy like this, by specifying the following Service annotation in the Service artifact.

```yaml
apiVersion: v1
kind: Service
metadata:
  annotations:
    serviceloadbalancer/lb.private: "true"
```

If this Service annotation is present, the Service Load Balancer binary will not add it as an ACL rule or a Backend. This is useful for Services that are intended to be addressed only within the K8S Cluster.

### Reload time interval
By default, the Service Load Balancer binary had a job that kept on reloading the HAProxy config, every second. This has been made configurable and has been reduced to a default value of 1 minute. To customize this value, edit the following argument in the Service Load Balancer Replication Controller.

```yaml
--reload-interval=60s
```
