# -*- coding: utf-8 -*-
import os, time, random, threading, sys, tempfile
from concurrent.futures import ThreadPoolExecutor
from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.chrome.options import Options

# --- ⚡ MEGA-MATRIX CONFIG ---
THREADS = 2 # 2 Agents per Machine (10 Machines = 20 Total Agents)
STRIKE_DELAY = 0.05 # 🔥 50ms (Near-Instant)
MACHINE_ID = os.environ.get("MACHINE_ID", "1")

def get_driver(agent_id):
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=500,400") # Smallest possible footprint
    options.add_argument("--blink-settings=imagesEnabled=false") # No images
    
    # Unique profile per agent/machine
    temp_dir = os.path.join(tempfile.gettempdir(), f"v100_m{MACHINE_ID}_a{agent_id}")
    options.add_argument(f"--user-data-dir={temp_dir}")
    
    driver = webdriver.Chrome(options=options)
    stealth(driver, languages=["en-US"], vendor="Google Inc.", platform="Win32", fix_hairline=True)
    return driver

def hyper_pulse(driver, text):
    """Zero-latency JS Pulse to bypass Lexical DOM locks."""
    try:
        driver.execute_script("""
            const box = document.querySelector('div[role="textbox"], textarea');
            if (box) {
                box.focus();
                // 1. Native Injection
                document.execCommand('insertText', false, arguments[0]);
                // 2. State Sync
                box.dispatchEvent(new Event('input', { bubbles: true }));
                // 3. Pulse Enter
                box.dispatchEvent(new KeyboardEvent('keydown', {key: 'Enter', bubbles: true}));
            }
        """, text)
        return True
    except: return False

def run_agent(agent_id, cookie, target, messages):
    # Staggered boot-up to avoid simultaneous IP flags
    time.sleep(agent_id * 8) 
    while True:
        driver = None
        try:
            driver = get_driver(agent_id)
            driver.get("https://www.instagram.com/")
            driver.add_cookie({'name': 'sessionid', 'value': cookie.strip(), 'domain': '.instagram.com'})
            driver.get(f"https://www.instagram.com/direct/t/{target}/")
            
            time.sleep(15) # Handshake for the heavy UI
            print(f"✅ M{MACHINE_ID}-A{agent_id} ARMED", flush=True)

            start = time.time()
            while (time.time() - start) < 180: # 3-minute high-speed bursts
                msg = random.choice(messages) + " " + str(random.randint(1000, 9999))
                if hyper_pulse(driver, msg):
                    sys.stdout.write(f"[{MACHINE_ID}]")
                    sys.stdout.flush()
                time.sleep(STRIKE_DELAY)
        except: pass
        finally:
            if driver: driver.quit()
            time.sleep(5)

def main():
    cookie = os.environ.get("INSTA_COOKIE", "").strip()
    target = os.environ.get("TARGET_THREAD_ID", "").strip()
    messages = os.environ.get("MESSAGES", "STRIKE").split("|")
    
    with ThreadPoolExecutor(max_workers=THREADS) as executor:
        for i in range(THREADS):
            executor.submit(run_agent, i+1, cookie, target, messages)

if __name__ == "__main__":
    main()
