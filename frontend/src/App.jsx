import { useState } from "react";

const API_URL = "http://localhost:8000";

const UI_STYLES = String.raw`
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=IBM+Plex+Mono:wght@500;600&display=swap');

:root {
  font-family: "DM Sans", "Segoe UI", Arial, sans-serif;
  color: #18212f;
  background: #f3f5f7;
  font-synthesis: none;
  text-rendering: optimizeLegibility;
  -webkit-font-smoothing: antialiased;
  --ink: #18212f;
  --muted: #667085;
  --soft: #8b95a5;
  --line: #e4e8ee;
  --line-strong: #d6dce5;
  --surface: #ffffff;
  --surface-soft: #f8fafc;
  --canvas: #f3f5f7;
  --navy: #10243e;
  --navy-2: #173451;
  --green: #157a61;
  --green-soft: #eaf6f1;
  --amber: #a86512;
  --amber-soft: #fff6e8;
  --red: #b42318;
  --red-soft: #fff0ee;
  --blue: #2864c7;
  --blue-soft: #edf4ff;
  --shadow-sm: 0 1px 2px rgba(16, 36, 62, .04), 0 5px 18px rgba(16, 36, 62, .035);
  --shadow-md: 0 12px 36px rgba(16, 36, 62, .075);
}

* {
  box-sizing: border-box;
}

html {
  scroll-behavior: smooth;
}

body {
  margin: 0;
  min-width: 320px;
  background: var(--canvas);
}

button,
textarea,
input {
  font: inherit;
}

button {
  -webkit-tap-highlight-color: transparent;
}

.app {
  min-height: 100vh;
  background:
    linear-gradient(180deg, #f7f8fa 0, #f3f5f7 240px, #f3f5f7 100%);
}

/* ---------- Navigation ---------- */

.navbar {
  position: sticky;
  top: 0;
  z-index: 50;
  min-height: 74px;
  padding: 0 5.5vw;
  display: grid;
  grid-template-columns: minmax(260px, 1fr) auto minmax(190px, 1fr);
  align-items: center;
  gap: 28px;
  background: rgba(255, 255, 255, .94);
  border-bottom: 1px solid rgba(214, 220, 229, .92);
  backdrop-filter: blur(18px);
}

.brand {
  display: flex;
  align-items: center;
  gap: 12px;
  min-width: 0;
}

.brand-icon {
  width: 38px;
  height: 38px;
  display: grid;
  place-items: center;
  flex: 0 0 38px;
  border-radius: 10px;
  background: var(--navy);
  color: #fff;
  font-family: "IBM Plex Mono", monospace;
  font-size: 12px;
  font-weight: 600;
  letter-spacing: -.03em;
  box-shadow: 0 5px 14px rgba(16, 36, 62, .16);
}

.brand h1 {
  margin: 0;
  color: var(--ink);
  font-size: 16px;
  line-height: 1.15;
  font-weight: 700;
  letter-spacing: -.025em;
}

.brand span {
  display: block;
  margin-top: 3px;
  color: #8791a0;
  font-size: 10px;
  font-weight: 500;
  letter-spacing: .02em;
}

.navbar nav {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 4px;
}

.nav-button {
  position: relative;
  border: 0;
  background: transparent;
  color: #667085;
  padding: 10px 15px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 13px;
  font-weight: 600;
  transition: color .18s ease, background .18s ease;
}

.nav-button:hover {
  color: var(--ink);
  background: #f4f6f8;
}

.nav-button.active {
  color: var(--navy);
  background: #eef2f6;
}

.nav-button.active::after {
  content: "";
  position: absolute;
  left: 15px;
  right: 15px;
  bottom: 3px;
  height: 2px;
  border-radius: 99px;
  background: var(--green);
}

.status {
  justify-self: end;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  color: #5f6b7a;
  font-size: 12px;
  font-weight: 600;
}

.status-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: #20a779;
  box-shadow: 0 0 0 4px rgba(32, 167, 121, .10);
}

/* ---------- Layout ---------- */

.container {
  width: min(1240px, calc(100% - 48px));
  margin: 0 auto;
  padding: 46px 0 72px;
}

.page-header {
  margin: 0 0 26px;
  max-width: 780px;
}

.section-label,
.eyebrow,
.card-label {
  color: #708096;
  font-size: 10px;
  font-weight: 700;
  letter-spacing: .13em;
}

.section-label {
  display: inline-flex;
  align-items: center;
  gap: 8px;
}

.section-label::before {
  content: "";
  width: 18px;
  height: 1px;
  background: #94a0b0;
}

.page-header h2 {
  margin: 10px 0 8px;
  color: var(--ink);
  font-size: clamp(30px, 4vw, 42px);
  line-height: 1.06;
  letter-spacing: -.045em;
  font-weight: 700;
}

.page-header p {
  max-width: 680px;
  margin: 0;
  color: #697586;
  font-size: 14px;
  line-height: 1.75;
}

/* ---------- Dashboard hero ---------- */

.hero {
  position: relative;
  overflow: hidden;
  min-height: 440px;
  display: grid;
  grid-template-columns: minmax(0, 1.08fr) minmax(390px, .92fr);
  gap: 50px;
  padding: 58px 62px;
  border: 1px solid #213a56;
  border-radius: 20px;
  background:
    radial-gradient(circle at 92% 8%, rgba(76, 148, 119, .16), transparent 27%),
    linear-gradient(135deg, #10243e 0%, #142d49 58%, #193b53 100%);
  box-shadow: 0 24px 60px rgba(16, 36, 62, .14);
}

.hero::after {
  content: "";
  position: absolute;
  width: 520px;
  height: 520px;
  right: -260px;
  bottom: -320px;
  border: 1px solid rgba(255,255,255,.06);
  border-radius: 50%;
  pointer-events: none;
}

.hero-content {
  position: relative;
  z-index: 1;
  align-self: center;
}

.hero .eyebrow {
  color: #9eb2c9;
}

.hero h2 {
  margin: 16px 0 17px;
  max-width: 650px;
  color: #fff;
  font-size: clamp(39px, 5.2vw, 65px);
  line-height: .99;
  letter-spacing: -.06em;
  font-weight: 700;
}

.hero h2 span {
  color: #7bc4a8;
}

.hero p {
  max-width: 650px;
  margin: 0;
  color: #c1ccda;
  font-size: 15px;
  line-height: 1.75;
}

.hero-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin: 26px 0 30px;
}

.hero-tags span {
  padding: 7px 10px;
  border: 1px solid rgba(255,255,255,.12);
  border-radius: 6px;
  color: #d4dde8;
  background: rgba(255,255,255,.045);
  font-size: 10px;
  font-weight: 600;
}

.hero-button {
  min-width: 184px;
}

.hero-visual {
  position: relative;
  z-index: 1;
  display: grid;
  place-items: center;
}

.visual-card {
  width: min(100%, 410px);
  padding: 22px;
  border: 1px solid rgba(255,255,255,.12);
  border-radius: 14px;
  background: rgba(7, 22, 38, .42);
  box-shadow: inset 0 1px 0 rgba(255,255,255,.05);
}

.visual-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-bottom: 17px;
  border-bottom: 1px solid rgba(255,255,255,.09);
  color: #93a6ba;
  font-family: "IBM Plex Mono", monospace;
  font-size: 9px;
  font-weight: 600;
  letter-spacing: .08em;
}

.pulse {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: #64c59f;
  box-shadow: 0 0 0 5px rgba(100,197,159,.10);
}

.visual-flow {
  display: grid;
  grid-template-columns: 1fr 34px 1fr 34px 1fr;
  align-items: center;
  gap: 0;
  margin: 34px 0;
}

.flow-node {
  min-height: 92px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding: 13px;
  border: 1px solid rgba(255,255,255,.09);
  border-radius: 10px;
  background: rgba(255,255,255,.035);
}

.flow-node.highlighted {
  border-color: rgba(123,196,168,.42);
  background: rgba(123,196,168,.08);
}

.flow-node strong {
  color: #fff;
  font-size: 14px;
  font-weight: 700;
}

.flow-node small {
  margin-top: 5px;
  color: #8fa1b5;
  font-size: 9px;
  line-height: 1.35;
}

.flow-line {
  position: relative;
  height: 1px;
  background: rgba(255,255,255,.18);
}

.flow-line::after {
  content: "›";
  position: absolute;
  right: -1px;
  top: -9px;
  color: #71879d;
  font-size: 14px;
}

.visual-footer {
  display: flex;
  justify-content: space-between;
  gap: 16px;
  color: #91a3b6;
  font-family: "IBM Plex Mono", monospace;
  font-size: 9px;
}

/* ---------- Dashboard cards ---------- */

.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 14px;
  margin-top: 18px;
}

.stat-card {
  min-height: 120px;
  padding: 20px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  border: 1px solid var(--line);
  border-radius: 12px;
  background: var(--surface);
  box-shadow: var(--shadow-sm);
}

.stat-icon {
  width: 27px;
  height: 27px;
  display: grid;
  place-items: center;
  border: 1px solid #dfe5ec;
  border-radius: 7px;
  color: var(--navy);
  font-size: 13px;
}

.overview-number {
  margin-top: 14px;
  color: var(--navy);
  font-family: "IBM Plex Mono", monospace;
  font-size: 25px;
  font-weight: 600;
  letter-spacing: -.04em;
}

.stat-card > span:last-child,
.stat-card label {
  color: #7b8796;
  font-size: 11px;
  font-weight: 600;
}

.dashboard-actions {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 14px;
  margin-top: 14px;
}

.action-card {
  position: relative;
  min-height: 170px;
  padding: 25px 26px 23px;
  display: grid;
  grid-template-columns: 42px 1fr auto;
  align-items: start;
  gap: 16px;
  border: 1px solid var(--line);
  border-radius: 13px;
  background: var(--surface);
  box-shadow: var(--shadow-sm);
  transition: transform .2s ease, box-shadow .2s ease, border-color .2s ease;
}

.action-card:hover {
  transform: translateY(-2px);
  border-color: #cfd7e2;
  box-shadow: var(--shadow-md);
}

.action-icon {
  width: 40px;
  height: 40px;
  display: grid;
  place-items: center;
  border-radius: 9px;
  color: var(--navy);
  background: #eef3f7;
  border: 1px solid #e0e7ee;
  font-size: 17px;
}

.action-card > div:nth-child(2) > span {
  color: #8190a1;
  font-size: 9px;
  font-weight: 700;
  letter-spacing: .12em;
}

.action-card h3 {
  margin: 6px 0 6px;
  color: var(--ink);
  font-size: 17px;
  letter-spacing: -.025em;
}

.action-card p {
  max-width: 460px;
  margin: 0;
  color: #717d8d;
  font-size: 12px;
  line-height: 1.65;
}

.action-card button {
  align-self: end;
  border: 0;
  background: transparent;
  color: var(--green);
  cursor: pointer;
  font-size: 11px;
  font-weight: 700;
  white-space: nowrap;
}

/* ---------- Buttons ---------- */

.analyze-button,
.pdf-button,
.secondary-button,
.new-analysis-button {
  border: 0;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 700;
  transition: transform .18s ease, box-shadow .18s ease, background .18s ease;
}

.analyze-button {
  min-height: 42px;
  padding: 0 17px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 9px;
  background: var(--green);
  color: #fff;
  box-shadow: 0 6px 18px rgba(21, 122, 97, .17);
  font-size: 12px;
}

.analyze-button:hover:not(:disabled) {
  transform: translateY(-1px);
  background: #116c55;
  box-shadow: 0 9px 22px rgba(21, 122, 97, .21);
}

.analyze-button:disabled,
.pdf-button:disabled {
  opacity: .55;
  cursor: not-allowed;
  box-shadow: none;
}

.secondary-button,
.new-analysis-button {
  min-height: 40px;
  padding: 0 14px;
  background: #eef2f5;
  color: #425166;
  border: 1px solid #dce2e9;
  font-size: 11px;
}

.secondary-button:hover,
.new-analysis-button:hover {
  background: #e7ecf1;
}

.pdf-button {
  min-height: 40px;
  padding: 0 15px;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: var(--navy);
  color: #fff;
  font-size: 11px;
  box-shadow: 0 5px 16px rgba(16, 36, 62, .13);
}

.pdf-button:hover:not(:disabled) {
  background: #183552;
  transform: translateY(-1px);
}

.pdf-icon {
  font-family: "IBM Plex Mono", monospace;
  font-size: 13px;
}

.pdf-spinner,
.spinner,
.dark-spinner {
  width: 14px;
  height: 14px;
  border: 2px solid currentColor;
  border-right-color: transparent;
  border-radius: 50%;
  animation: spin .7s linear infinite;
}

.pdf-spinner {
  color: #fff;
}

.spinner {
  color: #fff;
}

.dark-spinner {
  color: var(--navy);
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* ---------- Tender ---------- */

.tender-card {
  padding: 26px;
  border: 1px solid var(--line);
  border-radius: 14px;
  background: var(--surface);
  box-shadow: var(--shadow-sm);
}

.input-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 20px;
  margin-bottom: 16px;
}

.input-header label {
  display: block;
  color: var(--ink);
  font-size: 13px;
  font-weight: 700;
}

.input-header p {
  max-width: 720px;
  margin: 5px 0 0;
  color: #7a8594;
  font-size: 11px;
  line-height: 1.55;
}

.character-count {
  color: #8b95a3;
  font-family: "IBM Plex Mono", monospace;
  font-size: 9px;
  white-space: nowrap;
}

.tender-card textarea {
  width: 100%;
  min-height: 190px;
  resize: vertical;
  padding: 17px;
  border: 1px solid #d9e0e8;
  border-radius: 9px;
  outline: none;
  color: var(--ink);
  background: #fbfcfd;
  font-size: 13px;
  line-height: 1.75;
  transition: border .18s ease, box-shadow .18s ease, background .18s ease;
}

.tender-card textarea::placeholder {
  color: #a2aab5;
}

.tender-card textarea:focus {
  border-color: #82bca9;
  background: #fff;
  box-shadow: 0 0 0 3px rgba(21,122,97,.08);
}

.input-footer {
  min-height: 55px;
  padding-top: 18px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
}

.input-hint {
  display: flex;
  align-items: center;
  gap: 7px;
  color: #7a8593;
  font-size: 10px;
}

.input-hint span {
  color: var(--green);
  font-size: 9px;
}

/* ---------- Alerts ---------- */

.error-box {
  margin-top: 14px;
  padding: 14px 16px;
  display: flex;
  flex-direction: column;
  gap: 4px;
  border: 1px solid #f2c9c5;
  border-left: 3px solid var(--red);
  border-radius: 9px;
  background: #fff7f6;
}

.error-box strong {
  color: #8f1c15;
  font-size: 12px;
}

.error-box span {
  color: #9b4b44;
  font-size: 11px;
}

/* ---------- Search / explorer ---------- */

.standards-search-card {
  margin-bottom: 16px;
  padding: 18px;
  border: 1px solid var(--line);
  border-radius: 13px;
  background: var(--surface);
  box-shadow: var(--shadow-sm);
}

.search-box {
  display: flex;
  align-items: center;
  gap: 9px;
  padding: 0 12px;
  min-height: 46px;
  border: 1px solid #d7dee7;
  border-radius: 9px;
  background: #fbfcfd;
}

.search-symbol {
  color: #8591a0;
  font-size: 16px;
}

.search-box input {
  flex: 1;
  min-width: 0;
  border: 0;
  outline: none;
  background: transparent;
  color: var(--ink);
  font-size: 12px;
}

.search-box input::placeholder {
  color: #a3acb8;
}

.search-examples {
  display: flex;
  flex-wrap: wrap;
  gap: 7px;
  margin-top: 10px;
}

.search-examples span {
  padding: 5px 8px;
  border: 1px solid #e3e7ec;
  border-radius: 5px;
  color: #7a8797;
  background: #fafbfc;
  font-size: 9px;
}

.explorer-layout {
  display: grid;
  grid-template-columns: minmax(340px, .86fr) minmax(0, 1.4fr);
  gap: 16px;
  align-items: start;
}

.search-results,
.standard-intelligence {
  min-width: 0;
}

.results-header {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 15px;
  margin: 2px 0 10px;
}

.results-heading {
  color: var(--ink);
  font-size: 16px;
  font-weight: 700;
  letter-spacing: -.02em;
}

.standard-search-result {
  width: 100%;
  display: grid;
  grid-template-columns: 36px 1fr auto;
  gap: 12px;
  align-items: start;
  padding: 14px;
  margin-bottom: 7px;
  text-align: left;
  border: 1px solid var(--line);
  border-radius: 10px;
  background: #fff;
  color: inherit;
  cursor: pointer;
  transition: border .18s ease, background .18s ease, transform .18s ease;
}

.standard-search-result:hover {
  border-color: #cfd8e3;
  background: #fbfcfd;
  transform: translateY(-1px);
}

.standard-search-result.selected {
  border-color: #8fc8b5;
  background: #f6fbf9;
  box-shadow: inset 3px 0 0 var(--green);
}

.standard-result-icon {
  width: 36px;
  height: 36px;
  display: grid;
  place-items: center;
  border: 1px solid #dce3ea;
  border-radius: 8px;
  color: var(--navy);
  background: #f5f7f9;
  font-family: "IBM Plex Mono", monospace;
  font-size: 9px;
  font-weight: 600;
}

.standard-result-content {
  min-width: 0;
}

.standard-result-top {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 7px;
}

.standard-result-top strong,
.standard-number,
.primary-number,
.graph-primary-number,
.graph-node-number {
  font-family: "IBM Plex Mono", monospace;
}

.standard-result-top strong {
  color: var(--navy);
  font-size: 11px;
  font-weight: 600;
}

.standard-result-content p {
  margin: 5px 0 0;
  color: #707c8d;
  font-size: 10px;
  line-height: 1.55;
}

.result-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 5px;
  margin-top: 8px;
}

.result-tags span,
.ai-badge,
.exact-match-pill,
.confidence-pill {
  display: inline-flex;
  align-items: center;
  border-radius: 5px;
  font-size: 8px;
  font-weight: 700;
}

.result-tags span {
  padding: 4px 6px;
  background: #f0f3f6;
  color: #687588;
}

.ai-badge {
  padding: 4px 6px;
  background: var(--blue-soft);
  color: var(--blue);
}

.exact-match-pill {
  padding: 4px 6px;
  background: var(--green-soft);
  color: var(--green);
}

.confidence-pill {
  padding: 4px 6px;
  background: #f1f3f6;
  color: #6c7786;
  font-family: "IBM Plex Mono", monospace;
}

.result-arrow {
  color: #a0a9b5;
  font-size: 14px;
}

.exact-match-banner {
  margin-bottom: 12px;
  padding: 9px 11px;
  display: flex;
  align-items: center;
  gap: 7px;
  border: 1px solid #bfe2d3;
  border-radius: 7px;
  background: #f1faf6;
  color: #1b745d;
  font-size: 10px;
  font-weight: 600;
}

.explorer-empty,
.intelligence-empty {
  min-height: 340px;
  padding: 42px 24px;
  display: grid;
  place-items: center;
  align-content: center;
  text-align: center;
  border: 1px dashed #d6dde5;
  border-radius: 12px;
  background: rgba(255,255,255,.58);
}

.empty-icon,
.graph-empty-icon {
  width: 44px;
  height: 44px;
  display: grid;
  place-items: center;
  margin-bottom: 12px;
  border: 1px solid #dce3e9;
  border-radius: 10px;
  color: #6d7a8b;
  background: #f8fafb;
  font-family: "IBM Plex Mono", monospace;
  font-size: 13px;
}

.explorer-empty h3,
.intelligence-empty h3 {
  margin: 0 0 5px;
  color: var(--ink);
  font-size: 14px;
}

.explorer-empty p,
.intelligence-empty p {
  max-width: 420px;
  margin: 0;
  color: #7b8695;
  font-size: 11px;
  line-height: 1.65;
}

/* ---------- Intelligence ---------- */

.intelligence-panel {
  overflow: hidden;
  border: 1px solid var(--line);
  border-radius: 14px;
  background: var(--surface);
  box-shadow: var(--shadow-sm);
}

.intelligence-header {
  padding: 21px 22px;
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 20px;
  border-bottom: 1px solid var(--line);
  background: #fcfdfe;
}

.intelligence-header h3 {
  margin: 6px 0 4px;
  color: var(--navy);
  font-family: "IBM Plex Mono", monospace;
  font-size: 19px;
  letter-spacing: -.035em;
}

.intelligence-header p {
  margin: 0;
  color: #717d8c;
  font-size: 11px;
  line-height: 1.55;
}

.intelligence-meta {
  display: flex;
  flex-wrap: wrap;
  justify-content: flex-end;
  gap: 6px;
}

.intelligence-meta span {
  padding: 5px 7px;
  border: 1px solid #e0e5eb;
  border-radius: 5px;
  color: #718092;
  background: #fff;
  font-size: 8px;
  font-weight: 700;
}

.detail-section {
  padding: 20px 22px;
  border-bottom: 1px solid var(--line);
}

.detail-section:last-child {
  border-bottom: 0;
}

.detail-section-header,
.card-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 14px;
  margin-bottom: 12px;
}

.detail-section-header h4,
.details-heading,
.card-title-row h4 {
  margin: 0;
  color: var(--ink);
  font-size: 13px;
  font-weight: 700;
  letter-spacing: -.015em;
}

.detail-grid,
.requirements-grid,
.compliance-list {
  display: grid;
  gap: 8px;
}

.detail-grid {
  grid-template-columns: repeat(2, minmax(0, 1fr));
}

.detail-item {
  min-height: 58px;
  padding: 11px 12px;
  border: 1px solid #e7ebef;
  border-radius: 7px;
  background: #fbfcfd;
}

.detail-icon {
  display: none;
}

.detail-item span {
  display: block;
  color: #8490a0;
  font-size: 8px;
  font-weight: 700;
  letter-spacing: .06em;
  text-transform: uppercase;
}

.detail-item strong {
  display: block;
  margin-top: 5px;
  color: #314054;
  font-size: 11px;
  line-height: 1.45;
  word-break: break-word;
}

.detail-note {
  margin: 9px 0 0;
  color: #778292;
  font-size: 10px;
  line-height: 1.6;
}

.certification-status-box,
.compliance-status {
  padding: 12px 13px;
  border-radius: 8px;
  border: 1px solid #cfe5db;
  background: #f4faf7;
}

.certification-status-box strong,
.compliance-status strong {
  color: #17674f;
  font-size: 11px;
}

.compliance-row,
.requirement-item,
.evidence-row {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 16px;
  padding: 9px 0;
  border-bottom: 1px solid #edf0f3;
}

.compliance-row:last-child,
.requirement-item:last-child,
.evidence-row:last-child {
  border-bottom: 0;
}

.compliance-row span:first-child,
.requirement-item span:first-child,
.evidence-row span:first-child {
  color: #7b8795;
  font-size: 10px;
}

.compliance-row strong,
.requirement-item strong,
.evidence-row strong {
  color: #334156;
  font-size: 10px;
  text-align: right;
}

.amendment-summary {
  margin-bottom: 10px;
  color: #778292;
  font-size: 10px;
}

.amendment-list,
.certification-records {
  display: grid;
  gap: 7px;
}

.amendment-row,
.certification-record {
  padding: 10px 11px;
  border: 1px solid #e7ebef;
  border-radius: 7px;
  background: #fbfcfd;
}

.amendment-row {
  display: grid;
  grid-template-columns: 28px 1fr auto;
  align-items: center;
  gap: 10px;
}

.amendment-number {
  color: var(--navy);
  font-family: "IBM Plex Mono", monospace;
  font-size: 10px;
  font-weight: 600;
}

.amendment-row span,
.certification-record span {
  color: #788494;
  font-size: 9px;
}

.certification-record {
  display: grid;
  gap: 4px;
}

.certification-check,
.check-circle {
  color: var(--green);
  font-weight: 700;
}

.no-data-box {
  padding: 11px;
  border: 1px dashed #d9dfe6;
  border-radius: 7px;
  color: #7f8a98;
  background: #fafbfc;
  font-size: 10px;
}

/* ---------- Report ---------- */

.results-section {
  margin-top: 20px;
}

.results-section > .results-header {
  padding: 0 0 14px;
  align-items: center;
}

.results-header h3 {
  margin: 6px 0 0;
  color: var(--navy);
  font-size: 24px;
  letter-spacing: -.035em;
}

.report-actions {
  display: flex;
  align-items: center;
  gap: 8px;
}

.success-badge,
.review-badge {
  display: inline-flex;
  align-items: center;
  min-height: 31px;
  padding: 0 10px;
  border-radius: 6px;
  font-size: 9px;
  font-weight: 700;
}

.success-badge {
  color: #17674f;
  border: 1px solid #c8e3d7;
  background: #f0faf5;
}

.review-badge {
  color: #8b5411;
  border: 1px solid #ecd6b1;
  background: #fff8ec;
}

.result-grid {
  display: grid;
  grid-template-columns: minmax(0, 1.18fr) minmax(320px, .82fr);
  gap: 14px;
}

.result-card {
  min-width: 0;
  padding: 21px;
  border: 1px solid var(--line);
  border-radius: 12px;
  background: #fff;
  box-shadow: var(--shadow-sm);
}

.card-top {
  margin-bottom: 16px;
}

.card-label {
  color: #7d8998;
}

.verified-label {
  color: var(--green);
  font-size: 8px;
  font-weight: 700;
  letter-spacing: .1em;
}

.standard-overview {
  padding: 17px;
  border: 1px solid #dfe5eb;
  border-radius: 9px;
  background: #fafcfd;
}

.standard-overview .standard-number {
  color: var(--navy);
  font-size: 16px;
  font-weight: 600;
}

.standard-overview h4 {
  margin: 6px 0 8px;
  color: #26364a;
  font-size: 15px;
  letter-spacing: -.02em;
}

.standard-overview p {
  margin: 0;
  color: #778292;
  font-size: 10px;
  line-height: 1.6;
}

.confidence-section {
  margin-top: 15px;
  padding: 13px 14px;
  border: 1px solid #e4e9ee;
  border-radius: 8px;
}

.confidence-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  color: #707d8c;
  font-size: 9px;
  font-weight: 700;
}

.confidence-header strong {
  color: var(--navy);
  font-family: "IBM Plex Mono", monospace;
}

.confidence-bar {
  height: 5px;
  margin-top: 8px;
  overflow: hidden;
  border-radius: 99px;
  background: #e9edf1;
}

.confidence-bar > div {
  height: 100%;
  border-radius: inherit;
  background: var(--green);
}

.compliance-list {
  margin-top: 13px;
}

.compliance-status {
  margin-bottom: 8px;
}

.gap-summary {
  margin-bottom: 11px;
  padding: 12px;
  border: 1px solid #e4e8ed;
  border-radius: 8px;
  background: #fafbfc;
  color: #6d7887;
  font-size: 10px;
  line-height: 1.55;
}

.gap-list {
  display: grid;
  gap: 7px;
}

.gap-item {
  padding: 11px 12px;
  display: grid;
  grid-template-columns: auto 1fr;
  gap: 10px;
  border: 1px solid #e5e9ed;
  border-radius: 8px;
  background: #fff;
}

.gap-severity {
  min-width: 50px;
  height: fit-content;
  padding: 4px 5px;
  border-radius: 4px;
  text-align: center;
  font-size: 7px;
  font-weight: 800;
  letter-spacing: .07em;
}

.gap-severity.high {
  color: var(--red);
  background: var(--red-soft);
}

.gap-severity.medium {
  color: var(--amber);
  background: var(--amber-soft);
}

.gap-severity.low {
  color: #6b7583;
  background: #f1f3f5;
}

.gap-item strong {
  display: block;
  color: #39485b;
  font-size: 10px;
}

.gap-item p {
  margin: 4px 0 0;
  color: #7a8593;
  font-size: 9px;
  line-height: 1.55;
}

.no-gaps {
  padding: 12px;
  border: 1px solid #cfe5db;
  border-radius: 8px;
  background: #f4faf7;
  color: #226d59;
  font-size: 10px;
  font-weight: 600;
}

/* ---------- Knowledge graph ---------- */

.graph-card {
  margin-top: 14px;
  padding: 21px;
  border: 1px solid var(--line);
  border-radius: 12px;
  background: #fff;
  box-shadow: var(--shadow-sm);
}

.card-title-row {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 20px;
}

.card-title-row h4 {
  margin-top: 5px;
  font-size: 15px;
}

.graph-subtitle {
  max-width: 660px;
  margin: 5px 0 0;
  color: #778392;
  font-size: 10px;
  line-height: 1.6;
}

.relationship-count {
  padding: 6px 8px;
  border: 1px solid #e2e7ec;
  border-radius: 5px;
  color: #6e7b8a;
  background: #fafbfc;
  font-family: "IBM Plex Mono", monospace;
  font-size: 8px;
  white-space: nowrap;
}

.relationship-stats {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 8px;
  margin-top: 15px;
}

.relation-stat {
  padding: 11px 12px;
  border: 1px solid #e6eaee;
  border-radius: 7px;
  background: #fbfcfd;
}

.relation-stat strong {
  display: block;
  color: var(--navy);
  font-family: "IBM Plex Mono", monospace;
  font-size: 15px;
  font-weight: 600;
}

.relation-stat span {
  display: block;
  margin-top: 3px;
  color: #7e8997;
  font-size: 8px;
  font-weight: 600;
}

.knowledge-graph {
  margin-top: 15px;
  overflow: hidden;
  border: 1px solid #e2e7ec;
  border-radius: 10px;
  background:
    linear-gradient(rgba(18, 42, 66, .035) 1px, transparent 1px),
    linear-gradient(90deg, rgba(18, 42, 66, .035) 1px, transparent 1px),
    #fbfcfd;
  background-size: 26px 26px;
}

.graph-legend {
  min-height: 43px;
  padding: 0 13px;
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 15px;
  border-bottom: 1px solid #e5e9ed;
  background: rgba(255,255,255,.88);
}

.graph-legend span {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  color: #6f7b8a;
  font-size: 8px;
  font-weight: 600;
}

.legend-dot {
  width: 7px;
  height: 7px;
  display: inline-block;
  border-radius: 50%;
  background: #98a3b0;
}

.legend-dot.primary { background: #173451; }
.legend-dot.test { background: #4675c4; }
.legend-dot.material { background: #8a62ae; }
.legend-dot.conformity { background: #4b927a; }

.graph-canvas {
  overflow-x: auto;
}

.graph-svg {
  width: 100%;
  min-width: 760px;
  height: auto;
  display: block;
}

.graph-line {
  stroke: #d6dde5;
  stroke-width: 1.3;
  stroke-dasharray: 3 4;
}

.graph-line.test { stroke: #b6c9e7; }
.graph-line.material { stroke: #d0c0df; }
.graph-line.conformity { stroke: #b9d8cc; }

.graph-node-group {
  outline: none;
}

.graph-node-group[role="button"] {
  cursor: pointer;
}

.graph-node {
  fill: #fff;
  stroke: #dbe1e7;
  stroke-width: 1;
  transition: stroke .18s ease, fill .18s ease;
}

.graph-node-group:hover .graph-node,
.graph-node-group:focus .graph-node {
  fill: #f6fbf9;
  stroke: #75b89f;
  stroke-width: 1.4;
}

.graph-node-number {
  fill: #21344b;
  font-size: 9px;
  font-weight: 600;
}

.graph-node-title {
  fill: #7a8593;
  font-family: "DM Sans", sans-serif;
  font-size: 7px;
}

.graph-primary-group {
  cursor: default;
}

.graph-primary-node {
  fill: #10243e;
  stroke: #10243e;
}

.graph-primary-label {
  fill: #82c6aa;
  font-family: "DM Sans", sans-serif;
  font-size: 7px;
  font-weight: 700;
  letter-spacing: .08em;
}

.graph-primary-number {
  fill: #fff;
  font-size: 10px;
  font-weight: 600;
}

.graph-primary-title {
  fill: #aebdcb;
  font-family: "DM Sans", sans-serif;
  font-size: 7px;
}

.graph-node-list {
  display: none;
}

.graph-summary-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
}

.graph-mini-list {
  display: grid;
  gap: 6px;
}

.graph-mini-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 7px 8px;
  border: 1px solid #e8ecf0;
  border-radius: 6px;
  background: #fff;
  color: #677485;
  font-size: 9px;
}

.graph-type {
  padding: 3px 5px;
  border-radius: 4px;
  font-size: 7px;
  font-weight: 700;
}

/* ---------- Evidence / review / audit ---------- */

.two-column {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 14px;
  margin-top: 14px;
}

.evidence-detail {
  display: grid;
  gap: 0;
}

.evidence-row {
  flex-direction: column;
  gap: 3px;
  padding: 9px 0;
}

.evidence-row strong {
  text-align: left;
  font-weight: 600;
  word-break: break-word;
}

.bis-source-button {
  color: var(--green);
  font-size: 9px;
  font-weight: 700;
  text-decoration: none;
}

.review-card {
  display: flex;
  align-items: flex-start;
  gap: 13px;
}

.review-icon {
  width: 34px;
  height: 34px;
  display: grid;
  place-items: center;
  flex: 0 0 34px;
  border-radius: 8px;
  background: var(--amber-soft);
  border: 1px solid #eed9b7;
  color: var(--amber);
}

.review-content h4 {
  margin: 0 0 5px;
  color: #344256;
  font-size: 12px;
}

.review-content p {
  margin: 0;
  color: #788493;
  font-size: 10px;
  line-height: 1.6;
}

.audit-trail {
  margin-top: 14px;
  padding: 19px 21px;
  border: 1px solid var(--line);
  border-radius: 12px;
  background: #fff;
  box-shadow: var(--shadow-sm);
}

.audit-step {
  position: relative;
  display: grid;
  grid-template-columns: 28px 1fr;
  gap: 11px;
  padding: 0 0 16px;
}

.audit-step:last-child {
  padding-bottom: 0;
}

.audit-number {
  width: 25px;
  height: 25px;
  display: grid;
  place-items: center;
  border-radius: 7px;
  background: #eef2f6;
  color: #546377;
  font-family: "IBM Plex Mono", monospace;
  font-size: 8px;
  font-weight: 600;
}

.audit-step strong {
  color: #3d4c60;
  font-size: 10px;
}

.audit-step span {
  display: block;
  margin-top: 3px;
  color: #7c8795;
  font-size: 9px;
  line-height: 1.5;
}

.audit-step:not(:last-child)::after {
  content: "";
  position: absolute;
  left: 12px;
  top: 26px;
  bottom: 0;
  width: 1px;
  background: #e2e6eb;
}

.report-actions + * {
  min-width: 0;
}

/* ---------- Loading ---------- */

.intelligence-loading {
  min-height: 340px;
  display: grid;
  place-items: center;
  gap: 11px;
  color: #778393;
  font-size: 10px;
}

.intelligence-loading .dark-spinner {
  width: 20px;
  height: 20px;
}

/* ---------- Footer ---------- */

footer {
  width: min(1240px, calc(100% - 48px));
  margin: 0 auto;
  padding: 24px 0 30px;
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 25px;
  border-top: 1px solid #dfe4ea;
  color: #8a94a2;
  font-size: 9px;
}

footer div {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

footer strong {
  color: #536174;
  font-size: 10px;
}

footer span {
  line-height: 1.5;
}

/* ---------- Utility ---------- */

.full-width {
  grid-column: 1 / -1;
}

.primary {
  color: var(--navy);
}

.test {
  color: #4675c4;
}

.material {
  color: #8a62ae;
}

.conformity {
  color: #4b927a;
}

@media (max-width: 1080px) {
  .navbar {
    grid-template-columns: 1fr auto;
  }

  .navbar nav {
    grid-column: 1 / -1;
    grid-row: 2;
    padding-bottom: 8px;
  }

  .status {
    grid-column: 2;
    grid-row: 1;
  }

  .brand {
    grid-column: 1;
    grid-row: 1;
  }

  .hero {
    grid-template-columns: 1fr;
    gap: 34px;
    padding: 48px;
  }

  .hero-visual {
    justify-items: start;
  }

  .explorer-layout {
    grid-template-columns: 1fr;
  }

  .result-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 760px) {
  .navbar {
    min-height: auto;
    padding: 12px 18px 8px;
    gap: 9px;
  }

  .brand span {
    display: none;
  }

  .status {
    font-size: 10px;
  }

  .navbar nav {
    justify-content: flex-start;
    overflow-x: auto;
  }

  .nav-button {
    padding: 8px 10px;
    font-size: 11px;
    white-space: nowrap;
  }

  .container {
    width: min(100% - 28px, 1240px);
    padding: 30px 0 48px;
  }

  .hero {
    min-height: 0;
    padding: 34px 25px;
    border-radius: 15px;
  }

  .hero h2 {
    font-size: 40px;
  }

  .hero p {
    font-size: 13px;
  }

  .visual-card {
    width: 100%;
  }

  .visual-flow {
    grid-template-columns: 1fr;
    gap: 8px;
  }

  .flow-line {
    width: 1px;
    height: 20px;
    justify-self: center;
  }

  .flow-line::after {
    right: -5px;
    top: 10px;
    transform: rotate(90deg);
  }

  .stats-grid,
  .dashboard-actions,
  .two-column {
    grid-template-columns: 1fr;
  }

  .action-card {
    grid-template-columns: 38px 1fr;
  }

  .action-card button {
    grid-column: 2;
    justify-self: start;
    margin-top: 5px;
  }

  .input-header,
  .input-footer,
  .results-header,
  .intelligence-header,
  .card-title-row {
    align-items: flex-start;
    flex-direction: column;
  }

  .tender-card,
  .result-card,
  .graph-card {
    padding: 17px;
  }

  .detail-grid,
  .relationship-stats {
    grid-template-columns: 1fr;
  }

  .report-actions,
  .intelligence-meta {
    justify-content: flex-start;
  }

  footer {
    width: min(100% - 28px, 1240px);
    flex-direction: column;
  }
}

@media (max-width: 460px) {
  .hero h2 {
    font-size: 34px;
  }

  .hero-tags {
    gap: 6px;
  }

  .hero-tags span {
    font-size: 9px;
  }

  .standard-search-result {
    grid-template-columns: 32px 1fr;
  }

  .standard-result-icon {
    width: 32px;
    height: 32px;
  }

  .result-arrow {
    display: none;
  }
}


/* ============================================================
   AUTH / LOGIN
============================================================ */
.login-shell { min-height:100vh; display:grid; grid-template-columns:1.08fr .92fr; background:#101b25; color:#f7f5ef; overflow:hidden; }
.login-panel { position:relative; display:flex; align-items:center; justify-content:center; padding:56px; background:radial-gradient(circle at 18% 20%,rgba(39,126,113,.18),transparent 34%),radial-gradient(circle at 82% 72%,rgba(177,135,52,.12),transparent 30%),#101b25; }
.login-grid { position:absolute; inset:0; opacity:.14; background-image:linear-gradient(rgba(255,255,255,.06) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.06) 1px,transparent 1px); background-size:42px 42px; mask-image:linear-gradient(to bottom,black,transparent 92%); }
.login-copy { position:relative; max-width:610px; z-index:1; }
.login-kicker { display:inline-flex; align-items:center; gap:9px; font-family:"IBM Plex Mono",monospace; font-size:11px; letter-spacing:.14em; color:#c6a65b; text-transform:uppercase; margin-bottom:22px; }
.login-kicker::before { content:""; width:28px; height:1px; background:#c6a65b; }
.login-copy h1 { margin:0; font-size:clamp(42px,5vw,68px); line-height:.98; letter-spacing:-.045em; font-weight:700; }
.login-copy h1 span { color:#74a99e; }
.login-copy p { max-width:560px; margin:24px 0 30px; color:#aab6bf; font-size:15px; line-height:1.75; }
.login-points { display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:10px; max-width:570px; }
.login-point { border:1px solid rgba(255,255,255,.10); background:rgba(255,255,255,.035); padding:12px 13px; color:#d9e0e4; font-size:12px; }
.login-point strong { display:block; font-family:"IBM Plex Mono",monospace; color:#f0e9d9; font-size:11px; margin-bottom:4px; }
.login-form-panel { display:flex; align-items:center; justify-content:center; padding:32px; background:#f3f5f7; color:#18212f; border-left:1px solid rgba(255,255,255,.08); }
.login-card { width:min(100%,440px); background:#fff; border:1px solid #dfe4ea; box-shadow:0 24px 70px rgba(0,0,0,.14); padding:34px; }
.login-card-top { display:flex; justify-content:space-between; align-items:center; margin-bottom:28px; }
.login-mark { width:44px; height:44px; display:grid; place-items:center; background:#173b3f; color:#f4e7c6; font-family:"IBM Plex Mono",monospace; font-weight:600; letter-spacing:-.05em; }
.login-status { display:inline-flex; align-items:center; gap:7px; font-family:"IBM Plex Mono",monospace; font-size:10px; color:#157a61; text-transform:uppercase; }
.login-status::before { content:""; width:7px; height:7px; border-radius:50%; background:#157a61; box-shadow:0 0 0 4px #eaf6f1; }
.login-card h2 { margin:0 0 8px; font-size:27px; letter-spacing:-.025em; }
.login-card .login-subtitle { margin:0 0 26px; color:#667085; font-size:13px; line-height:1.6; }
.login-field { margin-bottom:17px; }
.login-field label { display:block; margin-bottom:7px; font-family:"IBM Plex Mono",monospace; font-size:10px; color:#475467; letter-spacing:.06em; text-transform:uppercase; }
.login-field input { width:100%; height:46px; border:1px solid #d7dde5; background:#fbfcfd; padding:0 13px; outline:none; color:#18212f; font:inherit; transition:border-color .18s,box-shadow .18s,background .18s; }
.login-field input:focus { border-color:#4d8178; background:#fff; box-shadow:0 0 0 3px rgba(77,129,120,.12); }
.login-error { margin:0 0 15px; padding:10px 12px; border:1px solid #f1c5c0; background:#fff0ee; color:#b42318; font-size:12px; line-height:1.5; }
.login-submit { width:100%; height:48px; border:0; cursor:pointer; background:#173b3f; color:#fff; font:600 12px/1 "IBM Plex Mono",monospace; letter-spacing:.04em; text-transform:uppercase; transition:transform .15s,background .15s; }
.login-submit:hover { background:#22545a; transform:translateY(-1px); }
.login-meta { display:flex; justify-content:space-between; gap:10px; margin-top:18px; color:#8b95a5; font-size:10px; font-family:"IBM Plex Mono",monospace; }
.login-demo { margin-top:22px; padding:11px 12px; border:1px dashed #d7dde5; background:#f8fafc; color:#667085; font-size:10px; line-height:1.6; }
.login-demo strong { color:#344054; }
.nav-user { display:inline-flex; align-items:center; gap:10px; margin-left:6px; padding-left:12px; border-left:1px solid var(--line); }
.nav-user-info { display:flex; flex-direction:column; align-items:flex-end; line-height:1.15; }
.nav-user-info strong { font-size:11px; color:var(--ink); }
.nav-user-info span { margin-top:3px; font-size:9px; color:var(--muted); font-family:"IBM Plex Mono",monospace; }
.logout-button { border:1px solid var(--line-strong); background:#fff; color:var(--muted); height:31px; padding:0 10px; cursor:pointer; font:600 9px/1 "IBM Plex Mono",monospace; text-transform:uppercase; letter-spacing:.04em; }
.logout-button:hover { color:var(--red); border-color:#efc2bd; background:var(--red-soft); }
@media (max-width:920px) { .login-shell{grid-template-columns:1fr}.login-panel{min-height:42vh;padding:38px 24px}.login-form-panel{min-height:58vh;padding:24px}.login-copy h1{font-size:46px} }
@media (max-width:560px) { .login-points{grid-template-columns:1fr}.login-card{padding:25px}.nav-user-info{display:none} }

`;


