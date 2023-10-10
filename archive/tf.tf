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


resource "google_compute_firewall" "allow_ssh" {
  name    = "allow-ssh"
  network = google_compute_network.default.name
  allow {
    protocol = "tcp"
    ports    = ["22"]
  }
  source_ranges = ["77.125.87.177/32"]
  target_tags = ["allow-ssh"]
}