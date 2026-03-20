# VoidPay — Parametric Income Insurance for Gig Delivery Workers

> **DEVTrails 2026 Hackathon Submission**
> Track: FinTech / InsurTech / AI for Social Good

---

## Project Overview

**VoidPay** is a simple, AI-assisted parametric insurance platform built for gig delivery workers in India. It protects riders from **income loss** caused by things they can't control — bad weather, severe pollution (AQI), or local disruptions like curfews.

The core idea is straightforward: instead of filing a claim, the system watches live weather and AQI data. When a threshold is crossed (like AQI > 350 or rainfall > 80mm), the rider automatically gets compensated. So the rider doesn’t have to do anything manually..

This is a **Phase 1 prototype** — focused on proving the concept works with a working demo and clear logic.

> Note: VoidPay only covers income loss due to external disruptions and does not include health, accident, or vehicle-related insurance.

---

## Problem Statement

India has over **11 million gig delivery workers** with no income protection when external conditions stop them from working.

| Challenge | Impact |
|---|---|
| Heavy rainfall or flooding | Riders can't move; orders drop by 60–80% |
| Severe AQI / smog | Health advisories keep riders off the road |
| Civic curfews or protests | Entire zones become unoperational |
| No formal employer | No sick leave, no backup, no insurance |
| Traditional insurance | Too complex, too slow, too expensive |

These workers are independent contractors. When disruptions hit, they absorb 100% of the loss — alone.

---

## Persona & Scenario

### Persona: Arjun, 26 — Food Delivery Rider, Delhi

- **Location:** Laxmi Nagar, East Delhi
- **Works on:** Zomato (self-declared)
- **Earnings:** ₹600–₹900/day (roughly 18–22 deliveries)
- **Weekly income target:** ₹4,500–₹5,500
- **Device:** Android smartphone, UPI-enabled

### Scenario

> It's November in Delhi. The AQI hits **412 (Severe)** due to stubble burning and winter smog. Order volumes drop by 70%. Arjun manages only 6 deliveries instead of his usual 20 — earning ₹180 instead of ₹750.

**Without VoidPay:** Arjun absorbs the full loss. No options.

**With VoidPay:**
1. The system detects AQI > 350 in Arjun's area using a live API.
2. The parametric trigger fires automatically.
3. Arjun gets a simulated payout of ₹375 (50% of his daily average) — no claim needed.

---

## Application Workflow

```
┌──────────────────────────────────────────────────────────┐
│                     VoidPay PLATFORM                     │
│                                                          │
│  1. SIGN UP                                              │
│     Rider enters: name, city, pin code, daily income     │
│     (self-declared — no external API needed)             │
│     System assigns a risk level → suggests a plan        │
│                                                          │
│  2. SUBSCRIBE                                            │
│     Rider picks a weekly plan → payment simulated        │
│     Coverage active from that point                      │
│                                                          │
│  3. MONITORING                                           │
│     Backend polls Weather + AQI APIs every 15 minutes    │
│     Checks if thresholds are crossed in rider's zone     │
│                                                          │
│  4. TRIGGER CHECK                                        │
│     Threshold crossed for 45+ min? → Basic checks run    │
│     Is rider subscribed and in the affected zone?        │
│                                                          │
│  5. PAYOUT                                               │
│     Payout calculated and shown to rider (simulated)     │
│     Notification sent → Claim logged in database         │
└──────────────────────────────────────────────────────────┘
```

---

## Weekly Premium Model

VoidPay runs on a **weekly subscription** because gig workers think in weekly earning cycles — not monthly ones. It's easy to opt in, and easy to pause.

### Plan Tiers

| Plan | Weekly Premium | Weekly Payout Cap | Best For |
|---|---|---|---|
| **Basic** | ₹49 | ₹500 | Occasional riders |
| **Standard** | ₹89 | ₹1,200 | Regular riders |
| **Pro** | ₹149 | ₹2,500 | Full-time riders |

### How Premiums Are Set

At signup, riders answer a few questions (city, zone, daily income, how often they ride). A simple rule-based scoring system places them into a risk category — Low, Medium, or High — which maps to a suggested plan.

In the prototype, premiums are **static per plan**. Dynamic adjustment is a future improvement.

