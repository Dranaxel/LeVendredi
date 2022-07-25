resource "aws_s3_bucket" "website_bucket" {
  bucket = "levendredi"
}

resource "aws_s3_bucket_acl" "website_bucket_acl" {
  bucket = aws_s3_bucket.website_bucket.id
  acl    = "public-read"
}

resource "aws_s3_object" "website_main_page" {
  bucket       = aws_s3_bucket.website_bucket.id
  key          = "index.html"
  source       = "../web-src/main.html"
  content_type = "text/html"
acl = "public-read"
}
