locals {
  # only whether a key is set is exposed, never the key itself
  use_tailscale = nonsensitive(var.tailscale_auth_key != "")
}

resource "hcloud_ssh_key" "admin" {
  name       = "${var.name}-admin"
  public_key = var.ssh_public_key
}

# The pipeline only makes outbound connections, so SSH is the only inbound port:
# key-only, from admin_cidrs (default anywhere). With Tailscale, not even that.
resource "hcloud_firewall" "host" {
  name = var.name

  dynamic "rule" {
    for_each = local.use_tailscale || length(var.admin_cidrs) == 0 ? [] : [1]
    content {
      direction  = "in"
      protocol   = "tcp"
      port       = "22"
      source_ips = var.admin_cidrs
    }
  }
}

resource "hcloud_server" "host" {
  name         = var.name
  server_type  = var.server_type
  location     = var.location
  image        = "debian-13"
  ssh_keys     = [hcloud_ssh_key.admin.id]
  firewall_ids = [hcloud_firewall.host.id]

  # IPv4 stays on: github.com has no IPv6 address, so an IPv6-only host cannot push.
  public_net {
    ipv4_enabled = true
    ipv6_enabled = true
  }

  user_data = templatefile("${path.module}/cloud-init.yaml.tftpl", {
    name               = var.name
    repo_url           = var.repo_url
    ssh_public_key     = var.ssh_public_key
    tailscale_auth_key = var.tailscale_auth_key
  })

  lifecycle {
    # user_data only runs on first boot; editing it must not replace a live host.
    ignore_changes = [user_data]
  }
}
