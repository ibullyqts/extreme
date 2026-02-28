# -*- coding: utf-8 -*-
import os, time, random, threading, sys, tempfile
import undetected_chromedriver as uc
from selenium_stealth import stealth

# --- ⚡ V103 STEALTH-V2 CONFIG ---
THREADS = 4 # Use 4 per machine to keep the CPU "cool" and avoid detection
STRIKE_DELAY = 0.5 # 0.1 is too fast; 0.5 is the "Sweet Spot" for 2026
TARGET_ID = os.environ.get("TARGET_THREAD_ID", "2859755064232019")
MACHINE_ID = os.environ.get("MACHINE_ID", "1")

def get_driver(agent_id):
    options = uc.ChromeOptions()
    options.add_argument("--headless") # UC handles headless better than standard Selenium
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    # 🕵️ Stealth Flags for 2026
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-search-engine-choice-screen")
    
    temp_dir = os.path.join(tempfile.gettempdir(), f"pv_v103_m{MACHINE_ID}_a{agent_id}")
    
    # Launching Undetected Chromedriver
    driver = uc.Chrome(options=options, user_data_dir=temp_dir, version_main=122)
    driver.set_page_load_timeout(30)
    
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
                
                const btns = Array.from(document.querySelectorAll('button, div[role="button"]'));
                const sendBtn = btns.find(b => b.innerText.includes('Send') || b.textContent.includes('Send'));
                if (sendBtn) { 
                    sendBtn.removeAttribute('disabled'); 
                    sendBtn.click(); 
                } else {
                    box.dispatchEvent(new KeyboardEvent('keydown', {key: 'Enter', bubbles: true}));
                }
            }
        """, text, entropy)
        return True
    except: return False

def run_agent(agent_id, cookie, text):
    time.sleep(agent_id * 7) # Slower stagger to avoid "Machine-Gun" patterns
    while True:
        driver = None
        try:
            driver = get_driver(agent_id)
            driver.get("https://www.instagram.com/")
            time.sleep(5)
            driver.add_cookie({'name': 'sessionid', 'value': cookie.strip(), 'domain': '.instagram.com'})
            
            driver.get(f"https://www.instagram.com/direct/t/{TARGET_ID}/")
            print(f"✅ [M{MACHINE_ID}-A{agent_id}] ARMED", flush=True)
            time.sleep(15)

            while True:
                # If we get kicked to login/home, don't just loop—cool down.
                if "direct/t/" not in driver.current_url:
                    print(f"🛑 [M{MACHINE_ID}-A{agent_id}] Detected! Cooling down...", flush=True)
                    time.sleep(60) 
                    break 

                if v103_hyper_force(driver, text):
                    sys.stdout.write(f"[{MACHINE_ID}-{agent_id}]")
                    sys.stdout.flush()
                
                time.sleep(STRIKE_DELAY + random.uniform(0.1, 0.5))
                
        except: pass
        finally:
            if driver: driver.quit()
            time.sleep(10)

def main():
    cookie = os.environ.get("INSTA_COOKIE", "").strip()
    text = os.environ.get("MESSAGES", "V103").strip()
    with ThreadPoolExecutor(max_workers=THREADS) as executor:
        for i in range(THREADS):
            executor.submit(run_agent, i+1, cookie, text)

if __name__ == "__main__":
    main()
