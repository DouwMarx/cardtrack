variable "hcloud_token" {
  description = "Hetzner Cloud API token (project > Security > API tokens, Read & Write)."
  type        = string
  sensitive   = true
}

variable "name" {
  description = "Server name, also used for the SSH key and firewall."
  type        = string
  default     = "cardtrack"
}

variable "server_type" {
  description = "Hetzner server type. cx23 = 2 vCPU x86, 4 GB RAM, 40 GB disk. x86 so a laptop can build and copy."
  type        = string
  default     = "cx23"
}

variable "location" {
  description = "Hetzner location: nbg1, fsn1 (Germany) or hel1 (Finland)."
  type        = string
  default     = "nbg1"
}

variable "ssh_public_key" {
  description = "Public key for root and the app user (contents of ~/.ssh/id_ed25519.pub)."
  type        = string
}

variable "repo_url" {
  description = "Git URL the host clones and pulls (its default branch must contain infra/). Use your fork's HTTPS URL."
  type        = string
  default     = "https://github.com/DouwMarx/cardtrack.git"
}

variable "tailscale_auth_key" {
  description = <<-EOT
    Optional; most deployments leave it empty and use key-only SSH.
    A ONE-OFF, pre-authorized, tagged (tag:cardtrack) Tailscale auth key
    that expires within hours. If set, the host joins your tailnet and the firewall
    allows no inbound traffic at all. It ends up in Terraform state and Hetzner's
    server metadata, which is why it must be single-use and short-lived.
  EOT
  type        = string
  default     = ""
  sensitive   = true
}

variable "admin_cidrs" {
  description = "Without Tailscale: source ranges allowed to SSH in. Default: anywhere (SSH is key-only, see bootstrap.sh)."
  type        = list(string)
  default     = ["0.0.0.0/0", "::/0"]
}
