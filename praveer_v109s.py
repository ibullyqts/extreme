import os, time, random, threading, sys, gc, tempfile
from concurrent.futures import ThreadPoolExecutor
from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# --- ⚡ RECOVERY CONFIG ---
THREADS = 2 # Reduced to 2 for stable recovery on GitHub Runners
BURST_SPEED = (0.5, 1.2) 
SESSION_RESTART_SEC = 600 # Restart browser every 10 mins to clear RAM

def get_driver(agent_id, machine_id):
    options = Options()
    options.add_argument("--headless=new") 
    options.add_argument("--no-sandbox") 
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    
    # Randomize minor UA version for entropy
    ua = f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/12{random.randint(1,4)}.0.0.0 Safari/537.36"
    options.add_argument(f"user-agent={ua}")
    
    driver = webdriver.Chrome(options=options)
    stealth(driver, languages=["en-US"], vendor="Google Inc.", platform="Win32", fix_hairline=True)
    return driver

def run_life_cycle(agent_id, machine_id, cookie, target, custom_text):
    print(f"🚀 [Agent {agent_id}] Engine Initialized.", flush=True)
    
    while True: # 🛡️ INFINITE RECOVERY LOOP
        driver = None
        try:
            driver = get_driver(agent_id, machine_id)
            driver.get("https://www.instagram.com/")
            
            # Inject session
            driver.add_cookie({'name': 'sessionid', 'value': cookie.strip(), 'path': '/', 'domain': '.instagram.com'})
            driver.get(f"https://www.instagram.com/direct/t/{target}/")
            
            time.sleep(10) # Handshake
            
            session_start = time.time()
            # Run for a set duration, then restart to prevent memory bloat
            while (time.time() - session_start) < SESSION_RESTART_SEC:
                # JS Triple-Tap execution
                entropy = [f"{random.randint(100,999)}" for _ in range(3)]
                driver.execute_script("""
                    var box = document.querySelector('div[role="textbox"], textarea');
                    if (box) {
                        arguments[1].forEach(salt => {
                            box.focus();
                            document.execCommand('insertText', false, arguments[0] + " " + salt);
                            box.dispatchEvent(new KeyboardEvent('keydown', {key: 'Enter', code: 'Enter', keyCode: 13, which: 13, bubbles: true}));
                        });
                    }
                """, custom_text, entropy)
                
                sys.stdout.write(f" {agent_id}⚡")
                sys.stdout.flush()
                time.sleep(random.uniform(*BURST_SPEED))
                
        except Exception as e:
            print(f"\n⚠️ [Agent {agent_id}] Crash Detected. Auto-restarting in 10s...", flush=True)
        finally:
            if driver:
                try: driver.quit()
                except: pass
            gc.collect() # Force Python to clear memory
            time.sleep(10) # Cooling period

def main():
    cookie = os.environ.get("INSTA_COOKIE", "").strip()
    target = os.environ.get("TARGET_THREAD_ID", "").strip()
    text = os.environ.get("MESSAGES", "V109 ACTIVE")
    
    with ThreadPoolExecutor(max_workers=THREADS) as executor:
        for i in range(THREADS):
            executor.submit(run_life_cycle, i+1, "1", cookie, target, text)

if __name__ == "__main__":
    main()
