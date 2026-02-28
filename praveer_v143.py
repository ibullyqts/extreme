# -*- coding: utf-8 -*-
# 🚀 PROJECT: PRAVEER.OWNS (V144 GHOST-PATCH)
# 📅 STATUS: ANTI-DETECTION | STEALTH-LOG | 4-8 AGENTS

import os, time, sys, base64, threading, random
from concurrent.futures import ThreadPoolExecutor
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# --- ⚡ V144 STEALTH CONFIG ---
THREADS_PER_MACHINE = 4            
BASE_DELAY_MS = 90                 
RECOVERY_RANGE = (1.5, 3.0)        
PURGE_INTERVAL_SEC = 900           
ENTRY_STAGGER = 8.5                # 🛡️ Increased slightly to prevent "Instant Logout"

def get_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new") 
    chrome_options.add_argument("--no-sandbox") 
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    # 🕵️ CRITICAL STEALTH ARGUMENTS (Hiding Selenium)
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    ua_list = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    ]
    chrome_options.add_argument(f"--user-agent={random.choice(ua_list)}")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    # 👻 Masking WebDriver Property in JS
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            })
        """
    })
    return driver

def v144_dispatch(driver, b64_text, delay):
    driver.execute_script("""
        window.praveer_active = true;
        window.msg_count = 0;
        const rawText = atob(arguments[0]);

        async function fire(msg, ms) {
            const getBox = () => document.querySelector('div[role="textbox"], textarea, [contenteditable="true"]');
            
            while(window.praveer_active) {
                let burstLimit = 8 + Math.floor(Math.random() * 7); 
                
                for(let i=0; i < burstLimit; i++) {
                    const box = getBox();
                    if (box) {
                        box.focus();
                        const salt = Math.random().toString(36).substring(5);
                        document.execCommand('insertText', false, msg + "\\n" + salt);
                        box.dispatchEvent(new Event('input', { bubbles: true }));
                        
                        let btn = [...document.querySelectorAll('div[role="button"], button')].find(b => b.innerText === 'Send' || b.textContent === 'Send');
                        if (btn) btn.click();
                        else box.dispatchEvent(new KeyboardEvent('keydown', {key: 'Enter', code: 'Enter', keyCode: 13, bubbles: true}));
                        
                        window.msg_count++;
                        await new Promise(r => setTimeout(r, ms + Math.floor(Math.random() * 25)));
                    }
                }
                // 🛑 Stealth Recovery
                await new Promise(r => setTimeout(r, 1500 + Math.random() * 1500));
            }
        }
        fire(rawText, arguments[1]);
    """, b64_text, delay)

def run_agent(agent_id, machine_id, cookie, target, b64_text):
    time.sleep(agent_id * ENTRY_STAGGER) 
    while True:
        driver = None
        try:
            driver = get_driver()
            driver.get("https://www.instagram.com/")
            time.sleep(12) 
            driver.add_cookie({'name': 'sessionid', 'value': cookie.strip(), 'path': '/', 'domain': '.instagram.com'})
            driver.refresh() # Force refresh to apply cookie stealthily
            time.sleep(10)
            
            driver.get(f"https://www.instagram.com/direct/t/{target}/")
            time.sleep(15)
            
            if "login" in driver.current_url: 
                print(f"❌ [M{machine_id}-A{agent_id}] LOGOUT DETECTED. Stopping Agent.")
                return 

            v144_dispatch(driver, b64_text, BASE_DELAY_MS)

            start = time.time()
            while (time.time() - start) < PURGE_INTERVAL_SEC:
                time.sleep(30)
                try: 
                    c = driver.execute_script("return window.msg_count;")
                    print(f"💓 [M{machine_id}-A{agent_id}] Ghost-Active: {c}")
                    sys.stdout.flush()
                except: break
        except Exception as e:
            print(f"⚠️ Error in Agent {agent_id}: {e}")
        finally:
            if driver: driver.quit()
            time.sleep(30)

def main():
    cookie = os.environ.get("INSTA_COOKIE", "").strip()
    target = os.environ.get("TARGET_THREAD_ID", "").strip()
    raw_messages = os.environ.get("MESSAGES", "").strip()
    b64_messages = base64.b64encode(raw_messages.encode('utf-8')).decode('utf-8')
    machine_id = os.environ.get("MACHINE_ID", "1")
    
    with ThreadPoolExecutor(max_workers=THREADS_PER_MACHINE) as executor:
        for i in range(THREADS_PER_MACHINE):
            executor.submit(run_agent, i+1, machine_id, cookie, target, b64_messages)
            time.sleep(5) # Local pool stagger

if __name__ == "__main__":
    main()
