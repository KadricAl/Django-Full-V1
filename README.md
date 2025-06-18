# POS Monitoring System

A full-stack Django application for monitoring service and installation requests for POS devices.

## 🚀 Features

- Role-based login (Client & Technician)
- Track devices, shops, and services
- Client device service requests
- Technicians track yearly maintenance
- PDF generation using WeasyPrint
- Email integration
- Clean Tailwind-based UI

## 🛠 Tech Stack

- **Backend:** Python, Django
- **Frontend:** HTML, Tailwind CSS
- **Database:** MySQL / SQLite
- **PDF:** WeasyPrint
- **Others:** Django Auth, File Upload, Email, .env support

## Project

- home/ # Home pages and login logic
- contact/ # Contact page logic and view
- customer/ # Customer-facing logic and dashboard
- technician/ # Technician dashboard
- devices/ # Devices/Products models and views
- installed_devices/ # Installed_devices models and views
- service/ # Service model logic
- templates/
- static/
- media/
- requirements.txt
- README.md

## 🗂 Setup

1. Create `.env` 
2. Install dependencies:


pip install -r requirements.txt