function LoginScreen({ onLogin }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const submit = (event) => {
    event.preventDefault();
    const normalizedEmail = email.trim().toLowerCase();
    // Demo authentication gate. Replace with backend/JWT auth for production.
    if (normalizedEmail === "admin@standardsinsight.in" && password === "admin123") {
      const user = { name: "Procurement Officer", email: normalizedEmail, role: "Procurement Officer" };
      sessionStorage.setItem("standardsinsight_authenticated", "true");
      sessionStorage.setItem("standardsinsight_user", JSON.stringify(user));
      onLogin(user);
      return;
    }
    setError("Invalid credentials. Use the demo credentials shown below.");
  };

  return (
    <>
      <style>{UI_STYLES}</style>
      <div className="login-shell">
      <div className="login-panel">
        <div className="login-grid" />
        <div className="login-copy">
          <div className="login-kicker">PROCUREMENT INTELLIGENCE PLATFORM</div>
          <h1>Standards<span>Insight</span></h1>
          <p>AI-assisted identification of applicable Indian Standards for procurement specifications — with semantic recommendation, compliance intelligence, related standards and tender gap analysis.</p>
          <div className="login-points">
            <div className="login-point"><strong>SEMANTIC SEARCH</strong>Meaning-based IS recommendation</div>
            <div className="login-point"><strong>KNOWLEDGE GRAPH</strong>Allied and referenced standards</div>
            <div className="login-point"><strong>COMPLIANCE</strong>Version, amendments and certification</div>
            <div className="login-point"><strong>GAP ANALYSIS</strong>Detect incomplete specifications</div>
          </div>
        </div>
      </div>
      <div className="login-form-panel">
        <form className="login-card" onSubmit={submit}>
          <div className="login-card-top"><div className="login-mark">SI</div><div className="login-status">System Online</div></div>
          <h2>Sign in</h2>
          <p className="login-subtitle">Access the StandardsInsight procurement workspace.</p>
          {error && <div className="login-error">{error}</div>}
          <div className="login-field">
            <label htmlFor="login-email">Email address</label>
            <input id="login-email" type="email" autoComplete="username" value={email} onChange={(e)=>{setEmail(e.target.value);setError("");}} placeholder="officer@department.gov.in" required />
          </div>
          <div className="login-field">
            <label htmlFor="login-password">Password</label>
            <input id="login-password" type="password" autoComplete="current-password" value={password} onChange={(e)=>{setPassword(e.target.value);setError("");}} placeholder="Enter password" required />
          </div>
          <button className="login-submit" type="submit">Enter StandardsInsight →</button>
          <div className="login-meta"><span>SECURE WORKSPACE</span><span>SIH 2026 PROTOTYPE</span></div>
          <div className="login-demo"><strong>Demo access:</strong><br/>Email: admin@standardsinsight.in<br/>Password: admin123</div>
        </form>
      </div>
      </div>
    </>
  );
}

