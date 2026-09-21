# Build Brief — Uni+ Trial Lesson Interactive Guideline

## Goal
Build a **single self-contained interactive HTML file** at the repo root named `uni-plus-trial-lesson-playbook.html`.

It is an onboarding + daily-reference playbook for **S3 AI Courses tutors and CSMs**, derived from `source/uni-plus-trial-lesson-sop-v5.md` (高試堂轉化比率注意事項和流程 V5, by Sura Tai). Purpose: raise the standard of trial-lesson delivery and hit a **>70% trial-to-enrolment conversion rate**.

## Hard constraints
- **ONE file.** No build step, no external JS/CSS/font/CDN requests. Must work fully offline by double-clicking. Inline all CSS and JS in `<style>` / `<script>`.
- **Language:** Traditional Chinese (HK) is the primary content language, exactly preserving the Cantonese scripts/話術 verbatim — these are operational scripts and must not be paraphrased or simplified. UI chrome labels may be bilingual (中文 / English).
- **Font stack** must render Traditional Chinese cleanly on Windows + macOS, e.g. `"Noto Sans TC", "Microsoft JhengHei", "PingFang TC", "Hiragino Sans", "Segoe UI", system-ui, sans-serif`.
- `<html lang="zh-Hant-HK">`, `<meta charset="utf-8">`, responsive viewport meta.
- Must be usable on a phone (tutors will open it between lessons) — responsive down to 360px.
- No emojis in the UI. Use CSS shapes, inline SVG, or text badges for iconography.

## Required sections & interactions

### 0. Header
Title, V5 version badge, owner (Sura Tai), audience (S3 AI Courses Team), and the conversion target `>70%` as a prominent KPI. Include a link back to the Notion source: `https://app.notion.com/p/V5-3e03573e5e6180f6bc6bfd0beec326da?source=copy_link`. Sticky top nav that scroll-spies the sections.

### 1. 核心原則 (3 cards)
轉化第一性原理 / 多進度平衡鐵律 / 回饋黃金三角. For 多進度平衡, render the 40% trial-student vs 60% existing-student attention split as a visual bar. For 回饋黃金三角, render the 3-step chain (特質賦能 ➔ 精準指出學術錯漏 ➔ 專屬改善方案) as a visual flow.

### 2. 【全景地圖】60 分鐘試堂時序總表 — **interactive timeline**
An interactive horizontal (desktop) / vertical (mobile) timeline covering 課前 24H–5H → 課前 15M → 0–3M → 3–20M → 20–50M → 50–55M → 55–60M → 課後 30M → 課後 24H.
- Clicking a node reveals that stage's detail panel (owner, action, deliverable).
- Colour-code by owner: 導師 / CSM / 導師+CSM / 學生.
- Visually distinguish 課前 (pre) / 課堂 (in-class) / 課後 (post) zones.

### 3. 課前載入規範
The hard rule (嚴禁課前 10 分鐘內開題庫找卷; 15 分鐘前必須就緒) styled as a prominent warning callout. Then the 【數位雙模套組】 checklist: 實體教學筆記 (Level 1 基礎核心題 / Level 2 典型變種題 / Level 3 綜合思維題) + Uni+ 電子互動看板 (視覺化思維導圖 / 步驟分解動態框 / 課題重點總結). Make the Level 1/2/3 distinction visually clear as an escalating difficulty ladder.

### 4. 課堂 TLA 節奏控制表 — **the centrepiece**
Present 0–3M 破冰 / Phase 1 (Cycle 1 + Cycle 2) / Phase 2 (Cycle 3 + 小測) / Phase 3 雙向存檔 / 55–60M 心錨+前台交付.
- For every Cycle, show the Teaching → Learning → Assessment breakdown **with its minute budget** and the 五行 tag (水/土/火/金/木) as a small badge.
- Explicitly flag which minutes are the tutor's **safe window to attend to existing students (舊生)** — this is the 多進度平衡鐵律 in practice and is the single most important thing a new tutor must internalise. Make it unmistakable (e.g. a distinct "導師可巡視舊生" band on each cycle).
- Include the 【降階防禦機制】 (student stuck → NO re-lecturing, give a verb command) as a distinct "if stuck" branch, not just a bullet.
- Include a note on 試堂生單點專注力極限 10–12 分鐘.
- All 話術 (scripts) must appear verbatim in styled quote blocks with a **copy button**.

### 5. 前台交付 30 秒 (Moment of Truth)
The 3-sentence handover (特質肯定 → 實證呈現 → 預期管理) as a numbered, copyable sequence. Plus the 學生心錨 script.

### 6. 課後家長回饋 — **interactive report generator** (most valuable interactive feature)
A form-driven builder that composes the 4-段式 report:
- Text inputs: 同學名, 課題名稱, 具體題型.
- Radio/select: 學習特質模組 A / B / C / D (show the full text of the selected module).
- Radio/select: 診斷+處方 配對 1 / 2 / 3 — selecting a 診斷 **auto-pairs** the matching 處方 (they are fixed pairs; make that coupling obvious in the UI).
- 配對 1/2/3 each have a variable slot (e.g. 負號分配／移項代數變號／繁複運算) — offer these as a dropdown of the documented options plus a free-text option.
- Live preview of the assembled report in a monospace-ish block, with **Copy to clipboard** and a character count.
- Show the 發布時效 (30 分鐘內必發) and 措辭原則 (嚴禁與學校或競品拉踩比較) as guardrails near the generator.
- Reset button. Validate that required fields are filled before enabling copy, with a gentle inline hint rather than an alert.

### 7. 模組庫 reference
All 4 特質 modules and all 3 診斷/處方 pairs browsable in full verbatim text (tabs or accordion), each independently copyable — tutors may want to read them without using the generator.

### 8. 閉環 Checklist — **interactive, stateful**
The 8-row responsibility table (時間節點 / 核心動作 / 驗收標準・產出物 / 責任人) as tickable checkboxes with:
- A live progress ring or bar (e.g. "5 / 8 完成").
- Persist state to `localStorage` so a tutor can tick through a real lesson.
- A "重設 checklist" button.
- Filter or grouping by 責任人 (導師 / CSM).

### 9. Footer
Version V5, source attribution, and a short "如流程有更新，請以 Notion 最新版本為準" note.

## UX / visual direction
- Professional EdTech, exam-prep credibility. Not childish, not corporate-grey.
- Dark-on-light default with a **dark mode toggle** persisted to `localStorage`.
- A restrained accent palette; use colour semantically (owner roles, pre/in/post zones, difficulty levels) rather than decoratively. Ensure WCAG AA contrast in both themes.
- Smooth but fast transitions; respect `prefers-reduced-motion`.
- **Print stylesheet**: `@media print` should produce a clean, expanded, single-flow document (all accordions/tabs open, nav and buttons hidden) so it can be printed as a physical desk reference.
- Keyboard accessible: real `<button>`/`<input>` elements, visible focus rings, ARIA on tabs/accordions/timeline.

## Quality bar
- No `console.error` on load; no broken interactions.
- Verbatim fidelity of all Chinese operational content — **do not invent, translate away, or drop any script, module, or checklist row**. Cross-check every item in the source markdown appears in the output.
- Clean, commented-where-necessary code. Reasonable file size (aim under ~250KB).
