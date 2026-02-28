# -*- coding: utf-8 -*-
# 🚀 PROJECT: PRAVEER.OWNS (V109 TRIPLE-TAP)
# 📅 STATUS: TRIPLE-STRIKE-ACTIVE | 4-AGENTS PER MACHINE | ENTROPY-SHIELD

import os, time, re, random, datetime, threading, sys, gc, tempfile, subprocess, shutil
from concurrent.futures import ThreadPoolExecutor
from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# --- ⚡ TRIPLE-TAP CONFIG ---
THREADS = 4                        
TOTAL_DURATION = 21600             
# 🔥 STRIKE SPEED: 0.2-0.5s pause between TRIPLE-TAPS (Total 10+ msgs/sec per agent)
BURST_SPEED = (0.2, 0.5)           
SESSION_RESTART_SEC = 300          

GLOBAL_SENT = 0
COUNTER_LOCK = threading.Lock()
BROWSER_LAUNCH_LOCK = threading.Lock()

def get_driver(agent_id, machine_id):
    chrome_options = Options()
    chrome_options.add_argument("--headless=new") 
    chrome_options.add_argument("--no-sandbox") 
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    
    ua = f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/12{random.randint(1,4)}.0.0.0 Safari/537.36"
    chrome_options.add_argument(f"user-agent={ua}")
    
    temp_dir = os.path.join(tempfile.gettempdir(), f"pv_v109_{machine_id}_{agent_id}")
    chrome_options.add_argument(f"--user-data-dir={temp_dir}")
    driver = webdriver.Chrome(options=chrome_options)
    stealth(driver, languages=["en-US"], vendor="Google Inc.", platform="Win32", fix_hairline=True)
    driver.custom_temp_path = temp_dir
    return driver

def triple_tap_dispatch(driver, text):
    """Fires 3 unique messages in a single JS execution cycle."""
    try:
        # We pass 3 unique 'Entropy' strings to the JS worker
        entropy = [f"{random.randint(100,999)}", f"{random.randint(100,999)}", f"{random.randint(100,999)}"]
        
        driver.execute_script("""
            var box = document.querySelector('div[role="textbox"], textarea');
            var msg = arguments[0];
            var salts = arguments[1];
            
            if (box) {
                salts.forEach(salt => {
                    box.focus();
                    // Inject text + invisible bit for safety
                    document.execCommand('insertText', false, msg + " \\u200B" + salt);
                    
                    var e = new KeyboardEvent('keydown', {
                        key: 'Enter', code: 'Enter', keyCode: 13, which: 13, 
                        bubbles: true, cancelable: true
                    });
                    box.dispatchEvent(e);
                });
            }
        """, text, entropy)
        return True
    except: return False

def run_life_cycle(agent_id, machine_id, cookie, target, custom_text):
    global_start = time.time()
    while (time.time() - global_start) < TOTAL_DURATION:
        driver = None
        try:
            driver = get_driver(agent_id, machine_id)
            driver.get("https://www.instagram.com/")
            
            # 🛡️ SAFETY STAGGER: Wait before injecting cookie
            login_delay = (int(agent_id) * 8) + (int(machine_id) * 15) - 20
            time.sleep(max(5, login_delay))
            
            driver.add_cookie({'name': 'sessionid', 'value': cookie.strip(), 'path': '/', 'domain': '.instagram.com'})
            driver.get(f"https://www.instagram.com/direct/t/{target}/")
            time.sleep(12) # Full handshake
            
            session_start = time.time()
            while (time.time() - session_start) < SESSION_RESTART_SEC:
                if triple_tap_dispatch(driver, custom_text):
                    with COUNTER_LOCK:
                        global GLOBAL_SENT
                        GLOBAL_SENT += 3 # Count 3 per strike
                    sys.stdout.write("🚀")
                    sys.stdout.flush()
                
                time.sleep(random.uniform(*BURST_SPEED))
        except: pass
        finally:
            if driver: driver.quit()
            time.sleep(10)

def main():
    cookie = os.environ.get("INSTA_COOKIE", "").strip()
    target = os.environ.get("TARGET_THREAD_ID", "").strip()
    custom_text = os.environ.get("MESSAGES", "V109 TRIPLE").strip()
    machine_id = os.environ.get("MACHINE_ID", "1")
    
    with ThreadPoolExecutor(max_workers=THREADS) as executor:
        for i in range(THREADS):
            executor.submit(run_life_cycle, i+1, machine_id, cookie, target, custom_text)

if __name__ == "__main__":
    main()
