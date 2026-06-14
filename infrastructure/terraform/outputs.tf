output "public_ip" {
  description = "IP público da EC2"
  value       = aws_instance.sitewatch.public_ip
}

output "public_dns" {
  description = "DNS público da EC2"
  value       = aws_instance.sitewatch.public_dns
}

output "ssh_command" {
  description = "Comando SSH para acessar a instância"
  value       = "ssh -i ~/.ssh/${var.key_name}.pem ubuntu@${aws_instance.sitewatch.public_ip}"
}
