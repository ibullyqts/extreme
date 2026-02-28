const axios = require('axios');

// --- ⚡ LOAD ENVIRONMENT SECRETS ---
const COOKIE = process.env.INSTA_COOKIE;
const THREAD_ID = process.env.TARGET_THREAD_ID;
const MESSAGE_BODY = process.env.MESSAGES;

/**
 * 🔥 AUTO-EXTRACT CSRF
 * Searches the cookie string for the 'csrftoken' value required for the POST handshake.
 */
function getCsrf(cookieString) {
    if (!cookieString) return null;
    const match = cookieString.match(/csrftoken=([^;]+)/);
    return match ? match[1] : null;
}

async function sendStrike(agentId) {
    const csrftoken = getCsrf(COOKIE);
    
    if (!csrftoken) {
        console.log(`❌ [Agent ${agentId}] FATAL: csrftoken not found in INSTA_COOKIE secret.`);
        return;
    }

    console.log(`🛡️ [Agent ${agentId}] Handshake Ready. CSRF: ${csrftoken.substring(0, 6)}...`);

    const config = {
        method: 'post',
        url: `https://www.instagram.com/api/v1/direct_messages/threads/${THREAD_ID}/send_item/`,
        headers: {
            'cookie': COOKIE,
            'x-csrftoken': csrftoken,
            'content-type': 'application/x-www-form-urlencoded',
            'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Mobile/15E148 Safari/604.1',
            'x-requested-with': 'XMLHttpRequest',
            'referer': `https://www.instagram.com/direct/t/${THREAD_ID}/`,
            'origin': 'https://www.instagram.com'
        }
    };

    while (true) {
        try {
            // Adds a unique timestamp and random salt to prevent server-side message merging
            const salt = Math.random().toString(36).substring(2, 10);
            const data = `text=${encodeURIComponent(MESSAGE_BODY + " " + salt)}&client_context=${Date.now()}`;
            
            await axios({ ...config, data });
            process.stdout.write(`✅ [Agent ${agentId}] Strike Delivered\r`);
            
        } catch (error) {
            if (error.response) {
                const status = error.response.status;
                if (status === 429) {
                    // 🛡️ SMART-WAIT: Backs off for 5-7 seconds when rate-limited
                    const waitTime = 5000 + Math.random() * 2000;
                    console.log(`\n⚠️ [Agent ${agentId}] Rate Limited (429). Sleeping ${Math.round(waitTime/1000)}s...`);
                    await new Promise(r => setTimeout(r, waitTime));
                } else if (status === 403) {
                    console.log(`\n🚫 [Agent ${agentId}] Forbidden (403). CSRF or Session expired.`);
                    process.exit(1);
                } else {
                    console.log(`\n⚠️ [Agent ${agentId}] Error ${status}: ${error.message}`);
                }
            } else {
                console.log(`\n📡 [Agent ${agentId}] Connection Issue: ${error.message}`);
            }
            // Brief pause before retry on general errors
            await new Promise(r => setTimeout(r, 3000));
        }
        
        // Constant pressure with small randomized jitter
        await new Promise(r => setTimeout(r, 45 + Math.random() * 20));
    }
}

// 💥 Initialize 8 parallel agents per GitHub machine
for (let i = 1; i <= 8; i++) {
    sendStrike(i);
}
