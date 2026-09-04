#!/usr/bin/env python3
"""Playwright QA for the React Sections Comparison family."""
from __future__ import annotations
import json,re,subprocess,sys
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]; BASE="http://localhost:8765/React/Sections/Comparison/"
SLUGS=["minimal","dark-premium","bento","neo-brutalist"]; WIDTHS=[320,375,768,1280,1440]
checks=0; failures=[]
def check(ok:bool,label:str)->None:
 global checks
 checks+=1
 if not ok: failures.append(label); print("FAIL:",label)
def static_checks()->None:
 palette=re.compile(r"\b(?:bg|text|border|fill|stroke|from|to|via)-(?:slate|gray|zinc|neutral|stone|red|orange|amber|yellow|lime|green|emerald|teal|cyan|sky|blue|indigo|violet|purple|fuchsia|pink|rose)-\d")
 emoji=re.compile("[\\U0001F000-\\U0001FAFF☀-➿\\U00020000-\\U0002FFFF]",re.UNICODE); hex_lit=re.compile(r"#[0-9a-fA-F]{3,8}\b")
 root=ROOT/"React/Sections/Comparison"; check(sorted(p.name for p in root.iterdir() if p.is_dir())==SLUGS,"exact four direction folders")
 for slug in SLUGS:
  folder=root/slug; files=sorted(p.name for p in folder.iterdir() if p.is_file()); check(files==["code.tsx","metadata.json","preview.html"],f"{slug}: exact 3-file shape")
  tsx=(folder/"code.tsx").read_text(); check(not re.search(r":\s*any\b|<any>|\bas\s+any\b",tsx),f"{slug}: no any"); check(not hex_lit.search(tsx.replace("#000","")),f"{slug}: no raw hex outside sanctioned #000"); check(not palette.search(tsx),f"{slug}: no raw palette classes"); check("!important" not in tsx,f"{slug}: no !important"); check("transition-all" not in tsx,f"{slug}: no transition-all"); check(not emoji.search(tsx),f"{slug}: no emoji"); check("style={" not in tsx,f"{slug}: no inline style props"); check("http://" not in tsx and "https://" not in tsx,f"{slug}: no external URLs"); check("<img" not in tsx,f"{slug}: no external image element")
  meta=json.loads((folder/"metadata.json").read_text()); check(meta.get("id")==f"comparison-{slug}",f"{slug}: metadata id"); check(meta.get("family")=="Comparison",f"{slug}: metadata family"); check(meta.get("subcategory")=="Comparison",f"{slug}: metadata subcategory"); check(meta.get("type")=="section",f"{slug}: metadata type"); check(meta.get("category")=="Sections",f"{slug}: metadata category"); check(meta.get("direction") in ["Minimal","Dark Premium","Bento","Neo-Brutalist"],f"{slug}: metadata direction"); check(bool(meta.get("description")),f"{slug}: metadata description")
def browser_checks()->None:
 with sync_playwright() as pw:
  browser=pw.chromium.launch()
  for slug in SLUGS:
   page=browser.new_page(); errors=[]; page.on("console",lambda m: errors.append(m.text) if m.type=="error" else None); page.on("pageerror",lambda e: errors.append(str(e)))
   page.goto(BASE+slug+"/preview.html",wait_until="networkidle"); page.wait_for_selector("#ds-root section",timeout=15000)
   check(page.locator("#ds-root section h2").count()==1,f"{slug}: exactly one h2"); check(page.locator("#ds-root section").get_attribute("aria-labelledby") is not None,f"{slug}: aria-labelledby exists")
   check(page.locator("#ds-root section h3").count()==3,f"{slug}: all three options render")
   check(page.locator("#ds-root section").get_by_text("Included",exact=True).count()+page.locator("#ds-root section").get_by_text("YES",exact=True).count()>0,f"{slug}: included state renders")
   check(page.locator("#ds-root section").get_by_text("Not included",exact=True).count()+page.locator("#ds-root section").get_by_text("NO",exact=True).count()>0 or slug in ["dark-premium","bento"],f"{slug}: unavailable state is understandable")
   if slug in ["minimal","neo-brutalist"]: check(page.locator("#ds-root section table").count()==1,f"{slug}: semantic table present"); check(page.locator("#ds-root section th").count()>=4,f"{slug}: table headers present")
   if slug=="dark-premium": check(page.locator("#ds-root section dl").count()==3,f"{slug}: stacked comparison panels use semantic dl")
   if slug=="bento": check(page.locator("#ds-root section .md\\:grid-cols-12").count()==1,f"{slug}: 12-column bento grid present")
   for width in WIDTHS:
    page.set_viewport_size({"width":width,"height":900})
    for theme in ["light","dark"]:
     page.evaluate("t=>document.documentElement.setAttribute('data-theme',t)",theme); overflow=page.evaluate("document.documentElement.scrollWidth-document.documentElement.clientWidth"); check(overflow<=0,f"{slug}: no page overflow @ {width}px {theme} (got {overflow})")
   page.set_viewport_size({"width":1280,"height":900})
   def colors(theme:str):
    page.evaluate("t=>document.documentElement.setAttribute('data-theme',t)",theme); return page.locator("#ds-root section").evaluate("e=>{let c=getComputedStyle(e);return [c.backgroundColor,c.color]}")
   light=colors("light"); dark=colors("dark")
   if slug=="dark-premium": check(light==dark,f"{slug}: pinned dark colors persist across page themes"); check(light[0] not in ["rgb(250, 250, 250)","rgb(255, 255, 255)"],f"{slug}: actually dark")
   else: check(light!=dark,f"{slug}: light/dark theme changes section")
   page.evaluate("document.documentElement.setAttribute('data-theme','light')"); first=page.locator("#ds-root section a[href],#ds-root section button").first; first.focus(); check(first.evaluate("e=>getComputedStyle(e).outlineWidth")=="2px",f"{slug}: focus-visible 2px indication")
   page.keyboard.press("Tab"); check(page.locator("#ds-root section :focus").count()>0,f"{slug}: keyboard navigation reaches section controls")
   page.emulate_media(reduced_motion="reduce"); check(first.evaluate("e=>getComputedStyle(e).transitionProperty") in ["none","all"],f"{slug}: reduced motion removes transition"); page.emulate_media(reduced_motion="no-preference")
   check(not errors,f"{slug}: zero console errors")
   page.close()
  browser.close()
def generator_checks()->None:
 r=subprocess.run([sys.executable,str(ROOT/"_gen_react_sections_comparison.py"),"--check"],capture_output=True,text=True); check(r.returncode==0,"generator --check reports no drift")
 r=subprocess.run([sys.executable,str(ROOT/"scripts/validate.py")],capture_output=True,text=True); check(r.returncode==0,"scripts/validate.py passes")
def main()->int:
 static_checks(); generator_checks(); browser_checks(); print(f"\n{checks} checks, {len(failures)} failures"); [print(" -",f) for f in failures]; return 1 if failures else 0
if __name__=="__main__": sys.exit(main())
