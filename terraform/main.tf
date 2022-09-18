module "function" {
  source = "./modules/function"
  project = var.project
  name = "my-function"
  entry = "cloud_function"
}