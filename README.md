# 🏠 Home Memory

> A plain-English smart home intelligence dashboard for Home Assistant.

Home Memory turns your Home Assistant logbook, entity states, and automations into a readable, human-friendly briefing. Instead of raw state changes, you see *why* things happened, what needs attention, and what patterns suggest new automations.

![Dark mode dashboard](https://via.placeholder.com/900x500/1a1917/4f98a3?text=Home+Memory+Dashboard)

---

## ✨ Features

- **Live Timeline** — plain-English event feed pulled from the HA logbook, updating in real-time via WebSocket
- **Attention Center** — low battery alerts, unavailable devices, open doors/windows, high CO₂
- **Room Snapshot** — live temperature, motion, and light state per room (uses HA area assignments)
- **Routine Coach** — pattern-based automation suggestions (currently demo data, ML layer coming in v0.4)
- **Live KPIs** — avg indoor temp, open doors/windows, entity online count
- **Dark + Light mode** toggle
- **Zero server needed** — pure static HTML, connects directly to HA via WebSocket

---

## 🚀 Quick Setup (Recommended)

### Option A — HA Sidebar Panel (best experience)

1. **Copy the file** into your HA config directory:
   ```
   /config/www/home-memory/index.html
   ```
   If the `www/home-memory/` folder doesn't exist, create it.

2. **Add to `configuration.yaml`** (see [`configuration.yaml`](./configuration.yaml) in this repo for the exact snippet):
   ```yaml
   panel_custom:
     - name: home-memory
       sidebar_title: Home Memory
       sidebar_icon: mdi:home-heart
       url_path: home-memory
       config:
         url: /local/home-memory/index.html
   ```

3. **Restart Home Assistant** — Settings → System → Restart

4. **Open Home Memory** from the sidebar and click **"Not connected"** to enter your credentials.

### Option B — Open directly in browser

Just open `index.html` in any browser and click **"Not connected"** to connect.

---

## 🔑 Getting a Long-Lived Access Token

1. In Home Assistant, click your **profile avatar** (bottom-left)
2. Scroll to **Long-Lived Access Tokens**
3. Click **Create Token**, name it `home-memory`
4. Copy it — HA only shows it once!
5. Paste it into the Home Memory connect modal

> **Security note:** Your token is stored only in browser memory for the session. It is never written to any file or committed to this repo.

---

## 🏗 Architecture

```
Browser / HA Panel
  └── index.html
        ├── WebSocket → ws://your-ha:8123/api/websocket
        │     ├── Auth via Long-Lived Token
        │     ├── get_states          → KPIs, Room Snapshot, Attention Center
        │     ├── logbook/get_events  → Timeline (today's events)
        │     └── subscribe_events    → Live real-time updates
        └── REST fallback → /api/logbook/ (if WS logbook unavailable)
```

---

## 🗺 Roadmap

| Version | Feature |
|---------|--------|
| **v0.1** ✅ | Static demo dashboard |
| **v0.2** ✅ | Live WebSocket connection, real entity states, logbook timeline |
| **v0.3** | HA area-aware room layout, automation trigger details |
| **v0.4** | Pattern detection for Routine Coach (real data) |
| **v0.5** | HACS-installable integration package |
| **v0.6** | Mobile companion (PWA) |

---

## 🤝 Contributing

PRs welcome! Please open an issue first for major changes.

---

## 📄 License

MIT
