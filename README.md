# F1-2026-Energy-Management-and-Overtake-Mode-Simulation
This project presents a comprehensive and innovative simulation system forF1 2026 energy management and overtake mode mechanics. The system has been developed with meticulous attention to the official 2026 F1 regulation and provide accurate modeling of hybrid power unit dynamics.
# F1 2026 Energy Management & Overtake Mode Simulation

## 📋 Project Overview

A comprehensive web-based simulation system for Formula 1 2026 cars that models energy management, fuel consumption, tire degradation, and strategic overtake mechanics. Built with Python Flask backend and interactive JavaScript frontend, this simulator enables users to understand complex energy dynamics in modern hybrid racing vehicles.

**Features:**
- Realistic physics-based simulation of 2026 F1 regulations
- Real-time interactive dashboard with 8 metric cards
- 4 interactive charts showing energy trends
- Multi-driver competitive racing simulation
- Support for 1-56 lap races
- Automatic pit stop mechanics at strategic laps
- AI-powered energy deployment suggestions

---

## 🎯 Motivation

Formula 1 2026 introduces significant changes to hybrid power unit regulations, emphasizing strategic energy management. This project addresses the lack of accessible simulation tools for understanding these complex system interactions. Instead of expensive physical testing, teams, students, and enthusiasts can now explore energy management strategies digitally.

**Problem it solves:**
- No public F1 2026 energy simulation tools available
- Need for understanding multi-system interactions (battery, fuel, tires)
- Educational gap in motorsports engineering
- Lack of tools for strategy planning and analysis

---

## 🚀 Key Features

### Core Simulation
- **Battery Management System** (14 kWh capacity)
  - Real-time state-of-charge tracking (0-100%)
  - Energy recovery from braking at 65% efficiency
  - Energy deployment for power boost
  - Automatic charge capping at 100%

- **Fuel Consumption Model** (50 kg tank)
  - Baseline consumption: 0.14 kg/km
  - Dynamic modifiers based on tire wear
  - Overtake mode penalty (+30%)
  - Automatic refueling at pit stops (+15 kg)

- **Tire Degradation System**
  - Linear degradation: 1.5% per lap
  - Impact on fuel consumption efficiency
  - Automatic reset at pit stops
  - Capped at 100% maximum wear

- **Overtake Mode** (6 uses per race)
  - +50 kW power boost
  - 20-second activation duration
  - 50 kJ energy cost per use
  - Strategic use tracking

- **Pit Stop Mechanics**
  - Automatic triggers at lap 5 & 12
  - Fuel refill: +15 kg (max 50 kg)
  - Battery recharge: +5% (max 100%)
  - Tire replacement: 0% degradation reset
  - Complete event logging

### User Interface
- **Professional Dashboard**
  - 8 real-time metric cards (4 per driver)
  - Progress bars with percentage displays
  - Color-coded indicators
  - Responsive design (mobile to 4K)

- **Interactive Visualization**
  - Battery trend chart with pit stop markers
  - Fuel consumption graph
  - Tire degradation progression
  - Power output variation tracking
  - Real-time chart updates with animations

- **Race Log**
  - Detailed lap-by-lap event logging
  - Pit stop event highlighting
  - Chronological event display
  - Scrollable history view

- **Multi-Driver Support**
  - Simultaneous simulation of 2+ drivers
  - Comparative performance analysis
  - Individual driver tracking
  - Side-by-side metric comparison

---

## 🛠️ Technology Stack

### Backend
- **Language:** Python 3.10+
- **Framework:** Flask 2.3.0
- **Server:** Werkzeug WSGI
- **Templating:** Jinja2 3.1.2
- **Data Processing:** pandas

### Frontend
- **Markup:** HTML5
- **Styling:** CSS3 (Responsive Grid/Flexbox)
- **Interactivity:** JavaScript ES6+
- **Visualization:** Chart.js 3.9.1 (via CDN)

### Data Storage
- **Format:** CSV (comma-separated values)
- **File:** `productivity_data.csv`
- **Structure:** Date, Driver, Metrics, Race Data

### Development Tools
- **IDE:** Visual Studio Code / PyCharm
- **Version Control:** Git
- **Testing:** Python unittest framework

---

## 📊 System Architecture

### 3-Tier Architecture
