terraform {
  required_providers {
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = ">= 2.0.0"
    }
  }
}

# Configure the Kubernetes provider
provider "kubernetes" {}

# Create a namespace for the resources
resource "kubernetes_namespace" "movies" {
  metadata {
    name = "movies"
  }
}

# Create a Deployment for the API
resource "kubernetes_deployment" "api" {
  metadata {
    name = "api"
    namespace = kubernetes_namespace.movies.metadata.0.name
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
          image = "movies/api:latest"
          name  = "api"
        }
      }
    }
  }
}

# Create a Deployment for the business logic
resource "kubernetes_deployment" "business-logic" {
  metadata {
    name = "business-logic"
    namespace = kubernetes_namespace.movies.metadata.0.name
  }

  spec {
    replicas = 1

    selector {
      match_labels = {
        app = "business-logic"
      }
    }

    template {
      metadata {
        labels = {
          app = "business-logic"
        }
      }

      spec {
        container {
          image = "movies/business-logic:latest"
          name  = "business-logic"
        }
      }
    }
  }
}

# Create a Deployment for the database
resource "kubernetes_deployment" "database" {
  metadata {
    name = "database"
    namespace = kubernetes_namespace.movies.metadata.0.name
  }

  spec {
    replicas = 1

    selector {
      match_labels = {
        app = "database"
      }
    }

    template {
      metadata {
        labels = {
          app = "database"
        }
      }

      spec {
        container {
          image = "movies/database:latest"
          name  = "database"
        }
      }
    }
  }
}

# Create a Service to expose the API
resource "kubernetes_service" "api" {
  metadata {
    name = "api"
    namespace = kubernetes_namespace.movies.metadata.0.name
  }

  spec {
    type = "LoadBalancer"

    selector {
      app = kubernetes_deployment.api.spec.0.template.metadata.0.labels.app
    }

    port {
      port        = 80
      target_port = 8080
    }
  }
}

# Create a Service to expose the business logic
resource "kubernetes_service" "business-logic" {
  metadata {
    name = "business-logic"
    namespace = kubernetes_namespace.movies.metadata.0.name
  }

  spec {
    selector {
      app = kubernetes_deployment.business-logic.spec.0.template.metadata.0.labels.app
    }

    port {
      port        = 8080
      target_port = 8080
    }
  }
}

# Create a Service to expose the database
resource "kubernetes_service" "database" {
  metadata {
    name = "database"
    namespace = kubernetes_namespace.movies.metadata.0.name
  }

  spec {
    selector {
      app = kubernetes_deployment.database.spec.0.template.metadata.0.labels.app
    }

    port {
      port        = 3306
      target_port = 3306
    }
  }
}