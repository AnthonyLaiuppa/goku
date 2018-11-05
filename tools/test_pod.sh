kubectl create namespace goku 
kubectl config set-context $(kubectl config current-context) --namespace=goku
kubectl apply -f pod.yml
kubectl get pods --watch
