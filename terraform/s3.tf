resource "aws_s3_bucket" "website_bucket" {
  bucket = "levendredi"
}

resource "aws_s3_object" "website_main_page" {
  bucket = aws_s3_bucket.website_bucket.id
  key = "main.html"
  source = "../web-src/main.html"
}