### Payout Calculation

```
Daily Payout = Self-declared Daily Income × Severity Multiplier

Severity Multipliers:
  - Partial disruption  (e.g., AQI 300–350): 30% of daily income
  - Moderate disruption (e.g., AQI 350–400): 50% of daily income
  - Severe disruption   (e.g., AQI > 400):   75% of daily income

Total payout is capped at the plan's weekly limit.
```

---

## Parametric Triggers

The whole system revolves around **objective data thresholds** — no human decides if a payout happens. The data decides.

### Trigger Table

| Disruption Type | Data Source | Trigger Threshold | Payout Level |
|---|---|---|---|
| Heavy Rainfall | OpenWeatherMap API | > 80mm in 3 hours | Moderate–Severe |
| Severe AQI | AQI India / CPCB API | AQI Index > 350 | Moderate–Severe |
| Storm / Cyclone Warning | OpenWeatherMap alerts | Orange or Red alert | Severe |
| Extreme Heat | OpenWeatherMap API | Heat index > 47°C | Partial |
| Dense Fog | OpenWeatherMap API | Visibility < 500m | Partial |

> **Note:** Civic curfews are not auto-detected in the prototype. Riders can flag them manually; an admin verifies before triggering a payout.

### How Triggers Work

1. The backend polls APIs every **15 minutes**.
2. A condition must persist for at least **45 minutes** before a payout triggers (avoids false alarms from brief spikes).
3. Triggers are **zone-based** — only riders in the affected pin code area get paid.
4. Every trigger event is saved with a timestamp and the data reading that caused it.

---

## AI / ML Integration

The AI layer in VoidPay is intentionally simple and explainable — appropriate for a student team building a working prototype.

### 1. Risk Scoring (Onboarding)
When a rider signs up, a **rule-based scoring script** (built in Python) assigns a risk level based on:
- City and zone (Delhi in winter = higher risk)
- Self-declared income and work frequency
- Historical disruption frequency for that zone (pulled from past API records)

Output: Low / Medium / High risk → maps to a recommended plan.

### 2. Pricing Suggestion Logic
A simple Python script looks at the **7-day weather and AQI forecast** for the rider's zone and suggests a plan tier for that week. If a bad week is predicted, the system nudges the rider toward a higher plan.

This is rule-based in the prototype (e.g., if 3+ days forecast AQI > 300 → suggest Pro plan).

### 3. Basic Fraud Checks
Before a payout goes through, the system runs a few simple rule checks:
- Has this rider already been paid for the same trigger type this week?
- Does the API data actually confirm the disruption in their pin code?
- Does the payout amount stay within their weekly cap?

These are **if-else checks** — not a complex model — but they handle the obvious abuse cases cleanly for a prototype.

---

## Tech Stack

| Layer | Technology |
|---|---|
| **UI / Prototype** | Figma (wireframes) + React (web demo) |
| **Backend** | Node.js + Express |
| **Database** | SQLite (prototype) |
| **AI / ML** | Python (rule-based scripts) |
| **Weather & AQI** | OpenWeatherMap API, AQI India API |
| **Notifications** | In-app browser / app alerts |
| **Payments** | Simulated (UI-only in prototype) |
| **Hosting** | Render / Railway (free tier for demo) |

No Kafka, no blockchain, no heavy cloud infra — just a clean, working stack that a small team can actually build and demo within a hackathon.

---

## System Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                    RIDER WEB / APP UI                        │
│         (Sign Up · Dashboard · Alerts · Claim History)       │
└───────────────────────────┬──────────────────────────────────┘
                            │ REST API
┌───────────────────────────▼──────────────────────────────────┐
│                  BACKEND (Node.js + Express)                 │
│       Rider Auth · Plan Management · Payout Logic            │
└──────────┬─────────────────────────┬─────────────────────────┘
           │                         │
┌──────────▼──────────┐   ┌──────────▼──────────┐
│  SQLite Database    │   │  Python ML Script   │
│  Riders, Plans,     │   │  Risk Score         │
│  Claims, Events     │   │  Pricing Suggestion │
└─────────────────────┘   └─────────────────────┘

