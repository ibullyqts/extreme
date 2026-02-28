# -*- coding: utf-8 -*-
# 🚀 PROJECT: PRAVEER.OWNS (V103 MEGA-FORCE)
# 📅 STATUS: MULTI-MACHINE ACTIVE | HYPER-LOCK ENABLED

import os, time, random, threading, sys, tempfile
from concurrent.futures import ThreadPoolExecutor
from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.chrome.options import Options

# --- ⚡ MEGA-FORCE CONFIG ---
THREADS = 4  # 4 Agents per Machine (e.g., 5 Machines = 20 Agents)
STRIKE_DELAY = 0.1 
TARGET_ID = os.environ.get("TARGET_THREAD_ID", "2859755064232019")
MACHINE_ID = os.environ.get("MACHINE_ID", "1")

def get_driver(agent_id):
    options = Options()
    options.page_load_strategy = 'eager' # ⚡ Skip heavy trackers to stop hanging
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1280,720")
    
    # 🔥 Anti-Detection & Memory Optimization
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-extensions")
    
    # Unique profile per agent per machine
    temp_dir = os.path.join(tempfile.gettempdir(), f"pv_v103_m{MACHINE_ID}_a{agent_id}")
    options.add_argument(f"--user-data-dir={temp_dir}")
    
    driver = webdriver.Chrome(options=options)
    driver.set_page_load_timeout(25) 
    
    stealth(driver, languages=["en-US"], vendor="Google Inc.", platform="Win32", fix_hairline=True)
    return driver

def v103_hyper_force(driver, text):
    """Bypasses React DOM and force-clicks the Send button."""
    try:
        entropy = f"{random.randint(100,999)}"
        driver.execute_script("""
            const box = document.querySelector('div[role="textbox"]');
            const msg = arguments[0] + " " + arguments[1];
            
            if (box) {
                box.focus();
                // 1. Force React State Sync via Native Setter
                const nativeSetter = Object.getOwnPropertyDescriptor(window.HTMLElement.prototype, 'innerText').set;
                nativeSetter.call(box, msg);
                box.dispatchEvent(new Event('input', { bubbles: true }));

                // 2. Locate Send Button (Lexical/React 2026 Path)
                const sendBtn = Array.from(document.querySelectorAll('button, div[role="button"]'))
                                     .find(el => el.textContent === 'Send' || el.innerText === 'Send');
                
                if (sendBtn) {
                    sendBtn.removeAttribute('disabled');
                    sendBtn.click();
                } else {
                    // 3. Fallback: Keyboard Dispatch if button is hidden
                    box.dispatchEvent(new KeyboardEvent('keydown', {
                        key: 'Enter', code: 'Enter', keyCode: 13, which: 13, bubbles: true
                    }));
                }
            }
        """, text, entropy)
        return True
    except:
        return False

def run_agent(agent_id, cookie, text):
    # 🛡️ Staggered Launch (Prevents RAM spikes & 429 blocks)
    time.sleep(agent_id * 5) 
    
    while True:
        driver = None
        try:
            driver = get_driver(agent_id)
            driver.get("https://www.instagram.com/")
            time.sleep(5)
            
            driver.add_cookie({'name': 'sessionid', 'value': cookie.strip(), 'domain': '.instagram.com'})
            driver.get(f"https://www.instagram.com/direct/t/{TARGET_ID}/")
            
            # 🔒 NAVIGATION LOCK: Stop the "Reloading" loop
            driver.execute_script("""
                window.onbeforeunload = function() { return false; };
                window.location.reload = function() { console.log('Reload Blocked'); };
                history.pushState(null, null, window.location.href);
            """)
            
            print(f"✅ [M{MACHINE_ID}-A{agent_id}] ARMED & LOCKED", flush=True)
            time.sleep(12) # Wait for Lexical Engine handshake

            while True:
                # Redirect Check: If we get kicked to Login/Home, restart.
                if "direct/t/" not in driver.current_url:
                    print(f"⚠️ Agent {agent_id} Redirected. Restarting...", flush=True)
                    break 

                if v103_hyper_force(driver, text):
                    sys.stdout.write(f"[{MACHINE_ID}-{agent_id}]")
                    sys.stdout.flush()
                
                # Hyper-Strike Delay with tiny jitter to mimic human variation
                time.sleep(STRIKE_DELAY + random.uniform(0.01, 0.05))
                
        except Exception as e:
            pass 
        finally:
            if driver:
                try: driver.quit()
                except: pass
            time.sleep(5)

def main():
    cookie = os.environ.get("INSTA_COOKIE", "").strip()
    text = os.environ.get("MESSAGES", "V103_MEGA").strip()
    
    print(f"🔥 Machine {MACHINE_ID} Initializing {THREADS} Agents...", flush=True)
    with ThreadPoolExecutor(max_workers=THREADS) as executor:
        for i in range(THREADS):
            executor.submit(run_agent, i+1, cookie, text)

if __name__ == "__main__":
    main()
