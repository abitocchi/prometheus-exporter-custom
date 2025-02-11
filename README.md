# prometheus-exporter

An application that allows to increment a counter for a simple metric and to retrieve the relative value.

## how to deploy

Use the following command to build the container image
```bash
# the address of the container registry i.e. docker.io, quay.io, ...
registry_address=""

# the image name i.e. my-prometheus-exporter
image_name="" 

podman build -t $registry_address/$image_name:latest .
```

Then push the builded image in the container registry
```bash
podman push $registry_address/$image_name:latest
```

And in the end deploy the application into the cluster
```bash
oc apply -f k8s
```

**NOTE**: Ensure to specify the proper image name and registry in this [file](k8s/deployment.yaml)

