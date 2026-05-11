# 🏠 Home Memory

**Home Memory** is a smart home intelligence dashboard that explains what your house is doing, why automations fired, and what needs attention — built as a companion layer on top of [Home Assistant](https://www.home-assistant.io/).

![Home Memory Dashboard](https://img.shields.io/badge/status-prototype-teal) ![Home Assistant](https://img.shields.io/badge/Home%20Assistant-compatible-blue) ![License](https://img.shields.io/badge/license-MIT-green)

---

## ✨ Features

- **🕒 Home Timeline** — Plain-English feed of every automation, alert, and device event. Tap any event to see *why* it happened.
- **🔔 Attention Center** — Critical alerts: low batteries, offline devices, unusual temperatures, available updates.
- **🏘️ Room Snapshot** — At-a-glance view of every room: temperature, occupancy, active devices.
- **⚡ Routine Coach** — Detects your behavioral patterns and suggests new automations with confidence scores.
- **📊 KPI Strip** — Daily stats: automations fired, average indoor temp, doors opened, energy saved.
- **🌙 Dark / Light mode** — System preference + manual toggle.
- **📱 Mobile responsive** — Works on phones and tablets.

---

## 🚀 Getting Started

### Option 1: Open Directly

Just open `index.html` in your browser. No build step or server needed.

### Option 2: Serve Locally

```bash
# Python
python3 -m http.server 8080

# Node
npx serve .
```

Then open `http://localhost:8080`.

---

## 🔌 Connecting to Home Assistant

1. Open the app and click **Connect HA** (sidebar) or the ⚙️ settings icon.
2. Enter your Home Assistant URL (e.g. `http://homeassistant.local:8123`).
3. Paste a **Long-Lived Access Token** from your HA profile page.

> **Note:** The current version is a UI prototype with demo data. Full HA WebSocket API integration is planned for v0.2.

---

## 🗺️ Roadmap

| Version | Feature |
|---------|----------|
| v0.1 | ✅ UI prototype with demo data |
| v0.2 | 🔄 Live HA WebSocket API connection |
| v0.3 | 🔄 Real timeline from logbook + automations |
| v0.4 | 🔄 Routine Coach ML pattern detection |
| v0.5 | 🔄 Custom Home Assistant panel / add-on |

---

## 🛠️ Tech Stack

- Vanilla HTML / CSS / JavaScript (no framework)
- [Lucide Icons](https://lucide.dev/)
- [Google Fonts](https://fonts.google.com/) — Inter + Instrument Serif
- Designed to integrate with the [Home Assistant REST & WebSocket APIs](https://developers.home-assistant.io/docs/api/rest/)

---

## 📁 Project Structure

```
home-memory/
├── index.html       # Main app (self-contained)
└── README.md        # This file
```

---

## 📄 License

MIT — free to use, modify, and integrate with your Home Assistant setup.

---

## 💬 Contributing

Ideas, issues, and PRs welcome! This project is built for the Home Assistant community.

Open an issue to discuss features or share your HA setup.
