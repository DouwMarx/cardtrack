terraform {
  # Works with Terraform >= 1.6 and OpenTofu >= 1.6 (same language, same providers).
  required_version = ">= 1.6"
  required_providers {
    hcloud = {
      source  = "hetznercloud/hcloud"
      version = "~> 1.52"
    }
  }
}

provider "hcloud" {
  token = var.hcloud_token
}
