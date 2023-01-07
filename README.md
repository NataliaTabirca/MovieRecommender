# MovieRecommender




- __Create kind cluster__ consisting of a control plane and two workers:

```sh
kind create cluster --config ./kind-config.yaml
```


- __Deploy__ the kubernetes-yaml folder

```sh
kubectl apply -R -f kubernetes-yaml
```

