# -*- coding: utf-8 -*-
import os, time, random, threading, sys, tempfile
from concurrent.futures import ThreadPoolExecutor
from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.chrome.options import Options

# --- ⚡ MEGA-STRIKE CONFIG ---
THREADS = 4  # 4 Agents per Machine (5 Machines total = 20 Agents)
STRIKE_DELAY = 0.1 
TARGET_ID = os.environ.get("TARGET_THREAD_ID", "2859755064232019")
MACHINE_ID = os.environ.get("MACHINE_ID", "1")

def get_driver(agent_id):
    options = Options()
    options.page_load_strategy = 'eager' # ⚡ FAST LOAD
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=800,600")
    
    # Unique profile per agent + machine
    temp_dir = os.path.join(tempfile.gettempdir(), f"pv_v103_m{MACHINE_ID}_a{agent_id}")
    options.add_argument(f"--user-data-dir={temp_dir}")
    
    driver = webdriver.Chrome(options=options)
    driver.set_page_load_timeout(25) # Stop hanging
    stealth(driver, languages=["en-US"], vendor="Google Inc.", platform="Win32", fix_hairline=True)
    return driver

def v103_hyper_force(driver, text):
    try:
        entropy = f"{random.randint(100,999)}"
        driver.execute_script("""
            const box = document.querySelector('div[role="textbox"]');
            if (box) {
                const nativeSetter = Object.getOwnPropertyDescriptor(window.HTMLElement.prototype, 'innerText').set;
                nativeSetter.call(box, arguments[0] + " " + arguments[1]);
                box.dispatchEvent(new Event('input', { bubbles: true }));
                
                const sendBtn = Array.from(document.querySelectorAll('button')).find(el => el.innerText === 'Send');
                if (sendBtn) { sendBtn.removeAttribute('disabled'); sendBtn.click(); }
                else { box.dispatchEvent(new KeyboardEvent('keydown', {key: 'Enter', bubbles: true})); }
            }
        """, text, entropy)
        return True
    except: return False

def run_agent(agent_id, cookie, text):
    # Staggered boot-up to prevent API rate limits
    time.sleep(agent_id * 5) 
    while True:
        driver = None
        try:
            driver = get_driver(agent_id)
            driver.get("https://www.instagram.com/")
            time.sleep(5)
            driver.add_cookie({'name': 'sessionid', 'value': cookie.strip(), 'domain': '.instagram.com'})
            driver.get(f"https://www.instagram.com/direct/t/{TARGET_ID}/")
            
            print(f"✅ Machine {MACHINE_ID} | Agent {agent_id} ARMED", flush=True)
            time.sleep(15)

            while True:
                if v103_hyper_force(driver, text):
                    sys.stdout.write(f"[M{MACHINE_ID}-A{agent_id}]")
                    sys.stdout.flush()
                time.sleep(STRIKE_DELAY)
        except: pass
        finally:
            if driver: driver.quit()
            time.sleep(5)

def main():
    cookie = os.environ.get("INSTA_COOKIE", "").strip()
    text = os.environ.get("MESSAGES", "V103_MEGA").strip()
    with ThreadPoolExecutor(max_workers=THREADS) as executor:
        for i in range(THREADS):
            executor.submit(run_agent, i+1, cookie, text)

if __name__ == "__main__":
    main()
