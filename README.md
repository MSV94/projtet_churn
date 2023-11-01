# Projet Churn 
Réalisation d'un projet dans le cadre de la formation Machine Learning Engineer chez Datascientest en binôme :
- Maxime Ceriser
- Amrita Valdant

## Sujets :
De nombreuses entreprises notamment dans les télécoms utilisent différentes techniques qui peuvent prédire les taux de désabonnement et aider à concevoir des plans efficaces de fidélisation de la clientèle, car le coût d'acquisition d'un nouveau client est beaucoup plus élevé que le coût de fidélisation de l'existant.
Dans ce cadre à partir d'un Dataset contenant les caractéristiques d'un groupe de client ainsi que le choix de se désabonner ou non, nous avons développé un modèle de machine learning pouvant prédire le désabonnement d'un client. Nous avons ensuite mis ce modèle en production pour être utilisable par tous. 

## Les différentes étapes

### Création d’un modèle de Machine learning

Pour ce faire nous avons réalisé:
- Audit + Exploration des données
- Visualisation
- Entraînement et évaluation de modèles de machine learning

### L'API
Nous avons utilisé fastapi pour construire une API qui permettra d'interroger les différents modèles de machine learning créés. Elle permettra également d'accéder aux performances de l'algorithme sur les jeux de tests. Elle sera également munie d'un système d'authentification en base 64 avec la liste d'utilisateurs/mots de passe suivante :
alice: wonderland
bob: builder
clementine: mandarine

### Docker et Test
L'api ainsi crée sera mis dans une image docker grâce à un Dockerfile pour faciliter son déploiement.

Nous avons également réalisé une série de test pour vérifier le bon fonctionnement de l'API conteneurisée. Ces tests on également été conteneurisée et s'exécute sur l'api grâce à un docker compose.


### Deploiments avec Kubernetes

Pour la mise en production nous avons utilisé minikube qui permet d'utiliser Kubernetes. Nous avons utilisé un fichier de déploiement ainsi qu'un Service et un Ingress pour permettre le déploiement de l'API sur au moins 3 Pods.


## L'exécution du code 


### L'API
 
 Pour lancer l'api il faut depuis le dossier principal lancer les commandes suivantes :
```
cd docker-fastapi/api
```

 ```python
uvicorn application_churn_v2:api --reload
 ```

Vous pouvez interagir avec l'api via le l'interface da fastapi:
```
http://localhost:8000/docs
```
ou via des requêtes curl dont vous pourrez obtenir le code via le lien précèdent.

### Docker

Pour créer un docker contenant l'api et l'exécuter il faut depuis le dossier principal entrer les commandes suivantes.

Il faut d'abord lancer docker
```
sudo service docker start
```

Ensuite il faut créer l’image :
```
docker build -t api_churn ./docker-fastapi
```

Et enfin vous pouvez lancer le container:
```
docker container run -d --rm -p 8000:8000 api_churn
```
Ensuite vous pouvez vous connecter à l'api comme expliqué dans l'onglet précédent.


### Docker Compose
Le docker compose a été codé de manière à ce que si les images n'ont pas déjà été créées il les crée, il faut juste que vous n'ayez pas d'image ayant le même nom que celle utilisé pour le docker compose (api_churn, test_authentication, test_score, test_modelisation, test_get), si c'est le cas, supprimez les ou renommez les images dans le docker compose.

Pour lancer le docker vous pouvez utiliser la commande suivante:

```+
docker-compose up
```
Si vous voulez que lorsque que vous arrêtez votre docker compose les containers soient supprimés, utilisez la commande suivante.
```
docker-compose up && docker-compose rm -fs
```
Une fois exécutée vous obtiendrez le fichier log.txt dans le dossier principal ou sera affiché le résultat des tests.

### Kubernetes

Pour mettre l'application en production nous utilisons kubenetes.

### kubernetes en local

Si la machine d'où vous lancez kubernetes est la même que celle où vous avez vos images docker il suffit de créer l'image docker de l'api

```
docker build -t api_churn:1.0.0 ./docker-fastapi
```

ou bien si vous créez l'image précédemment vous pouvez également l'utiliser mais vous devez changer le fichier dans kubernetes : deployments.yml
en changeant la ligne "image: api_churn:1.0.0" par "image: api_churn".

### minikube

Si vous utilisez kubernetes avec minikube vous êtes obligé de recréer l'image dans minikube, pour ce faire lancez minikube
```
minikube start 
```
Ensuite entrez la ligne suivante pour pointer vers le docker dans votre machine virtuelle :
```
eval $(minikube docker-env)

```
Ensuite créez votre image :
```
docker build -t api_churn:1.0.0 ./docker-fastapi
```

### Déploiement

Si ingress n'est pas activé, utilisez la ligne suivante pour l’activer :
```
 minikube addons enable ingress
 ```

Allez dans le dossier kubernetes:
```
cd kubernetes
```
puis pour déployer et exposer l'api, lancez les trois lignes suivantes:
```
kubectl apply -f deployments.yml

kubectl apply -f service.yml

kubectl apply -f ingress.yml
```

pour obtenir l'adresse ip du ingress, lancez la commande:
```
kubectl get ingress
```

vous pouver ensuite vous connecter à l'api  soit sur votre machine en allant à l'adresse
```
http://{adresse ip ingress}:80/docs
```
soit si vous êtes sur un machine distante via un tunnel ssh qui relie le port 80 du ingress à votre machine :

```
ssh -i "data_enginering_machine.pem" ubuntu@{ip machine à distance} -fNL 8000:{adresse ip ingress}:80
```