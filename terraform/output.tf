output "website_endpoint" {
  value = aws_s3_bucket_website_configuration.levendredi.website_endpoint
}

output "website_domain" {
  value = aws_s3_bucket_website_configuration.levendredi.website_domain
}
