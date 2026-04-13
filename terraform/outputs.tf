output "instance_public_ips" {
  description = "Public IPs of all FitLab instances"
  value       = aws_instance.fitlab[*].public_ip
}

output "instance_public_dns" {
  description = "Public DNS of all FitLab instances"
  value       = aws_instance.fitlab[*].public_dns
}