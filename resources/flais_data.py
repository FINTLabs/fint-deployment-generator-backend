import types

flais_default = types.MappingProxyType({
    "apiVersion": "fintlabs.no/v1alpha1",
    "kind": "Application",
    "metadata": {
        "name": "flais-test-application",
        "namespace": "{org-dash}",
        "labels": {
            "app.kubernetes.io/name": "",
            "app.kubernetes.io/instance": "",
            "app.kubernetes.io/version": "latest",
            "app.kubernetes.io/component": "",
            "app.kubernetes.io/part-of": "",
            "fintlabs.no/team": "",
            "fintlabs.no/org-id": "{org-dot}"
        }
    },
    "spec": {
        "port": 8000,
        "orgId": "{org-dot}",
        "image": "docker/getting-started",
        "prometheus": {
            "enabled": True,
            "port": "80",
            "path": "/prometheus"
        },
        "resources": {
            "limits": {
                "memory": "512Mi",
                "cpu": "500m"
            },
            "requests": {
                "memory": "256Mi",
                "cpu": "250m"
            }
        }
    }
})
