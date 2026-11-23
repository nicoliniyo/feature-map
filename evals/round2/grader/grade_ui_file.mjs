import { chromium } from "playwright-core";

import { resolve } from "node:path"; const dir = resolve(process.argv[2]);


const b = await chromium.launch({ executablePath: process.env.CHROME_PATH || "/usr/bin/google-chrome", headless: true });
const res = {};
try {
  const p = await b.newPage({ viewport: { width: 1280, height: 720 } });
  await p.goto(`file://${dir}/index.html#/settings`);
  await p.selectOption("#digest", "daily");
  try { await p.click("#settings-save", { timeout: 2500 }); res["Save clickable"] = true; } catch { res["Save clickable"] = false; }
  res["toast shown"] = await p.getByRole("status").filter({ hasText: "Settings saved" }).isVisible().catch(() => false);
  res["setting persisted"] = (await p.evaluate(() => localStorage.getItem("settings")) || "").includes("daily");
  const mp = await b.newPage({ viewport: { width: 390, height: 700 } });
  await mp.goto(`file://${dir}/index.html#/profile`);
  try { await mp.click("#profile-save", { timeout: 2500 }); res["mobile profile clickable"] = true; } catch { res["mobile profile clickable"] = false; }
  res["profile toast"] = await mp.getByRole("status").filter({ hasText: "Profile updated" }).isVisible().catch(() => false);
} finally { await b.close(); }
console.log(JSON.stringify(res, null, 1)); console.log(Object.values(res).every(Boolean) ? "PASS" : "FAIL");
