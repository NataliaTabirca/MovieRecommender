terraform {
  required_providers {
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = ">= 2.0.0"
    }
  }
}

# Configure the Kubernetes provider
provider "kubernetes" {
  config_path = "../kind-config.yaml"
}

resource "kubernetes_config_map" "app-configmap" {
  metadata {
    name = "app-configmap"
  }

  data = {
    AMQPURL       = "amqp://rabbitmq-service"
    POSTGRES_HOST = "database-service"
    POSTGRES_PORT = "5432"
    PORT          = "8000"
  }
}

resource "kubernetes_secret" "database-secret" {
  metadata {
    name = "database-secret"
  }

  data = {
    POSTGRES_DB       = "ZGF0YWJhc2U="
    POSTGRES_PASSWORD = "cGFzcw=="
    POSTGRES_USER     = "dXNlcg=="
  }
}

resource "kubernetes_persistent_volume" "pv" {
  metadata {
    name = "postgres-pv-volume"
    labels = {
      type = "local"
    }
  }

  spec {
    capacity = {
      storage = "1Gi"
    }

    access_modes = ["ReadWriteMany"]

    storage_class_name = "standard"

    persistent_volume_source {
      vsphere_volume {
        volume_path = "/data"
      }
    }
  }
}

resource "kubernetes_persistent_volume_claim" "pvc" {
  metadata {
    name = "postgres-pvc"
  }

  spec {
    access_modes = ["ReadWriteMany"]
    resources {
      requests = {
        storage = "1Gi"
      }
    }

    storage_class_name = "standard"
  }
}

# CREATE DEPLOYMENTS
# Create a Deployment for the API
resource "kubernetes_deployment" "api" {
  metadata {
    name = "api-deployment"
    labels = {
      run = "api"
    }
  }

  spec {
    replicas = 1

    selector {
      match_labels = {
        app = "api"
      }
    }

    template {
      metadata {
        labels = {
          app = "api"
        }
      }

      spec {
        container {
          image = "dianapatru/movierecommender-api:2.0"
          name  = "api"
          port {
            container_port = 8000
          }
          env_from {
            secret_ref {
              name = "database-secret"
            }
            config_map_ref {
              name = "app-configmap"
            }
          }
        }
      }
    }
  }
}

# Create a Deployment for the business logic
resource "kubernetes_deployment" "business-logic" {
  metadata {
    name = "business-deployment"
    labels = {
      app = "business-deployment"
    }
  }

  spec {
    replicas = 1

    selector {
      match_labels = {
        app = "business-deployment"
      }
    }

    template {
      metadata {
        labels = {
          app = "business-deployment"
        }
      }

      spec {
        container {
          image = "dianapatru/movierecommender-business:1.0"
          name  = "business-deployment"
          env_from {
            secret_ref {
              name = "database-secret"
            }
            config_map_ref {
              name = "app-configmap"
            }
          }
        }
      }
    }
  }
}

# Create a Deployment for the RabbitMQ
resource "kubernetes_deployment" "rabbitmq" {
  metadata {
    name = "rabbitmq-deployment"
    labels = {
      run = "rabbitmq-deployment"
    }
  }

  spec {
    replicas = 1

    selector {
      match_labels = {
        app = "rabbitmq-deployment"
      }
    }

    template {
      metadata {
        labels = {
          app = "rabbitmq-deployment"
        }
      }

      spec {
        container {
          image = "rabbitmq:3"
          name  = "rabbitmq-deployment"
          port {
            container_port = 5672
          }
        }
      }
    }
  }
}

# Create a Deployment for the database
resource "kubernetes_deployment" "database" {
  metadata {
    name = "database-deployment"
    labels = {
      app = "database-deployment"
    }
  }

  spec {
    replicas = 1

    selector {
      match_labels = {
        app = "database-deployment"
      }
    }

    template {
      metadata {
        labels = {
          app = "database-deployment"
        }
      }

      spec {
        container {
          image = "dianapatru/movierecommender-database:1.0"
          name  = "database-deployment"
          volume_mount {
            name      = "database-volume"
            mount_path = "/var/lib/postgresql/data"
          }
          port {
            container_port = 5432
          }
          env_from {
            secret_ref {
              name = "database-secret"
            }
          }
        }
        volume {
          name = "database-volume"
          persistent_volume_claim {
            claim_name = "postgres-pvc"
          }
        }
      }
    }
  }
}

# CREATE SERVICES
# Create a Service to expose the API
resource "kubernetes_service" "api" {
  metadata {
    name = "api-service"
    labels = {
      run = "api"
    }
  }

  spec {
    selector = {
      app = kubernetes_deployment.api.spec.0.template[0].metadata.0.labels.app
    }

    type = "NodePort"

    port {
      port        = 8000
      target_port = 8000
      protocol    = "TCP"
    }
  }
}

# Create a Service to expose the RabbitMQ
resource "kubernetes_service" "rabbitmq" {
  metadata {
    name = "rabbitmq-service"
    labels = {
      run = "rabbitmq-deployment"
    }
  }

  spec {
    selector = {
      app = kubernetes_deployment.rabbitmq.spec.0.template[0].metadata.0.labels.app
    }

    port {
      port        = 5672
      target_port = 5672
      protocol    = "TCP"
    }
  }
}

# Create a Service to expose the database
resource "kubernetes_service" "database" {
  metadata {
    name = "database-service"
    labels = {
      app = "database-deployment"
    }
  }

  spec {
    selector = {
      app = kubernetes_deployment.database.spec.0.template[0].metadata.0.labels.app
    }

    port {
      port        = 5432
      target_port = 5432
      protocol    = "TCP"
    }
  }
}