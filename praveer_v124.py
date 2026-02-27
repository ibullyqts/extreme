# -*- coding: utf-8 -*-
# 🚀 PROJECT: PRAVEER.OWNS (V127 BLOCK-ANCHOR)
# 📅 STATUS: MULTI-LINE-LOCKED | V103-VELOCITY | 16-AGENTS

import os, time, random, sys, threading, base64, json
from concurrent.futures import ThreadPoolExecutor
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# --- ⚡ PERFORMANCE CONFIG ---
THREADS_PER_MACHINE = 4            
INTERNAL_DELAY_MS = 50             
PURGE_INTERVAL_SEC = 600 # 10-Min Reset

def get_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new") 
    chrome_options.add_argument("--no-sandbox") 
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--js-flags='--max-old-space-size=512'")
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=chrome_options)

def v127_block_dispatch(driver, raw_text, delay):
    # Pass the text as a JSON string to preserve all newlines perfectly
    driver.execute_script("""
        window.praveer_active = true;
        window.msg_count = 0;
        (async function fire(msgBlock, ms) {
            const getBox = () => document.querySelector('div[role="textbox"], textarea, [contenteditable="true"]');
            
            while(window.praveer_active) {
                const box = getBox();
                if (box) {
                    box.focus();
                    const salt = Math.random().toString(36).substring(7);
                    
                    // Force the entire block into the box at once
                    document.execCommand('insertText', false, msgBlock + "\\n\\u200B" + salt);
                    
                    // Trigger validation events
                    box.dispatchEvent(new Event('input', { bubbles: true }));
                    box.dispatchEvent(new KeyboardEvent('keyup', { key: ' ', bubbles: true }));

                    let btn = [...document.querySelectorAll('div[role="button"], button')].find(b => 
                        b.innerText === 'Send' || b.textContent === 'Send'
                    );

                    if (btn && !btn.disabled) {
                        btn.click();
                    } else {
                        box.dispatchEvent(new KeyboardEvent('keydown', {key: 'Enter', code: 'Enter', keyCode: 13, bubbles: true}));
                    }
                    window.msg_count++;
                }
                await new Promise(r => setTimeout(r, ms));
            }
        })(arguments[0], arguments[1]);
    """, raw_text, delay)

def run_agent(agent_id, machine_id, cookie, target, raw_text):
    while True:
        driver = None
        try:
            driver = get_driver()
            driver.get("https://www.instagram.com/")
            time.sleep(5)
            driver.add_cookie({'name': 'sessionid', 'value': cookie.strip(), 'path': '/', 'domain': '.instagram.com'})
            driver.get(f"https://www.instagram.com/direct/t/{target}/")
            time.sleep(15)
            v127_block_dispatch(driver, raw_text, INTERNAL_DELAY_MS)
            
            start = time.time()
            while (time.time() - start) < PURGE_INTERVAL_SEC:
                time.sleep(30)
                try:
                    c = driver.execute_script("return window.msg_count;")
                    print(f"💓 [M{machine_id}-A{agent_id}] Block Striking | Count: {c}")
                except: break
        except: pass
        finally:
            if driver: driver.quit()
            time.sleep(5)

def main():
    cookie = os.environ.get("INSTA_COOKIE", "").strip()
    target = os.environ.get("TARGET_THREAD_ID", "").strip()
    raw_text = os.environ.get("MESSAGES", "").strip()
    machine_id = os.environ.get("MACHINE_ID", "1")
    
    with ThreadPoolExecutor(max_workers=THREADS_PER_MACHINE) as executor:
        for i in range(THREADS_PER_MACHINE):
            executor.submit(run_agent, i+1, machine_id, cookie, target, raw_text)
            time.sleep(10)

if __name__ == "__main__":
    main()
