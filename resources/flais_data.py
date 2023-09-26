flais_application = {
  "apiVersion": "fintlabs.no/v1alpha1",
  "kind": "Application",
  "metadata": {
    "name": "flais-test-application",
    "namespace": "rogfk-no",
    "labels": {
      "app.kubernetes.io/name": "flais-test-application",
      "app.kubernetes.io/instance": "flais-test-application_rogfk_no",
      "app.kubernetes.io/version": "latest",
      "app.kubernetes.io/component": "test-application",
      "app.kubernetes.io/part-of": "flais",
      "fintlabs.no/team": "flais",
      "fintlabs.no/org-id": "rogfk.no"
    }
  },
  "spec": {
    "port": 80,
    "orgId": "rogfk.no",
    "image": "docker/getting-started",
    "imagePullPolicy": "Always",
    "prometheus": {
      "enabled": true,
      "port": "80",
      "path": "/prometheus"
    },
    "env": [
      {
        "name": "ENV1",
        "value": "test"
      }
    ],
    "envFrom": [
      {
        "secretRef": {
          "name": "flais-test-application-secret"
        }
      }
    ],
    "onePassword": {
      "itemPath": "vaults/aks-alpha-vault/items/azurerator"
    },
    "kafka": {
      "enabled": true,
      "acls": [
        {
          "topic": "*.test.topic",
          "permission": "read"
        }
      ]
    },
    "database": {
      "enabled": true,
      "database": "fint-kontroll"
    },
    "url": {
      "hostname": "test.flais.io",
      "basePath": "/alpha/fintlabs-no"
    },
    "ingress": {
      "enabled": true,
      "basePath": "/alpha/fintlabs-no/api/users",
      "middlewares": [
        "fint-kontroll-sso"
      ]
    },
    "resources": {
      "limits": {
        "memory": "1024Mi",
        "cpu": "100m"
      },
      "requests": {
        "memory": "128Mi",
        "cpu": "100m"
      }
    },
    "restartPolicy": "Always",
    "replicas": 1,
    "strategy": {
      "type": "RollingUpdate",
      "rollingUpdate": {
        "maxSurge": 1,
        "maxUnavailable": 0
      }
    }
  }
}