function App() {
  const [authenticated, setAuthenticated] = useState(() =>
    sessionStorage.getItem("standardsinsight_authenticated") === "true"
  );
  const [currentUser, setCurrentUser] = useState(() => {
    try { return JSON.parse(sessionStorage.getItem("standardsinsight_user") || "null"); }
    catch { return null; }
  });
  const [activePage, setActivePage] = useState("dashboard");

  const handleLogin = (user) => {
    setCurrentUser(user);
    setAuthenticated(true);
  };

  const handleLogout = () => {
    sessionStorage.removeItem("standardsinsight_authenticated");
    sessionStorage.removeItem("standardsinsight_user");
    setAuthenticated(false);
    setCurrentUser(null);
  };

  // ==========================================================
  // TENDER ANALYSIS
  // ==========================================================

  const [tenderText, setTenderText] = useState("");
  const [report, setReport] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [pdfLoading, setPdfLoading] = useState(false);

  // ==========================================================
  // STANDARDS EXPLORER
  // ==========================================================

  const [searchQuery, setSearchQuery] = useState("");
  const [searchResults, setSearchResults] = useState([]);
  const [searchLoading, setSearchLoading] = useState(false);
  const [searchError, setSearchError] = useState("");

  const [selectedStandard, setSelectedStandard] =
    useState(null);

  const [intelligenceLoading, setIntelligenceLoading] =
    useState(false);

  // ==========================================================
  // TENDER ANALYSIS
  // ==========================================================

  const analyzeTender = async () => {
    if (!tenderText.trim()) {
      setError(
        "Please enter a procurement specification or tender."
      );
      return;
    }

    setLoading(true);
    setError("");
    setReport(null);

    try {
      const response = await fetch(
        `${API_URL}/standards/procurement-report`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            tender_text: tenderText,
            top_k: 5,
          }),
        }
      );

      if (!response.ok) {
        const data = await response
          .json()
          .catch(() => null);

        throw new Error(
          data?.detail ||
            `Request failed with status ${response.status}`
        );
      }

      const data = await response.json();

      setReport(data);
    } catch (err) {
      console.error(err);

      setError(
        err.message ||
          "Unable to connect to the StandardsInsight backend."
      );
    } finally {
      setLoading(false);
    }
  };

  // ==========================================================
  // PDF PROCUREMENT REPORT
  // ==========================================================

  const downloadProcurementPDF = async () => {
    if (!tenderText.trim()) {
      setError("Tender text is not available for PDF generation.");
      return;
    }

    try {
      setPdfLoading(true);
      setError("");

      const response = await fetch(
        `${API_URL}/standards/procurement-report/pdf`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            tender_text: tenderText,
            top_k: 5,
          }),
        }
      );

      if (!response.ok) {
        const data = await response
          .json()
          .catch(() => null);

        throw new Error(
          data?.detail ||
            `PDF generation failed with status ${response.status}`
        );
      }

      const blob = await response.blob();

      const downloadUrl =
        window.URL.createObjectURL(blob);

      const link =
        document.createElement("a");

      link.href = downloadUrl;
      link.download =
        "StandardsInsight_Procurement_Intelligence_Report.pdf";

      document.body.appendChild(link);
      link.click();
      link.remove();

      window.URL.revokeObjectURL(downloadUrl);

    } catch (err) {
      console.error("PDF generation error:", err);

      setError(
        err.message ||
          "Unable to generate the procurement PDF report."
      );
    } finally {
      setPdfLoading(false);
    }
  };

  const clearAnalysis = () => {
    setTenderText("");
    setReport(null);
    setError("");
  };

  // ==========================================================
  // STANDARD SEARCH
  // ==========================================================

  const searchStandards = async () => {
    if (!searchQuery.trim()) {
      setSearchError(
        "Enter a product, material, application, or standard number."
      );
      return;
    }

    setSearchLoading(true);
    setSearchError("");
    setSearchResults([]);
    setSelectedStandard(null);

    try {
      const response = await fetch(
        `${API_URL}/standards/search`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            query: searchQuery,
            top_k: 10,
          }),
        }
      );

      if (!response.ok) {
        const data = await response
          .json()
          .catch(() => null);

        throw new Error(
          data?.detail ||
            `Search failed with status ${response.status}`
        );
      }

      const data = await response.json();

      const results = Array.isArray(data)
        ? data
        : data.results ||
          data.standards ||
          [];

      setSearchResults(results);

      // Automatically open exact standard result
      if (
        results.length === 1 &&
        results[0].match_type ===
          "EXACT_STANDARD_NUMBER"
      ) {
        loadStandardIntelligence(results[0]);
      }
    } catch (err) {
      console.error(err);

      setSearchError(
        err.message ||
          "Unable to search the standards database."
      );
    } finally {
      setSearchLoading(false);
    }
  };

  // ==========================================================
  // LOAD STANDARD INTELLIGENCE
  // ==========================================================

  const loadStandardIntelligence = async (
    standard
  ) => {
    const id =
      standard?.id ||
      standard?.standard_id;

    if (!id) {
      return;
    }

    setSelectedStandard({
      ...standard,
      intelligence: null,
    });

    setIntelligenceLoading(true);

    try {
      const [
        versionResponse,
        amendmentResponse,
        certificationResponse,
        relationshipResponse,
      ] = await Promise.all([
        fetch(
          `${API_URL}/standards/${id}/version`
        ),
        fetch(
          `${API_URL}/standards/${id}/amendments`
        ),
        fetch(
          `${API_URL}/standards/${id}/certification`
        ),
        fetch(
          `${API_URL}/standards/${id}/relationships`
        ),
      ]);

      const [
        version,
        amendments,
        certification,
        relationships,
      ] = await Promise.all([
        safeJson(versionResponse),
        safeJson(amendmentResponse),
        safeJson(certificationResponse),
        safeJson(relationshipResponse),
      ]);

      setSelectedStandard({
        ...standard,

        intelligence: {
          version,
          amendments,
          certification,
          relationships,
        },
      });
    } catch (err) {
      console.error(
        "Standard intelligence error:",
        err
      );

      setSelectedStandard({
        ...standard,

        intelligence: {
          version: null,
          amendments: null,
          certification: null,
          relationships: null,

          error:
            "Unable to load standard intelligence.",
        },
      });
    } finally {
      setIntelligenceLoading(false);
    }
  };

  // ==========================================================
  // NAVIGATION
  // ==========================================================

  const openTenderPage = () => {
    setActivePage("tender");

    window.scrollTo({
      top: 0,
      behavior: "smooth",
    });
  };

  const openStandardsPage = () => {
    setActivePage("standards");

    window.scrollTo({
      top: 0,
      behavior: "smooth",
    });
  };

  const openReportStandardIntelligence = (standard) => {
    if (!standard?.id) {
      return;
    }

    setActivePage("standards");
    loadStandardIntelligence({
      ...standard,
      id: standard.id,
      is_number:
        standard.is_number ||
        standard.standard_number ||
        standard.reference,
    });

    window.scrollTo({
      top: 0,
      behavior: "smooth",
    });
  };

  // ==========================================================
  // AUTH GATE
  // ==========================================================

  if (!authenticated) {
    return <LoginScreen onLogin={handleLogin} />;
  }

  // ==========================================================
  // RENDER
  // ==========================================================

  return (
    <div className="app">
    <style>{UI_STYLES}</style>

      {/* ======================================================
          NAVBAR
      ====================================================== */}

      <header className="navbar">

        <div className="brand">

          <div className="brand-icon">
            SI
          </div>

          <div>
            <h1>
              StandardsInsight
            </h1>

            <span>
              Indian Standards Intelligence Platform
            </span>
          </div>

        </div>

        <nav>

          <button
            className={
              activePage === "dashboard"
                ? "nav-button active"
                : "nav-button"
            }
            onClick={() =>
              setActivePage("dashboard")
            }
          >
            Dashboard
          </button>

          <button
            className={
              activePage === "tender"
                ? "nav-button active"
                : "nav-button"
            }
            onClick={openTenderPage}
          >
            Tender Analysis
          </button>

          <button
            className={
              activePage === "standards"
                ? "nav-button active"
                : "nav-button"
            }
            onClick={openStandardsPage}
          >
            Standards
          </button>

        </nav>

        <div className="status">
          <span className="status-dot"></span>
          System Online
        </div>

        <div className="nav-user">
          <div className="nav-user-info">
            <strong>{currentUser?.name || "Procurement Officer"}</strong>
            <span>{currentUser?.role || "Procurement Officer"}</span>
          </div>
          <button className="logout-button" onClick={handleLogout}>Sign out</button>
        </div>

      </header>


      {/* ======================================================
          DASHBOARD
      ====================================================== */}

      {activePage === "dashboard" && (

        <main className="container">

          <section className="hero">

            <div className="hero-content">

              <div className="eyebrow">
                AI-POWERED PROCUREMENT INTELLIGENCE
              </div>

              <h2>
                Identify the right
                <span> Indian Standards</span>
              </h2>

              <p>
                Analyze procurement specifications,
                discover applicable BIS standards,
                detect compliance gaps, and receive
                evidence-backed recommendations.
              </p>

              <div className="hero-tags">

                <span>
                  Semantic Search
                </span>

                <span>
                  Compliance Intelligence
                </span>

                <span>
                  Knowledge Graph
                </span>

                <span>
                  Human-in-the-Loop
                </span>

              </div>

              <button
                className="analyze-button hero-button"
                onClick={openTenderPage}
              >
                Start Tender Analysis →
              </button>

            </div>


            <div className="hero-visual">

              <div className="visual-card">

                <div className="visual-header">
                  <span>
                    AI ANALYSIS ENGINE
                  </span>

                  <span className="pulse"></span>
                </div>

                <div className="visual-flow">

                  <div className="flow-node">
                    <strong>
                      Tender
                    </strong>

                    <small>
                      Specification
                    </small>
                  </div>

                  <div className="flow-line"></div>

                  <div className="flow-node highlighted">
                    <strong>
                      AI
                    </strong>

                    <small>
                      Semantic Match
                    </small>
                  </div>

                  <div className="flow-line"></div>

                  <div className="flow-node">
                    <strong>
                      BIS
                    </strong>

                    <small>
                      Standards
                    </small>
                  </div>

                </div>

                <div className="visual-footer">
                  <span>
                    314 Standards
                  </span>

                  <span>
                    39 Relationships
                  </span>
                </div>

              </div>

            </div>

          </section>


          <section className="stats-grid">

            <StatCard
              value="314"
              label="Standards Indexed"
              icon="◎"
            />

            <StatCard
              value="39"
              label="Knowledge Relationships"
              icon="◇"
            />

            <StatCard
              value="4"
              label="Certification Records"
              icon="✓"
            />

            <StatCard
              value="AI"
              label="Human Verified"
              icon="◈"
            />

          </section>


          <section className="dashboard-actions">

            <div className="action-card">

              <div className="action-icon">
                ⌕
              </div>

              <div>
                <span>
                  STANDARD DISCOVERY
                </span>

                <h3>
                  Explore Indian Standards
                </h3>

                <p>
                  Search standards using products,
                  materials, applications, or technical
                  requirements.
                </p>
              </div>

              <button
                onClick={openStandardsPage}
              >
                Explore Standards →
              </button>

            </div>


            <div className="action-card">

              <div className="action-icon">
                ▣
              </div>

              <div>
                <span>
                  PROCUREMENT INTELLIGENCE
                </span>

                <h3>
                  Analyze a Tender
                </h3>

                <p>
                  Identify applicable standards and
                  detect procurement compliance gaps.
                </p>
              </div>

              <button
                onClick={openTenderPage}
              >
                Analyze Tender →
              </button>

            </div>

          </section>

        </main>
      )}


      {/* ======================================================
          TENDER PAGE
      ====================================================== */}

      {activePage === "tender" && (

        <main className="container">

          <section className="page-header">

            <span className="section-label">
              PROCUREMENT INTELLIGENCE
            </span>

            <h2>
              Analyze a Tender
            </h2>

            <p>
              Paste your procurement requirement to
              identify applicable Indian Standards
              and evaluate compliance.
            </p>

          </section>


          <div className="tender-card">

            <div className="input-header">

              <div>

                <label>
                  Tender / Procurement Specification
                </label>

                <p>
                  Include product, material, grade,
                  application, certification requirements,
                  or explicit IS references.
                </p>

              </div>

              <span className="character-count">
                {tenderText.length} characters
              </span>

            </div>


            <textarea
              value={tenderText}
              onChange={(e) =>
                setTenderText(e.target.value)
              }
              placeholder="Example: Procurement of Ordinary Portland Cement 43 Grade for building construction. BIS certification is mandatory."
              disabled={loading}
            />


            <div className="input-footer">

              <div className="input-hint">

                <span>
                  ●
                </span>

                AI recommendation will be subject
                to confidence-based human verification.

              </div>


              <button
                className="analyze-button"
                onClick={analyzeTender}
                disabled={loading}
              >

                {loading ? (
                  <>
                    <span className="spinner"></span>
                    Analyzing...
                  </>
                ) : (
                  <>
                    Analyze Tender
                    <span>→</span>
                  </>
                )}

              </button>

            </div>

          </div>


          {error && (

            <div className="error-box">

              <strong>
                Analysis failed
              </strong>

              <span>
                {error}
              </span>

            </div>

          )}


          {report && (

            <ReportView
              report={report}
              tenderText={tenderText}
              onNewAnalysis={clearAnalysis}
              onDownloadPDF={downloadProcurementPDF}
              pdfLoading={pdfLoading}
              onOpenStandardIntelligence={openReportStandardIntelligence}
            />

          )}

        </main>
      )}


      {/* ======================================================
          STANDARDS EXPLORER
      ====================================================== */}

      {activePage === "standards" && (

        <main className="container">

          <section className="page-header">

            <span className="section-label">
              STANDARD DISCOVERY
            </span>

            <h2>
              Standards Explorer
            </h2>

            <p>
              Search the StandardsInsight knowledge
              base using products, materials, applications,
              or technical terms.
            </p>

          </section>


          <section className="standards-search-card">

            <div className="search-box">

              <span className="search-symbol">
                ⌕
              </span>

              <input
                value={searchQuery}
                onChange={(e) =>
                  setSearchQuery(e.target.value)
                }
                onKeyDown={(e) => {

                  if (e.key === "Enter") {
                    searchStandards();
                  }

                }}
                placeholder="Search e.g. IS 269:2015, ordinary Portland cement, coarse aggregate..."
              />

              <button
                onClick={searchStandards}
                disabled={searchLoading}
              >
                {searchLoading
                  ? "Searching..."
                  : "Search Standards"}
              </button>

            </div>


            <div className="search-examples">

              <span>
                Try:
              </span>

              <button
                onClick={() => {
                  setSearchQuery(
                    "IS 269:2015"
                  );
                }}
              >
                IS 269:2015
              </button>

              <button
                onClick={() => {
                  setSearchQuery(
                    "ordinary Portland cement"
                  );
                }}
              >
                Ordinary Portland Cement
              </button>

              <button
                onClick={() => {
                  setSearchQuery(
                    "coarse aggregate for concrete"
                  );
                }}
              >
                Coarse Aggregate
              </button>

            </div>

          </section>


          {searchError && (

            <div className="error-box">

              <strong>
                Search failed
              </strong>

              <span>
                {searchError}
              </span>

            </div>

          )}


          <div className="explorer-layout">

            {/* =================================================
                SEARCH RESULTS
            ================================================= */}

            <section className="search-results">

              <div className="results-heading">

                <span className="section-label">
                  SEARCH RESULTS
                </span>

                <h3>
                  {searchResults.length
                    ? `${searchResults.length} Standards Found`
                    : "Standards"}
                </h3>

              </div>


              {searchResults.length === 0 && (

                <div className="explorer-empty">

                  <div className="empty-icon">
                    ⌕
                  </div>

                  <h3>
                    Search the standards database
                  </h3>

                  <p>
                    Enter a technical requirement
                    to find semantically relevant
                    Indian Standards.
                  </p>

                </div>

              )}


              {searchResults.map(
                (standard, index) => {

                  const standardNumber =
                    standard.is_number ||
                    standard.reference ||
                    "Unknown Standard";

                  const title =
                    standard.title ||
                    "Standard title unavailable";

                  const confidence =
                    standard.rerank_score ??
                    standard.score ??
                    standard.confidence;

                  const isExact =
                    standard.match_type ===
                    "EXACT_STANDARD_NUMBER";

                  const isSelected =
                    selectedStandard?.id ===
                    standard.id;


                  return (

                    <button
                      className={
                        isSelected
                          ? "standard-search-result selected"
                          : "standard-search-result"
                      }
                      key={
                        standard.id ||
                        `${standardNumber}-${index}`
                      }
                      onClick={() =>
                        loadStandardIntelligence(
                          standard
                        )
                      }
                    >

                      <div className="standard-result-icon">
                        IS
                      </div>


                      <div className="standard-result-content">

                        <div className="standard-result-top">

                          <strong>
                            {standardNumber}
                          </strong>


                          {isExact ? (

                            <span className="exact-match-pill">
                              ✓ EXACT MATCH
                            </span>

                          ) : confidence !==
                            undefined ? (

                            <span className="confidence-pill">
                              {formatPercentage(
                                confidence
                              )}
                            </span>

                          ) : null}

                        </div>


                        <h4>
                          {title}
                        </h4>


                        <div className="result-tags">

                          {standard.domain && (
                            <span>
                              {standard.domain}
                            </span>
                          )}

                          {standard.standard_type && (
                            <span>
                              {standard.standard_type}
                            </span>
                          )}

                          {standard.status && (
                            <span>
                              {standard.status}
                            </span>
                          )}

                        </div>

                      </div>


                      <span className="result-arrow">
                        →
                      </span>

                    </button>

                  );

                }
              )}

            </section>


            {/* =================================================
                INTELLIGENCE
            ================================================= */}

            <section className="standard-intelligence">

              {!selectedStandard && (

                <div className="intelligence-empty">

                  <div className="intelligence-icon">
                    ◇
                  </div>

                  <h3>
                    Standard Intelligence
                  </h3>

                  <p>
                    Select a standard from the search
                    results to view its version, amendments,
                    certification, and related standards.
                  </p>

                </div>

              )}


              {selectedStandard && (

                <StandardIntelligence
                  standard={selectedStandard}
                  loading={intelligenceLoading}
                />

              )}

            </section>

          </div>

        </main>
      )}


      {/* ======================================================
          FOOTER
      ====================================================== */}

      <footer>

        <div>

          <strong>
            StandardsInsight
          </strong>

          <span>
            AI-Powered Recommendation Engine
            for Indian Standards
          </span>

        </div>

        <span>
          Metadata-level analysis • Human verification enabled
        </span>

      </footer>

    </div>
  );
}


