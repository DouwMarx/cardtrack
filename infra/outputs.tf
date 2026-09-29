output "ipv4" {
  value = hcloud_server.host.ipv4_address
}

output "next_steps" {
  value = <<-EOT
    Wait ~10 min for first boot (cloud-init installs TeX), then:
      infra/push-secrets.sh ${local.use_tailscale ? var.name : hcloud_server.host.ipv4_address}
      infra/migrate-data.sh ${local.use_tailscale ? var.name : hcloud_server.host.ipv4_address}
  EOT
}
