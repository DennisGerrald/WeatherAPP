# 🌦️ Weather App (Django) — Live & Simulation Mode

A modern, responsive weather web application built with **Django** that provides real-time weather data using the OpenWeatherMap API and automatically falls back to a smart **Simulation Mode** when no API key is provided or when the API request fails.

This project features a **premium glassmorphic UI**, intelligent fallback system, and full weather search history tracking.

---

## 🚀 Live Demo Features

- 🌍 Search weather by any city in the world
- ☀️ Real-time weather data (OpenWeatherMap API)
- 🧠 Intelligent simulation mode (no API key required)
- 📊 Weather history tracking (SQLite database)
- 🎨 Modern glassmorphic UI with animations
- ⚡ Quick city selection shortcuts
- 🧾 Clickable recent search history
- 📱 Fully responsive design (mobile, tablet, desktop)

---

## 🧠 Smart System Design

### 🔁 Dual Weather Engine

The app automatically switches between:

#### 1. 🌐 Live API Mode
- Uses OpenWeatherMap API
- Displays real-time weather data
- Saves exact fetched values into database
- Shows badge: **Live Data**

#### 2. 🧪 Simulation Mode
Activated when:
- API key is missing
- API key is invalid
- API request fails (401/timeout/no internet)

Features:
- Generates realistic weather data
- Based on:
  - City name hash
  - Local time of day
- Always functional (no setup required)
- Shows badge: **Simulated Data**

---

## ✨ Key Features

### 🌦️ Weather Data
- Temperature (°C)
- Humidity (%)
- Atmospheric pressure (hPa)
- Wind speed (m/s)
- Weather description
- Weather icon
- Country information

### 📊 History Tracking
- Stores all searched cities
- Saves weather snapshots
- Displays recent searches as clickable chips
- Chronological ordering

---

## 🎨 UI / UX Design

### 💎 Glassmorphism Dashboard
- Frosted glass container effects
- Smooth blur and transparency layers
- Soft shadows and glowing accents

### 🌈 Dynamic Backgrounds
UI changes based on weather:
- ☀️ Sunny → Warm gradient
- 🌧️ Rainy → Cool blue tones
- 🌫️ Fog/Mist → Soft grey overlay
- ❄️ Snow → Cold white-blue palette

### ⚡ Interactive Elements
- Hover animations
- Fade-in weather cards
- Smooth transitions
- Floating weather icons
- Responsive grid layout

---

## ⚙️ Tech Stack

### Backend
- Django (Python)
- SQLite database
- dotenv for environment variables

### Frontend
- HTML5
- CSS3 (Glassmorphism + animations)
- JavaScript (interactive UI)
- Google Fonts (Outfit / Inter)

### API
- OpenWeatherMap API

---