/* ============================================================
   STANDARD INTELLIGENCE
============================================================ */

function StandardIntelligence({
  standard,
  loading,
}) {
  const intelligence =
    standard?.intelligence;

  const version =
    intelligence?.version || {};

  const amendments =
    intelligence?.amendments || {};

  const certification =
    intelligence?.certification || {};

  const relationships =
    intelligence?.relationships || {};


  // ----------------------------------------------------------
  // Handle different backend response shapes
  // ----------------------------------------------------------

  const amendmentList =
    Array.isArray(amendments)
      ? amendments
      : amendments?.amendments ||
        amendments?.records ||
        [];


  const certificationList =
    certification?.certifications ||
    [];


  const graphStandards =
    relationships?.standards ||
    [];


  return (

    <div className="intelligence-panel">

      {/* ======================================================
          HEADER
      ====================================================== */}

      <div className="intelligence-header">

        <div>

          <span className="card-label">
            STANDARD INTELLIGENCE
          </span>

          <h3 className="details-heading">
            Detailed Standard Profile
          </h3>

        </div>

        <span className="verified-label">
          BIS DATA
        </span>

      </div>


      {/* ======================================================
          STANDARD OVERVIEW
      ====================================================== */}

      <div className="standard-overview">

        <div className="overview-number">

          {standard.is_number ||
            standard.reference ||
            "Unknown Standard"}

        </div>


        <h2>

          {standard.title ||
            "Standard title unavailable"}

        </h2>


        <div className="intelligence-meta">

          {standard.domain && (
            <span>
              {standard.domain}
            </span>
          )}

          {standard.standard_type && (
            <span>
              {standard.standard_type}
            </span>
          )}

          {standard.status && (
            <span>
              {standard.status}
            </span>
          )}

        </div>


        {standard.match_type ===
          "EXACT_STANDARD_NUMBER" && (

          <div className="exact-match-banner">

            ✓ Exact Standard Number Match

          </div>

        )}

      </div>


      {/* ======================================================
          LOADING
      ====================================================== */}

      {loading ? (

        <div className="intelligence-loading">

          <span className="spinner dark-spinner"></span>

          Loading standard intelligence...

        </div>

      ) : intelligence?.error ? (

        <div className="error-box">
          {intelligence.error}
        </div>

      ) : (

        <>

          {/* ==================================================
              VERSION
          ================================================== */}

          <div className="detail-section">

            <DetailSectionHeader
              icon="V"
              label="VERSION INTELLIGENCE"
              title="Version & Supersession"
            />


            <div className="detail-grid">

              <DetailItem
                label="Version Status"
                value={
                  version.version_status ||
                  "Current"
                }
              />

              <DetailItem
                label="Current Standard"
                value={
                  version.current_standard
                    ?.is_number ||
                  standard.is_number ||
                  "Not available"
                }
              />

              <DetailItem
                label="Relationship"
                value={
                  version.relationship ||
                  "No supersession relationship"
                }
              />

              <DetailItem
                label="Supersedes"
                value={
                  version.supersedes ||
                  "None recorded"
                }
              />

            </div>


            {version.resolution_note && (

              <div className="detail-note">

                <strong>
                  Resolution
                </strong>

                <p>
                  {version.resolution_note}
                </p>

              </div>

            )}

          </div>


          {/* ==================================================
              CERTIFICATION
          ================================================== */}

          <div className="detail-section">

            <DetailSectionHeader
              icon="C"
              label="CERTIFICATION INTELLIGENCE"
              title="BIS Certification & QCO"
            />


            <div className="certification-status-box">

              <div className="certification-check">
                ✓
              </div>

              <div>

                <strong>
                  {certification.overall_status ||
                    "No Certification Evidence"}
                </strong>

                <small>
                  Overall Certification Status
                </small>

              </div>

            </div>


            <div className="detail-grid">

              <DetailItem
                label="Compulsory"
                value={
                  certification.compulsory
                    ? "YES"
                    : "NO"
                }
                highlight={
                  certification.compulsory
                }
              />

              <DetailItem
                label="Certification Records"
                value={
                  certification.certification_count ??
                  certificationList.length
                }
              />

            </div>


            {certificationList.length > 0 && (

              <div className="certification-records">

                {certificationList.map(
                  (record, index) => (

                    <div
                      className="certification-record"
                      key={index}
                    >

                      <div className="record-header">

                        <strong>
                          {record.scheme ||
                            "BIS Certification"}
                        </strong>

                        {record.compulsory && (
                          <span>
                            COMPULSORY
                          </span>
                        )}

                      </div>


                      <DetailItem
                        label="Status"
                        value={
                          record.certification_status ||
                          "Not specified"
                        }
                      />

                      <DetailItem
                        label="Product Category"
                        value={
                          record.product_category ||
                          "Not specified"
                        }
                      />

                      <DetailItem
                        label="QCO"
                        value={
                          record.qco_name ||
                          "Not specified"
                        }
                      />

                      {record.notification_reference && (

                        <DetailItem
                          label="Notification"
                          value={
                            record.notification_reference
                          }
                        />

                      )}

                    </div>

                  )
                )}

              </div>

            )}

          </div>


          {/* ==================================================
              AMENDMENTS
          ================================================== */}

          <div className="detail-section">

            <DetailSectionHeader
              icon="A"
              label="AMENDMENT INTELLIGENCE"
              title="Amendment History"
            />


            <div className="amendment-summary">

              <div>

                <strong>
                  {amendmentList.length}
                </strong>

                <span>
                  Recorded Amendments
                </span>

              </div>


              <div>

                <strong>
                  {getLatestAmendmentYear(
                    amendmentList
                  )}
                </strong>

                <span>
                  Latest Amendment
                </span>

              </div>

            </div>


            {amendmentList.length > 0 ? (

              <div className="amendment-list">

                {amendmentList.map(
                  (amendment, index) => (

                    <div
                      className="amendment-row"
                      key={index}
                    >

                      <div className="amendment-number">

                        {amendment.amendment_number ||
                          index + 1}

                      </div>

                      <div>

                        <strong>
                          Amendment{" "}
                          {amendment.amendment_number ||
                            index + 1}
                        </strong>

                        <span>
                          Year:{" "}
                          {amendment.amendment_year ||
                            "Not specified"}
                        </span>

                      </div>

                    </div>

                  )
                )}

              </div>

            ) : (

              <div className="no-data-box">

                No amendment records are currently
                available for this standard in the
                verified dataset.

              </div>

            )}

          </div>


          {/* ==================================================
              KNOWLEDGE GRAPH
          ================================================== */}

          <div className="detail-section">

            <DetailSectionHeader
              icon="G"
              label="KNOWLEDGE GRAPH"
              title="Related Standards"
            />


            <div className="graph-counts detailed">

              <div>

                <strong>
                  {relationships.relationship_count ||
                    0}
                </strong>

                <span>
                  Relationships
                </span>

              </div>


              <div>

                <strong>
                  {relationships.category_counts
                    ?.test_references || 0}
                </strong>

                <span>
                  Test References
                </span>

              </div>


              <div>

                <strong>
                  {relationships.category_counts
                    ?.material_references || 0}
                </strong>

                <span>
                  Material
                </span>

              </div>


              <div>

                <strong>
                  {relationships.category_counts
                    ?.conformity_inputs || 0}
                </strong>

                <span>
                  Conformity
                </span>

              </div>

            </div>


            {graphStandards.length > 0 && (

              <div className="graph-mini-list">

                {graphStandards
                  .slice(0, 8)
                  .map((item, index) => (

                    <div
                      className="graph-mini-item"
                      key={index}
                    >

                      <span className="graph-type">

                        {getRelationshipInitial(
                          item.relationship_type
                        )}

                      </span>


                      <div>

                        <strong>
                          {item.is_number ||
                            item.standard_number ||
                            item.reference ||
                            "Standard"}
                        </strong>

                        <small>
                          {item.relationship_type ||
                            "Related Standard"}
                        </small>

                      </div>

                    </div>

                  ))}

              </div>

            )}

          </div>


          {/* ==================================================
              EVIDENCE
          ================================================== */}

          <div className="detail-section">

            <DetailSectionHeader
              icon="E"
              label="EVIDENCE"
              title="BIS Source & Verification"
            />


            <div className="evidence-detail">

              <DetailItem
                label="Source Authority"
                value={
                  standard.source_authority ||
                  "BIS"
                }
              />

              <DetailItem
                label="Source Type"
                value={
                  standard.source_type ||
                  "BIS Source"
                }
              />

              <DetailItem
                label="Verification Status"
                value={
                  standard.verification_status ||
                  "Not specified"
                }
              />

              <DetailItem
                label="Source Document"
                value={
                  standard.source_document ||
                  "Not available"
                }
              />

            </div>


            {standard.source_url && (

              <a
                className="bis-source-button"
                href={standard.source_url}
                target="_blank"
                rel="noreferrer"
              >
                Open BIS Source →
              </a>

            )}

          </div>

        </>

      )}

    </div>
  );
}