┌──────────────────────────────────────────────────┐
│              Data Monitor (Node.js)              │
│         Polls every 15 min:                      │
│         OpenWeatherMap API · AQI India API       │
└────────────────────────┬─────────────────────────┘
                         │ Threshold crossed?
┌────────────────────────▼─────────────────────────┐
│              Trigger Evaluator                   │
│   Zone match · 45-min rule · Basic fraud checks  │
└────────────────────────┬─────────────────────────┘
                         │ Approved
┌────────────────────────▼─────────────────────────┐
│              Payout Engine                       │
│   Calculate amount · Simulate transfer           │
│   Notify rider · Log claim                       │
└──────────────────────────────────────────────────┘
```

---

## Development Roadmap

This roadmap covers only what's realistic for a hackathon team.

### Phase 1 — Hackathon (Current)
- [x] Defined problem, persona, and parametric triggers
- [x] Designed system architecture
- [x] Created Figma wireframes for rider flow
- [ ] Prototype demo (simulated trigger + payout flow)
- [ ] Basic risk scoring logic (rule-based)

### Phase 2 — Post-Hackathon MVP (2–6 weeks)
- [ ] Complete rider signup and plan subscription flow
- [ ] Live OpenWeatherMap + AQI API integration
- [ ] Real trigger engine (persistent polling + zone match)
- [ ] Basic fraud checks before payout
- [ ] Rider dashboard with claim history
- [ ] Admin panel to monitor triggers and payouts

---

## Prototype Demo Flow

The prototype shows the full rider journey using **mock + live API data**:

```
Step 1: Sign Up
  → Enter name, city (Delhi), pin code, daily income (self-declared)
  → Risk level shown: "Medium Risk — Delhi Zone 3"
  → Suggested plan: Standard (₹89/week)

Step 2: Dashboard
  → Live AQI widget (from API or mocked): AQI = 378, Severe
  → Weather status: Heavy rain forecast
  → Coverage status: ACTIVE

Step 3: Trigger Fires
  → AQI crosses 350 and holds for 45 min
  → Alert: "Disruption detected in your zone — checking eligibility..."

Step 4: Payout
  → "₹375 added to your account (simulated)"
  → Claim logged with timestamp and trigger data

Step 5: Admin View (for judges)
  → Zone map with affected areas highlighted
  → Trigger log showing API readings
  → List of payouts issued for that event
```

---

## Repository Structure

```
VoidPay/
│
├── README.md
│
├── docs/
│   ├── wireframes/          # Figma exports / screenshots
│   └── architecture.png
│
├── backend/
│   ├── routes/              # riders, plans, payouts
│   ├── services/            # trigger logic, payout calc
│   ├── models/              # DB schema (SQLite)
│   ├── monitor/
│   │   ├── weather.js       # OpenWeatherMap polling
│   │   └── aqi.js           # AQI API polling
│   └── index.js
│
├── ml/
│   ├── risk_score.py        # Rule-based risk scoring
│   ├── pricing_logic.py     # Weekly plan suggestion
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── pages/           # Signup, Dashboard, Claims
│   │   └── components/
│   └── package.json
│
└── scripts/
    ├── seed.sql             # Sample rider + zone data
    └── simulate_trigger.js  # Manually fire a test trigger
```

---

## Key Design Decisions

| Decision | Reason |
|---|---|
| **Income loss only** | Keeps scope tight. Health and vehicle claims need entirely different systems. |
| **Weekly pricing** | Matches how gig workers plan their money. No long commitments needed. |
| **Self-declared income** | No need for platform API access. Riders know their own earnings. |
| **Parametric triggers** | Objective data = no disputes, no manual processing, no fraud from self-reporting. |
| **Simple rule-based ML** | Transparent, explainable, and actually buildable in a hackathon. |
| **Simulated payments** | Real UPI integration is out of scope for Phase 1. The logic is built — just not wired to a live gateway. |

---

## Team


| Name | Role |
|---|---|
| Mahak Makhija | Idea & Product Design |
| Dhyey Tailor | Backend Development |
| Himadary Rai & Shreya Patel | Frontend / UI |
| Karan Roy | ML & Data |

---

## Demo Video

Watch here: <paste your video link (Drive / YouTube)>

---

## License

MIT License — Built for DEVTrails 2026.

---

