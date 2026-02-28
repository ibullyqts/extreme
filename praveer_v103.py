# -*- coding: utf-8 -*-
import os, time, random, threading, sys, tempfile
from concurrent.futures import ThreadPoolExecutor
from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.chrome.options import Options

# --- ⚡ V103 HYPER-FORCE CONFIG ---
THREADS = 8 
STRIKE_DELAY = 0.1  # 100ms
TARGET_ID = os.environ.get("TARGET_THREAD_ID", "2859755064232019")

def get_driver(agent_id):
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1280,720")
    
    temp_dir = os.path.join(tempfile.gettempdir(), f"pv_v103_final_{agent_id}")
    options.add_argument(f"--user-data-dir={temp_dir}")
    
    driver = webdriver.Chrome(options=options)
    stealth(driver, languages=["en-US"], vendor="Google Inc.", platform="Win32", fix_hairline=True)
    return driver

def v103_hyper_force(driver, text):
    """DOM Bypass + Send Button Force-Click."""
    try:
        entropy = f"{random.randint(100,999)}"
        driver.execute_script("""
            const box = document.querySelector('div[role="textbox"]');
            const msg = arguments[0] + " " + arguments[1];
            
            if (box) {
                box.focus();
                // 1. React State Force-Sync
                const nativeSetter = Object.getOwnPropertyDescriptor(window.HTMLElement.prototype, 'innerText').set;
                nativeSetter.call(box, msg);
                box.dispatchEvent(new Event('input', { bubbles: true }));

                // 2. Backup: Find and Click Send Button
                const sendBtn = Array.from(document.querySelectorAll('button, div[role="button"]'))
                                     .find(el => el.textContent === 'Send' || el.innerText === 'Send');
                
                if (sendBtn) {
                    sendBtn.removeAttribute('disabled');
                    sendBtn.click();
                } else {
                    // 3. Fallback: Keyboard Dispatch
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
    time.sleep(agent_id * 3) # Staggered startup to prevent RAM spikes
    while True:
        driver = None
        try:
            driver = get_driver(agent_id)
            driver.get("https://www.instagram.com/")
            time.sleep(5)
            driver.add_cookie({'name': 'sessionid', 'value': cookie.strip(), 'domain': '.instagram.com'})
            
            driver.get(f"https://www.instagram.com/direct/t/{TARGET_ID}/")
            print(f"🚀 Agent {agent_id} ARMED", flush=True)
            time.sleep(15) # Handshake for Lexical/React UI

            while True:
                if v103_hyper_force(driver, text):
                    sys.stdout.write(f"[{agent_id}]")
                    sys.stdout.flush()
                time.sleep(STRIKE_DELAY)
        except:
            pass
        finally:
            if driver:
                try: driver.quit()
                except: pass
            time.sleep(5)

def main():
    cookie = os.environ.get("INSTA_COOKIE", "").strip()
    text = os.environ.get("MESSAGES", "V103_FINAL").strip()
    
    with ThreadPoolExecutor(max_workers=THREADS) as executor:
        for i in range(THREADS):
            executor.submit(run_agent, i+1, cookie, text)

if __name__ == "__main__":
    main()
