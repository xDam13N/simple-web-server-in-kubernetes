# 1. Build docker image
Build docker image with application
```
docker build -t public.ecr.aws/z7s0e9e6/py-hnts:latest .
```
I've already pushed the latest image version to registry

# 2. Start minikube
```
minikube start
minikube addons enable ingress
minikube addons enable metrics-server
```

# 3. Deploy to minikube
Deploy ingress, service and deployment to minikube
```
kubectl apply -f Deploy_py-hnts.yaml
```
Define load balancer address and add `<address> py-hnts.internal` to `/etc/hosts` for local tests
```
kubectl get ingress | grep py-hnts.internal | awk '{print $4" py-hnts.internal"}' | sudo tee -a /etc/hosts
```
Check load balancing and service availability
```
$ curl py-hnts.internal 
Hostname: py-hnts-dp-7fc68d57d5-7hbnf
Timestamp: 1661275771
$ curl py-hnts.internal 
Hostname: py-hnts-dp-7fc68d57d5-hwr22
Timestamp: 1661275773
```
# 4. Deploy prom-stack and add podmonitor
Deploy prometheus stack
```
helm upgrade --install -n monitoring --create-namespace prom-stack monitoring/kube-prometheus-stack/ -f monitoring/values.prom-stack.yaml
```
Define load balancer address and add `<address> prom.internal` to `/etc/hosts` for local tests
```
kubectl get ingress -n monitoring | grep prom.internal | awk '{print $4" prom.internal"}' | sudo tee -a /etc/hosts
```
Add podmonitor for pods in deployment
```
kubectl apply -f monitoring/Add_py-hnts-pm.yaml
```

Please, wait until pod targets appeared in up state http://prom.internal/targets?search=py-hnts

Check pod metrics

`ab -c 10 -n 1000 http://py-hnts.internal/1` - generate 404 requests

`ab -c 10 -n 1000 http://py-hnts.internal/` - generate 200 requests

http://prom.internal/graph?g0.expr=py_hnts_requests_total&g0.tab=1&g0.stacked=0&g0.show_exemplars=0&g0.range_input=1h&g1.expr=sum(rate(py_hnts_requests_total%5B1m%5D))%20by%20(pod%2Cstatus)&g1.tab=0&g1.stacked=0&g1.show_exemplars=0&g1.range_input=30m

![](https://i2.paste.pics/3db0d7d15d8637f60f61dc00259e319f.png?trs=9f59c9f2a567119fcc2e8b52a42c7386dd05b3aa67f469f73ab2d3e723f5a88a)