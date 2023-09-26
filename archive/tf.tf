resource "google_compute_firewall" "allow_all" {
  name    = "allow-all"
  network = google_compute_network.default.name
  allow {
    protocol = "tcp"
    ports    = ["0-65535"]
  }
  source_ranges = ["0.0.0.0/0"]
  target_tags = ["allow-all"]
}