/* ============================================================
   KNOWLEDGE GRAPH
============================================================ */

function KnowledgeGraph({
  primary,
  relationships = [],
}) {
  const nodes = relationships
    .filter(
      (item) =>
        item?.is_number ||
        item?.standard_number ||
        item?.reference
    )
    .slice(0, 12);

  const centerX = 430;
  const centerY = 190;
  const radiusX = 285;
  const radiusY = 135;

  const graphNodes = nodes.map((item, index) => {
    const angle =
      -Math.PI / 2 +
      (index * (Math.PI * 2)) /
        Math.max(nodes.length, 1);

    return {
      ...item,
      x:
        centerX +
        Math.cos(angle) * radiusX,
      y:
        centerY +
        Math.sin(angle) * radiusY,
    };
  });

  const primaryNumber =
    primary?.is_number ||
    "Recommended Standard";

  const primaryTitle =
    primary?.title ||
    "AI-selected procurement standard";

  if (!graphNodes.length) {
    return (
      <div className="graph-empty">
        <span className="graph-empty-icon">G</span>
        <div>
          <strong>
            No related standards mapped yet
          </strong>
          <p>
            The primary recommendation is available,
            but no verified relationship records were
            returned for this analysis.
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="knowledge-graph">

      <div className="graph-legend">

        <span>
          <i className="legend-dot primary"></i>
          Recommended
        </span>

        <span>
          <i className="legend-dot test"></i>
          Test
        </span>

        <span>
          <i className="legend-dot material"></i>
          Material
        </span>

        <span>
          <i className="legend-dot conformity"></i>
          Conformity
        </span>

      </div>


      <div className="graph-canvas">

        <svg
          className="graph-svg"
          viewBox="0 0 860 380"
          role="img"
          aria-label="Knowledge graph of related Indian Standards"
        >

          <defs>
            <filter
              id="graphShadow"
              x="-30%"
              y="-30%"
              width="160%"
              height="160%"
            >
              <feDropShadow
                dx="0"
                dy="3"
                stdDeviation="4"
                floodOpacity="0.10"
              />
            </filter>
          </defs>


          {/* RELATIONSHIP LINES */}

          {graphNodes.map((node, index) => (
            <line
              key={`line-${index}`}
              className={`graph-line ${getGraphCategory(node.relationship_type)}`}
              x1={centerX}
              y1={centerY}
              x2={node.x}
              y2={node.y}
            />
          ))}


          {/* RELATED NODES */}

          {graphNodes.map((node, index) => {
            const category =
              getGraphCategory(
                node.relationship_type
              );

            const number =
              node.is_number ||
              node.standard_number ||
              node.reference ||
              "Standard";

            const title =
              node.title || "";

            const shortTitle =
              title.length > 30
                ? `${title.slice(0, 30)}…`
                : title;

            return (
              <g
                key={`node-${index}`}
                className={`graph-node-group ${category}`}
                transform={`translate(${node.x - 67}, ${node.y - 29})`}
                role={node.id ? "button" : undefined}
                tabIndex={node.id ? 0 : undefined}
                onClick={() =>
                  node.id &&
                  onOpenStandardIntelligence &&
                  onOpenStandardIntelligence(node)
                }
                onKeyDown={(event) => {
                  if (
                    node.id &&
                    (event.key === "Enter" || event.key === " ")
                  ) {
                    event.preventDefault();
                    onOpenStandardIntelligence &&
                      onOpenStandardIntelligence(node);
                  }
                }}
              >

                <rect
                  className="graph-node"
                  width="134"
                  height="58"
                  rx="8"
                  filter="url(#graphShadow)"
                />

                <text
                  className="graph-node-number"
                  x="67"
                  y="22"
                  textAnchor="middle"
                >
                  {number}
                </text>

                <text
                  className="graph-node-title"
                  x="67"
                  y="40"
                  textAnchor="middle"
                >
                  {shortTitle || "Related Standard"}
                </text>

              </g>
            );
          })}


          {/* PRIMARY NODE */}

          <g
            className="graph-primary-group"
            transform={`translate(${centerX - 91}, ${centerY - 48})`}
          >

            <rect
              className="graph-primary-node"
              width="182"
              height="96"
              rx="12"
              filter="url(#graphShadow)"
            />

            <text
              className="graph-primary-label"
              x="91"
              y="24"
              textAnchor="middle"
            >
              AI RECOMMENDED
            </text>

            <text
              className="graph-primary-number"
              x="91"
              y="49"
              textAnchor="middle"
            >
              {primaryNumber}
            </text>

            <text
              className="graph-primary-title"
              x="91"
              y="70"
              textAnchor="middle"
            >
              {primaryTitle.length > 26
                ? `${primaryTitle.slice(0, 26)}…`
                : primaryTitle}
            </text>

          </g>

        </svg>

      </div>


      <div className="graph-node-list">

        {graphNodes.map((item, index) => (
          <div
            className={`graph-node-summary ${getGraphCategory(
              item.relationship_type
            )}`}
            key={`summary-${index}`}
          >

            <span className="graph-summary-dot"></span>

            <div>
              <strong>
                {item.is_number ||
                  item.standard_number ||
                  item.reference ||
                  "Standard"}
              </strong>

              <small>
                {prettyValue(
                  item.relationship_type ||
                    "Related Standard"
                )}
              </small>
            </div>

          </div>
        ))}

      </div>

    </div>
  );
}


function getGraphCategory(
  relationshipType
) {
  const value = String(
    relationshipType || ""
  ).toUpperCase();

  if (value.includes("TEST")) {
    return "test";
  }

  if (value.includes("MATERIAL")) {
    return "material";
  }

  if (value.includes("CONFORMITY")) {
    return "conformity";
  }

  return "related";
}


/* ============================================================
   DETAIL SECTION HEADER
============================================================ */

function DetailSectionHeader({
  icon,
  label,
  title,
}) {
  return (
    <div className="detail-section-header">

      <div className="detail-icon">
        {icon}
      </div>

      <div>

        <span>
          {label}
        </span>

        <h4>
          {title}
        </h4>

      </div>

    </div>
  );
}


/* ============================================================
   DETAIL ITEM
============================================================ */

function DetailItem({
  label,
  value,
  highlight = false,
}) {
  return (
    <div className="detail-item">

      <span>
        {label}
      </span>

      <strong
        className={
          highlight
            ? "detail-highlight"
            : ""
        }
      >
        {value || "Not available"}
      </strong>

    </div>
  );
}


/* ============================================================
   REPORT VIEW
============================================================ */

function ReportView({
  report,
  tenderText,
  onNewAnalysis,
  onDownloadPDF,
  pdfLoading,
  onOpenStandardIntelligence,
}) {
  return (
    <section className="results-section">

      <div className="results-header">

        <div>

          <span className="section-label">
            PROCUREMENT INTELLIGENCE REPORT
          </span>

          <h3>
            Analysis Results
          </h3>

        </div>

        <div
          className={
            report.executive_status ===
            "HUMAN REVIEW REQUIRED"
              ? "review-badge"
              : "success-badge"
          }
        >

          {report.executive_status ===
          "HUMAN REVIEW REQUIRED"
            ? "⚠ Human Review Required"
            : "✓ Analysis Complete"}

        </div>

      </div>


      <div className="result-grid">

        {/* RECOMMENDED STANDARD */}

        <div className="result-card">

          <div className="card-top">

            <span className="card-label">
              RECOMMENDED STANDARD
            </span>

            <span className="ai-badge">
              AI RECOMMENDED
            </span>

          </div>


          <div className="standard-number">
            {report.recommended_standard
              ?.is_number}
          </div>


          <h4>
            {report.recommended_standard
              ?.title}
          </h4>


          <div className="confidence-section">

            <div className="confidence-header">

              <span>
                Recommendation Confidence
              </span>

              <strong>
                {formatPercentage(
                  report.recommended_standard
                    ?.confidence
                )}
              </strong>

            </div>


            <div className="confidence-bar">

              <div
                style={{
                  width: `${Math.min(
                    (
                      report
                        .recommended_standard
                        ?.confidence || 0
                    ) * 100,
                    100
                  )}%`,
                }}
              ></div>

            </div>

          </div>

        </div>


        {/* COMPLIANCE */}

        <div className="result-card">

          <div className="card-top">

            <span className="card-label">
              COMPLIANCE INTELLIGENCE
            </span>

            <span className="verified-label">
              VERIFIED
            </span>

          </div>


          <div className="compliance-status">

            <span className="check-circle">
              ✓
            </span>

            <div>

              <strong>
                {report.compliance
                  ?.status ||
                  "Not available"}
              </strong>

              <small>
                Overall Compliance Status
              </small>

            </div>

          </div>


          <div className="compliance-list">

            <ComplianceRow
              label="QCO Applicable"
              value={
                report.compliance
                  ?.qco_applicable
              }
            />

            <ComplianceRow
              label="ISI Mark Required"
              value={
                report.compliance
                  ?.isi_mark_required
              }
            />

            <ComplianceRow
              label="Latest Version"
              value={
                report.compliance
                  ?.is_latest_version
              }
            />

          </div>

        </div>

      </div>


      {/* REQUIREMENTS */}

      <div className="result-card full-width">

        <div className="card-title-row">

          <div>

            <span className="card-label">
              REQUIREMENT EXTRACTION
            </span>

            <h4>
              Tender Requirements
            </h4>

          </div>

          <span className="verified-count">
            {report.tender_requirements
              ?.verified_requirements ||
              report.gap_analysis
                ?.summary
                ?.verified_requirements ||
              0}{" "}
            Verified
          </span>

        </div>


        <div className="requirements-grid">

          <Requirement
            label="Product"
            value={
              report.tender_requirements
                ?.product
            }
          />

          <Requirement
            label="Material"
            value={
              report.tender_requirements
                ?.material
            }
          />

          <Requirement
            label="Cement Type"
            value={prettyValue(
              report.tender_requirements
                ?.cement_type
            )}
          />

          <Requirement
            label="Grade"
            value={
              report.tender_requirements
                ?.grade
            }
          />

          <Requirement
            label="Application"
            value={
              report.tender_requirements
                ?.application
            }
          />

          <Requirement
            label="BIS Certification"
            value={
              report.tender_requirements
                ?.certification_required
                ? "Required"
                : "Not specified"
            }
          />

        </div>

      </div>


      {/* GAP ANALYSIS */}

      <div className="result-card full-width">

        <div className="card-title-row">

          <div>

            <span className="card-label">
              COMPLIANCE CHECK
            </span>

            <h4>
              Procurement Gap Analysis
            </h4>

          </div>


          <div className="gap-summary">

            <div>

              <strong>
                {report.gap_analysis
                  ?.summary?.total_gaps || 0}
              </strong>

              <span>
                Total Gaps
              </span>

            </div>


            <div className="high">

              <strong>
                {report.gap_analysis
                  ?.summary?.high || 0}
              </strong>

              <span>
                High
              </span>

            </div>


            <div className="medium">

              <strong>
                {report.gap_analysis
                  ?.summary?.medium || 0}
              </strong>

              <span>
                Medium
              </span>

            </div>

          </div>

        </div>


        {report.gap_analysis
          ?.items?.length > 0 ? (

          <div className="gap-list">

            {report.gap_analysis.items.map(
              (gap, index) => (

                <GapItem
                  key={index}
                  gap={gap}
                />

              )
            )}

          </div>

        ) : (

          <div className="no-gaps">

            <div className="large-check">
              ✓
            </div>

            <div>

              <strong>
                No procurement gaps detected
              </strong>

              <p>
                All currently evaluated tender
                requirements are satisfied by
                the available intelligence.
              </p>

            </div>

          </div>

        )}

      </div>


      {/* KNOWLEDGE GRAPH */}

      <div className="result-card full-width graph-card">

        <div className="card-title-row">

          <div>
            <span className="card-label">
              KNOWLEDGE GRAPH
            </span>

            <h4>
              Standard Relationship Map
            </h4>

            <p className="graph-subtitle">
              The recommended standard is connected to
              related testing, material, and conformity standards.
            </p>
          </div>

          <span className="relationship-count">
            {report.related_standards
              ?.relationship_count || 0}{" "}
            Relationships
          </span>

        </div>


        <div className="relationship-stats">

          <RelationStat
            label="Test References"
            value={
              report.related_standards
                ?.category_counts
                ?.test_references || 0
            }
          />

          <RelationStat
            label="Material References"
            value={
              report.related_standards
                ?.category_counts
                ?.material_references || 0
            }
          />

          <RelationStat
            label="Conformity Inputs"
            value={
              report.related_standards
                ?.category_counts
                ?.conformity_inputs || 0
            }
          />

        </div>


        <KnowledgeGraph
          primary={report.recommended_standard}
          relationships={
            report.related_standards
              ?.standards || []
          }
        />

      </div>


      {/* EVIDENCE + REVIEW */}

      <div className="two-column">

        <div className="result-card">

          <div className="card-top">

            <span className="card-label">
              EVIDENCE
            </span>

            <span className="verified-label">
              BIS SOURCE
            </span>

          </div>


          <Evidence
            label="Source Authority"
            value={
              report.evidence
                ?.source_authority
            }
          />

          <Evidence
            label="Source Type"
            value={
              report.evidence
                ?.source_type
            }
          />

          <Evidence
            label="Source Document"
            value={
              report.evidence
                ?.source_document
            }
          />


          {report.evidence
            ?.source_url && (

            <div className="evidence-row">

              <span>
                Source
              </span>

              <a
                href={
                  report.evidence.source_url
                }
                target="_blank"
                rel="noreferrer"
              >
                Open BIS Source →
              </a>

            </div>

          )}

        </div>


        <div className="result-card review-card">

          <span className="card-label">
            DECISION CONTROL
          </span>


          <div className="review-content">

            <div className="review-icon">
              ⚠
            </div>

            <div>

              <h4>
                {report.human_review
                  ?.required
                  ? "Human Review Required"
                  : "Human Review Not Required"}
              </h4>


              {report.human_review
                ?.reasons?.map(
                  (reason, index) => (

                    <p key={index}>
                      {reason}
                    </p>

                  )
                )}

            </div>

          </div>

        </div>

      </div>


      {/* AUDIT TRAIL */}

      <div className="result-card full-width">

        <div className="card-top">

          <span className="card-label">
            TRACEABILITY
          </span>

          <span className="verified-label">
            AUDIT TRAIL
          </span>

        </div>


        <div className="audit-trail">

          {report.audit_trail?.map(
            (step, index) => (

              <div
                className="audit-step"
                key={index}
              >

                <div className="audit-number">
                  {index + 1}
                </div>

                <strong>
                  {prettyValue(step)}
                </strong>

              </div>

            )
          )}

        </div>

      </div>


      <div className="report-actions">

        <button
          className="pdf-button"
          onClick={onDownloadPDF}
          disabled={pdfLoading || !tenderText?.trim()}
        >
          {pdfLoading ? (
            <>
              <span className="pdf-spinner"></span>
              Generating PDF...
            </>
          ) : (
            <>
              <span className="pdf-icon">↓</span>
              Generate PDF Report
            </>
          )}
        </button>

        <button
          className="secondary-button new-analysis-button"
          onClick={onNewAnalysis}
          disabled={pdfLoading}
        >
          ← New Analysis
        </button>

      </div>

    </section>
  );
}


/* ============================================================
   SMALL COMPONENTS
============================================================ */

function StatCard({
  value,
  label,
  icon,
}) {
  return (
    <div className="stat-card">

      <div className="stat-icon">
        {icon}
      </div>

      <div>

        <strong>
          {value}
        </strong>

        <span>
          {label}
        </span>

      </div>

    </div>
  );
}


function ComplianceRow({
  label,
  value,
}) {
  return (
    <div className="compliance-row">

      <span>
        {label}
      </span>

      <strong
        className={
          value === true
            ? "yes"
            : value === false
            ? "no"
            : ""
        }
      >
        {value === true
          ? "✓ YES"
          : value === false
          ? "NO"
          : "N/A"}
      </strong>

    </div>
  );
}


function Requirement({
  label,
  value,
}) {
  return (
    <div className="requirement-item">

      <span>
        {label}
      </span>

      <strong>
        {value || "Not specified"}
      </strong>

    </div>
  );
}


function GapItem({ gap }) {
  return (
    <div
      className={`gap-item ${
        gap.severity?.toLowerCase() ||
        "medium"
      }`}
    >

      <div className="gap-severity">
        {gap.severity || "MEDIUM"}
      </div>

      <div>

        <strong>
          {gap.requirement ||
            "Procurement Requirement"}
        </strong>

        <p>
          {gap.message ||
            "Verification required."}
        </p>

        {gap.recommended_action && (

          <small>
            Recommended action:{" "}
            {gap.recommended_action}
          </small>

        )}

      </div>

    </div>
  );
}


function RelationStat({
  label,
  value,
}) {
  return (
    <div className="relation-stat">

      <strong>
        {value}
      </strong>

      <span>
        {label}
      </span>

    </div>
  );
}


function Evidence({
  label,
  value,
}) {
  if (!value) {
    return null;
  }

  return (
    <div className="evidence-row">

      <span>
        {label}
      </span>

      <strong>
        {value}
      </strong>

    </div>
  );
}


/* ============================================================
   HELPERS
============================================================ */

async function safeJson(response) {
  if (!response.ok) {
    return null;
  }

  return response.json();
}


function formatPercentage(value) {
  if (
    value === null ||
    value === undefined ||
    Number.isNaN(Number(value))
  ) {
    return "0%";
  }

  return `${(
    Number(value) * 100
  ).toFixed(2)}%`;
}


function prettyValue(value) {
  if (!value) {
    return "Not specified";
  }

  return String(value)
    .replaceAll("_", " ")
    .replace(
      /\b\w/g,
      (char) => char.toUpperCase()
    );
}


function getLatestAmendmentYear(
  amendments
) {
  if (!amendments?.length) {
    return "—";
  }

  const years = amendments
    .map(
      (item) =>
        Number(item.amendment_year)
    )
    .filter(
      (year) =>
        Number.isFinite(year) &&
        year > 0
    );

  if (!years.length) {
    return "—";
  }

  return Math.max(...years);
}


function getRelationshipInitial(
  relationshipType
) {
  const value = String(
    relationshipType || ""
  ).toUpperCase();

  if (value.includes("TEST")) {
    return "T";
  }

  if (value.includes("MATERIAL")) {
    return "M";
  }

  if (value.includes("CONFORMITY")) {
    return "C";
  }

  return "R";
}


export default App;