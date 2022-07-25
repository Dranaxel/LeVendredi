resource "aws_s3_bucket_website_configuration" "levendredi" {
  bucket = aws_s3_bucket.website_bucket.bucket
  index_document {
    suffix = "index.html"
  }
}
