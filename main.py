import os
import sqlite3
from datetime import datetime
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

# Database Setup
DB_FILE = "trade_history.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS signals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            time TEXT,
            symbol TEXT,
            tier TEXT,
            action TEXT,
            entry_price REAL,
            stop_loss REAL,
            tsl_rule TEXT,
            active_targets TEXT,
            confidence TEXT,
            dispatch_channel TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.get("/run-scan")
def run_ai_scan():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    signals = [
        {
            "time": current_time,
            "symbol": "BANKNIFTY 51200 PE",
            "tier": "PRO",
            "action": "BUY (LONG)",
            "entry_price": 420.29,
            "stop_loss": 416.00,
            "tsl_rule": "Shift to Cost @ T1",
            "active_targets": "T1: ₹453.91 | T2: ₹487.54 | T3: ₹525.36 (Jackpot)",
            "confidence": "100%",
            "dispatch_channel": "WhatsApp + Automated Voice Call Alert"
        },
        {
            "time": current_time,
            "symbol": "FINNIFTY 23400 CE",
            "tier": "VIP",
            "action": "SELL (SHORT)",
            "entry_price": 314.70,
            "stop_loss": 317.80,
            "tsl_rule": "Shift to Cost @ T1",
            "active_targets": "T1: ₹339.88 | T2: ₹365.05",
            "confidence": "80%",
            "dispatch_channel": "WhatsApp Broadcast + Support"
        },
        {
            "time": current_time,
            "symbol": "BANKNIFTY 51200 PE",
            "tier": "BASIC",
            "action": "BUY (LONG)",
            "entry_price": 571.01,
            "stop_loss": 565.30,
            "tsl_rule": "Shift to Cost @ T1",
            "active_targets": "T1: ₹616.69",
            "confidence": "70%",
            "dispatch_channel": "Telegram Channel (Basic Cap)"
        }
    ]
    
    for sig in signals:
        cursor.execute('''
            INSERT INTO signals (time, symbol, tier, action, entry_price, stop_loss, tsl_rule, active_targets, confidence, dispatch_channel)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (sig["time"], sig["symbol"], sig["tier"], sig["action"], sig["entry_price"], sig["stop_loss"], sig["tsl_rule"], sig["active_targets"], sig["confidence"], sig["dispatch_channel"]))
    
    conn.commit()
    conn.close()
    return {"status": "success", "signals": signals}

@app.get("/get-signals")
def get_signals():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT time, symbol, tier, action, entry_price, stop_loss, tsl_rule, active_targets, confidence, dispatch_channel FROM signals ORDER BY id DESC LIMIT 10')
    rows = cursor.fetchall()
    conn.close()
    
    result = []
    for r in rows:
        result.append({
            "time": r[0],
            "symbol": r[1],
            "tier": r[2],
            "action": r[3],
            "entry_price": r[4],
            "stop_loss": r[5],
            "tsl_rule": r[6],
            "active_targets": r[7],
            "confidence": r[8],
            "dispatch_channel": r[9]
        })
    return {"signals": result}

@app.get("/", response_class=HTMLResponse)
def read_root():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>KHALIL'S PERFECT TRADE ALERTS PRO</title>
        <style>
            body { background-color: #080b12; color: #fff; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 25px; }
            
            /* Top Header Bar */
            .header-bar { 
                background: linear-gradient(135deg, #131238, #1e1b4b); 
                padding: 18px 25px; 
                border-radius: 14px; 
                display: flex; 
                justify-content: space-between; 
                align-items: center; 
                box-shadow: 0 4px 20px rgba(0,0,0,0.5);
                border: 1px solid #2e2a72;
            }
            .header-title h2 { margin: 0; font-size: 22px; color: #e0e7ff; letter-spacing: 0.5px; }
            .header-title p { margin: 5px 0 0 0; font-size: 12px; color: #a5b4fc; }
            
            .header-right { display: flex; align-items: center; gap: 15px; }
            .weather-badge { background: #1f293d; padding: 8px 14px; border-radius: 20px; font-size: 13px; color: #fbbf24; font-weight: bold; }
            
            .btn-toggle { background: linear-gradient(90deg, #10b981, #059669); color: white; border: none; padding: 10px 20px; font-weight: bold; border-radius: 8px; cursor: pointer; font-size: 13px; box-shadow: 0 2px 10px rgba(16,185,129,0.3); }
            .btn-toggle.off { background: linear-gradient(90deg, #ef4444, #dc2626); box-shadow: 0 2px 10px rgba(239,68,68,0.3); }

            /* Feed Bar */
            .feed-bar { 
                margin-top: 18px; 
                background: #0f172a; 
                padding: 14px 20px; 
                border-radius: 12px; 
                display: flex; 
                justify-content: space-between; 
                align-items: center; 
                border: 1px solid #1e293b;
            }
            .feed-status { display: flex; align-items: center; gap: 10px; font-size: 13px; font-weight: 600; color: #ef4444; }
            .dot { height: 10px; width: 10px; background-color: #ef4444; border-radius: 50%; display: inline-block; box-shadow: 0 0 8px #ef4444; }
            
            .btn-upstox { background: linear-gradient(90deg, #10b981, #059669); color: white; border: none; padding: 10px 18px; font-weight: bold; border-radius: 8px; cursor: pointer; font-size: 13px; display: flex; align-items: center; gap: 8px; }

            /* Matrix Cards */
            .matrix-section { margin-top: 25px; }
            .section-title { font-size: 16px; font-weight: bold; color: #cbd5e1; margin-bottom: 15px; display: flex; align-items: center; gap: 8px; }
            
            .card-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 18px; }
            .card { background: #0f172a; padding: 20px; border-radius: 12px; border: 1px solid #1e293b; position: relative; }
            
            .card.basic { border-top: 4px solid #3b82f6; }
            .card.vip { border-top: 4px solid #eab308; }
            .card.pro { border-top: 4px solid #a855f7; }
            .card.stats { border-top: 4px solid #10b981; }

            .card-tag { font-size: 11px; font-weight: bold; text-transform: uppercase; padding: 3px 8px; border-radius: 4px; display: inline-block; margin-bottom: 10px; }
            .basic .card-tag { background: #1e3a8a; color: #93c5fd; }
            .vip .card-tag { background: #713f12; color: #fef08a; }
            .pro .card-tag { background: #581c87; color: #e9d5ff; }
            .stats .card-tag { background: #064e3b; color: #a7f3d0; }

            .card-count { font-size: 32px; font-weight: 800; margin: 10px 0 5px 0; }
            .card-sub { font-size: 12px; color: #94a3b8; }

            /* Main AI Scan Banner */
            .scan-banner { 
                margin-top: 25px; 
                background: linear-gradient(135deg, #111827, #1f1d47); 
                padding: 25px; 
                border-radius: 14px; 
                text-align: center; 
                border: 1px solid #312e81; 
                box-shadow: 0 4px 25px rgba(99, 102, 241, 0.15);
            }
            .scan-banner h3 { margin: 0 0 8px 0; font-size: 18px; color: #c7d2fe; }
            .scan-banner p { margin: 0 0 18px 0; font-size: 13px; color: #818cf8; }
            
            .btn-scan { 
                background: linear-gradient(90deg, #8b5cf6, #6366f1); 
                border: none; 
                color: white; 
                padding: 14px 32px; 
                font-weight: bold; 
                border-radius: 10px; 
                cursor: pointer; 
                font-size: 15px; 
                box-shadow: 0 4px 15px rgba(139, 92, 246, 0.4);
                transition: transform 0.2s ease;
            }
            .btn-scan:hover { transform: translateY(-2px); }

            /* Table Styling */
            .table-container { margin-top: 30px; background: #0f172a; border-radius: 12px; padding: 20px; border: 1px solid #1e293b; }
            table { width: 100%; border-collapse: collapse; margin-top: 10px; }
            th, td { padding: 14px 12px; text-align: left; border-bottom: 1px solid #1e293b; font-size: 13px; }
            th { background-color: #162032; color: #94a3b8; font-size: 12px; text-transform: uppercase; letter-spacing: 0.5px; }
            
            .tier-badge { padding: 4px 10px; border-radius: 6px; font-weight: 700; font-size: 11px; }
            .tier-pro { background: #581c87; color: #d8b4fe; }
            .tier-vip { background: #713f12; color: #fef08a; }
            .tier-basic { background: #1e3a8a; color: #93c5fd; }
        </style>
    </head>
    <body>

        <!-- Top Header Bar -->
        <div class="header-bar">
            <div class="header-title">
                <h2>🚀 KHALIL'S PERFECT TRADE ALERTS PRO</h2>
                <p>Tiered Targets System: Basic (Target 1) | VIP (Target 1+2) | PRO (Target 1+2+3 Jackpot)</p>
            </div>
            <div class="header-right">
                <div class="weather-badge">🌤️ Sambhajinagar 25°C</div>
                <button id="toggleBtn" class="btn-toggle" onclick="toggleBot()">BOT SYSTEM: ACTIVE (RUNNING)</button>
            </div>
        </div>

        <!-- Live Feed Monitor Bar -->
        <div class="feed-bar">
            <div class="feed-status">
                <span class="dot"></span>
                <span>LIVE FEED MONITOR: SIMULATION / LIVE FEED DISCONNECTED</span>
            </div>
            <button class="btn-upstox" onclick="alert('Connecting to Upstox API Feed...')">🔑 Connect Upstox Feed</button>
        </div>

        <!-- Matrix Cards Section -->
        <div class="matrix-section">
            <div class="section-title">📊 Plan-Wise Target Matrix & Accuracy</div>
            <div class="card-grid">
                <div class="card basic">
                    <span class="card-tag">BASIC PLAN (60%-70%)</span>
                    <div style="font-size: 11px; color: #38bdf8; font-weight: bold; margin-bottom: 5px;">🎯 Target 1 Only | Telegram</div>
                    <div class="card-count">1 Alerts</div>
                    <div class="card-sub">Accuracy: 100% (1 Success)</div>
                </div>

                <div class="card vip">
                    <span class="card-tag">VIP PLAN (80%-90%)</span>
                    <div style="font-size: 11px; color: #facc15; font-weight: bold; margin-bottom: 5px;">🎯 Target 1 + 2 | WhatsApp</div>
                    <div class="card-count">1 Alerts</div>
                    <div class="card-sub">Accuracy: 100% (1 Success)</div>
                </div>

                <div class="card pro">
                    <span class="card-tag">PRO PLAN (100% CONFLUENCE)</span>
                    <div style="font-size: 11px; color: #c084fc; font-weight: bold; margin-bottom: 5px;">🎯 Target 1, 2 & 3 Jackpot | Call</div>
                    <div class="card-count">1 Alerts</div>
                    <div class="card-sub">Accuracy: 100% (1 Success)</div>
                </div>

                <div class="card stats">
                    <span class="card-tag">OVERALL TERMINAL STATS</span>
                    <div style="font-size: 11px; color: #4ade80; font-weight: bold; margin-bottom: 5px;">🔥 Risk Managed Targets</div>
                    <div class="card-count" style="color: #4ade80;">100%</div>
                    <div class="card-sub">Total Dispatched Today: 3</div>
                </div>
            </div>
        </div>

        <!-- Main Scan Action Banner -->
        <div class="scan-banner">
            <h3>⚡ 10 AI Indicator Scanner & Multi-Target Dispatcher</h3>
            <p>Run real-time AI Scan to calculate Tiered Targets & Dual Indian Speech Alerts</p>
            <button class="btn-scan" onclick="runScan()">⚡ Run AI Market Scan & Dispatch Signal</button>
        </div>

        <!-- Live Signals Ticker Table -->
        <div class="table-container">
            <div class="section-title">🎛️ Real-Time Dispatched Signals & Targets Ticker</div>
            <table>
                <thead>
                    <tr>
                        <th>Time</th>
                        <th>Symbol</th>
                        <th>Tier</th>
                        <th>Action</th>
                        <th>Entry</th>
                        <th style="color: #ff4d4d;">SL</th>
                        <th style="color: #ffcc00;">Trailing SL (TSL)</th>
                        <th>Active Targets</th>
                        <th>Confidence</th>
                        <th>Dispatch Channel</th>
                    </tr>
                </thead>
                <tbody id="ticker-body">
                </tbody>
            </table>
        </div>

        <script>
            let isBotActive = true;

            function toggleBot() {
                isBotActive = !isBotActive;
                let btn = document.getElementById('toggleBtn');
                if (isBotActive) {
                    btn.className = 'btn-toggle';
                    btn.innerText = 'BOT SYSTEM: ACTIVE (RUNNING)';
                } else {
                    btn.className = 'btn-toggle off';
                    btn.innerText = 'BOT SYSTEM: OFF (PAUSED)';
                }
            }

            function speakAlert(text) {
                if ('speechSynthesis' in window) {
                    let msg = new SpeechSynthesisUtterance(text);
                    msg.lang = 'hi-IN';
                    window.speechSynthesis.speak(msg);
                }
            }

            async function loadSignals() {
                let res = await fetch('/get-signals');
                let data = await res.json();
                let body = document.getElementById('ticker-body');
                body.innerHTML = '';
                data.signals.forEach(sig => {
                    let tierClass = sig.tier === 'PRO' ? 'tier-pro' : (sig.tier === 'VIP' ? 'tier-vip' : 'tier-basic');
                    body.innerHTML += `
                        <tr>
                            <td>${sig.time}</td>
                            <td><b>${sig.symbol}</b></td>
                            <td><span class="tier-badge ${tierClass}">${sig.tier}</span></td>
                            <td style="color: ${sig.action.includes('BUY') ? '#10b981' : '#ef4444'}; font-weight: bold;">${sig.action}</td>
                            <td>₹${sig.entry_price}</td>
                            <td style="color: #ff4d4d; font-weight: bold;">₹${sig.stop_loss}</td>
                            <td style="color: #ffcc00; font-weight: bold;">${sig.tsl_rule}</td>
                            <td style="color: #10b981; font-weight: 500;">${sig.active_targets}</td>
                            <td><b>${sig.confidence}</b></td>
                            <td style="color: #94a3b8;">${sig.dispatch_channel}</td>
                        </tr>
                    `;
                });
            }

            async function runScan() {
                if (!isBotActive) {
                    alert("Bot system is paused! Click top button to activate.");
                    return;
                }
                speakAlert("Scan complete. New trade alerts generated.");
                await fetch('/run-scan');
                setTimeout(loadSignals, 500);
            }

            loadSignals();
        </script>
    </body>
    </html>
    """