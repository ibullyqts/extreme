# -*- coding: utf-8 -*-
import os, time, sys, base64, threading, random
from concurrent.futures import ThreadPoolExecutor
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# --- ⚡ STEALTH CONFIG ---
THREADS_PER_MACHINE = 4            
INTERNAL_DELAY_MS = 100            # Increased to 100ms for safety after lock
PURGE_INTERVAL_SEC = 900           
TARGET_NC_NAME = "CHAL BHANGI NC KR~"
SVG_PATH = "M12.001.504a11.5 11.5 0 1 0 11.5 11.5 11.513 11.513 0 0 0-11.5-11.5Zm-.182 5.955a1.25 1.25 0 1 1-1.25 1.25 1.25 1.25 0 0 1 1.25-1.25Zm1.614 11.318h-2.865a1 1 0 0 1 0-2H11V12.05h-.432a1 1 0 0 1 0-2H12a1 1 0 0 1 1 1v4.727h.433a1 1 0 1 1 0 2Z"

def get_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new") 
    chrome_options.add_argument("--no-sandbox") 
    chrome_options.add_argument("--disable-dev-shm-usage")
    ua_list = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 17_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1"
    ]
    chrome_options.add_argument(f"--user-agent={random.choice(ua_list)}")
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=chrome_options)

def v133_dispatch(driver, b64_text, delay, target_nc, path_data):
    driver.execute_script("""
        window.praveer_active = true;
        window.msg_count = 0;
        
        async function watchNC(targetName, dPath) {
            while(window.praveer_active) {
                try {
                    let currentNC = document.querySelector('header span[role="link"], header div[role="button"] span')?.innerText;
                    if (currentNC && !currentNC.includes(targetName)) {
                        await new Promise(r => setTimeout(r, Math.random() * 3000)); 
                        let allPaths = document.querySelectorAll('path');
                        let targetBtn = null;
                        for (let p of allPaths) {
                            if (p.getAttribute('d') === dPath) {
                                targetBtn = p.closest('button') || p.closest('div[role="button"]');
                                break;
                            }
                        }
                        if (targetBtn) {
                            targetBtn.click();
                            await new Promise(r => setTimeout(r, 1500));
                            let nameInput = document.querySelector('input[name="groupChatName"]');
                            if (nameInput) {
                                nameInput.focus();
                                document.execCommand('selectAll', false, null);
                                document.execCommand('insertText', false, targetName);
                                nameInput.dispatchEvent(new Event('input', { bubbles: true }));
                                nameInput.dispatchEvent(new KeyboardEvent('keydown', {key: 'Enter', code: 'Enter', keyCode: 13, bubbles: true}));
                            }
                            await new Promise(r => setTimeout(r, 1000));
                            document.querySelector('div[aria-label="Back"], svg[aria-label="Back"], div[aria-label="Close"]')?.parentElement.click();
                        }
                    }
                } catch(e) {}
                await new Promise(r => setTimeout(r, 15000 + Math.random() * 5000)); 
            }
        }

        async function fire(b64, ms) {
            const msg = atob(b64);
            const getBox = () => document.querySelector('div[role="textbox"], textarea, [contenteditable="true"]');
            while(window.praveer_active) {
                const box = getBox();
                if (box) {
                    box.focus();
                    document.execCommand('insertText', false, msg + "\\n" + Math.random().toString(36).substring(7));
                    box.dispatchEvent(new Event('input', { bubbles: true }));
                    let btn = [...document.querySelectorAll('div[role="button"], button')].find(b => b.innerText === 'Send' || b.textContent === 'Send');
                    if (btn) btn.click();
                    else box.dispatchEvent(new KeyboardEvent('keydown', {key: 'Enter', code: 'Enter', keyCode: 13, bubbles: true}));
                    window.msg_count++;
                }
                await new Promise(r => setTimeout(r, ms + Math.floor(Math.random() * 20)));
            }
        }
        watchNC(arguments[2], arguments[3]);
        fire(arguments[0], arguments[1]);
    """, b64_text, delay, target_nc, path_data)

def run_agent(agent_id, machine_id, cookie, target, b64_text):
    time.sleep(agent_id * 20)
    while True:
        driver = None
        try:
            driver = get_driver()
            driver.get("https://www.instagram.com/")
            time.sleep(10)
            driver.add_cookie({'name': 'sessionid', 'value': cookie.strip(), 'path': '/', 'domain': '.instagram.com'})
            driver.get(f"https://www.instagram.com/direct/t/{target}/")
            time.sleep(15)
            if "login" in driver.current_url: return 
            v133_dispatch(driver, b64_text, INTERNAL_DELAY_MS, TARGET_NC_NAME, SVG_PATH)
            start = time.time()
            while (time.time() - start) < PURGE_INTERVAL_SEC:
                time.sleep(30)
                try:
                    c = driver.execute_script("return window.msg_count;")
                    print(f"💓 [M{machine_id}-A{agent_id}] Active: {c}")
                    sys.stdout.flush()
                except: break
        except: pass
        finally:
            if driver: driver.quit()
            time.sleep(15)

def main():
    cookie = os.environ.get("INSTA_COOKIE", "").strip()
    target = os.environ.get("TARGET_THREAD_ID", "").strip()
    raw_text = os.environ.get("MESSAGES", "").strip()
    machine_id = os.environ.get("MACHINE_ID", "1")
    b64_text = base64.b64encode(raw_text.encode('utf-8')).decode('utf-8')
    with ThreadPoolExecutor(max_workers=THREADS_PER_MACHINE) as executor:
        for i in range(THREADS_PER_MACHINE):
            executor.submit(run_agent, i+1, machine_id, cookie, target, b64_text)
            time.sleep(15)

if __name__ == "__main__":
    main()
