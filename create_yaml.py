deployment = """apiVersion: apps/v1
kind: Deployment
metadata:
  name: solarops
spec:
  replicas: 2
  selector:
    matchLabels:
      app: solarops
  template:
    metadata:
      labels:
        app: solarops
    spec:
      containers:
      - name: solarops
        image: solarops:v1
        imagePullPolicy: Never
        ports:
        - containerPort: 5000
"""

service = """apiVersion: v1
kind: Service
metadata:
  name: solarops-service
spec:
  selector:
    app: solarops
  ports:
  - port: 80
    targetPort: 5000
  type: NodePort
"""

open('kubernetes/deployment.yaml', 'w').write(deployment)
open('kubernetes/service.yaml', 'w').write(service)
print("Both files created successfully!"