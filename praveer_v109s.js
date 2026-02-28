const axios = require('axios');
const qs = require('qs');

const COOKIE = process.env.INSTA_COOKIE;
const THREAD_ID = process.env.TARGET_THREAD_ID;
const MESSAGE_BODY = process.env.MESSAGES;

function getCsrf(cookieString) {
    const match = cookieString.match(/csrftoken=([^;]+)/);
    return match ? match[1] : null;
}

async function sendStrike(agentId) {
    const csrftoken = getCsrf(COOKIE);
    if (!csrftoken) {
        console.log(`❌ Agent ${agentId}: CSRF Missing`);
        return;
    }

    const config = {
        method: 'post',
        // 🔥 Using the mobile direct broadcast endpoint
        url: 'https://i.instagram.com/api/v1/direct_v2/threads/broadcast/text/',
        headers: {
            'cookie': COOKIE,
            'x-csrftoken': csrftoken,
            'content-type': 'application/x-www-form-urlencoded',
            'user-agent': 'Instagram 150.0.0.0.0 (iPhone; iOS 14_4_1; en_US; en-US; scale=2.00; 750x1334) AppleWebKit/420+',
            'x-ig-app-id': '936619743392459',
            'x-requested-with': 'XMLHttpRequest'
        }
    };

    console.log(`🛡️ Agent ${agentId} Live - Targeting: ${THREAD_ID}`);

    while (true) {
        try {
            const ts = Date.now();
            const data = qs.stringify({
                'text': MESSAGE_BODY + " " + ts,
                'thread_ids': `[${THREAD_ID}]`,
                'client_context': ts,
                'offline_threading_id': ts
            });

            await axios({ ...config, data });
            process.stdout.write(`✅ [Agent ${agentId}] Hit\r`);
        } catch (e) {
            const status = e.response ? e.response.status : 'CONN_ERR';
            console.log(`\n⚠️ [Agent ${agentId}] Status: ${status}`);
            // If it's a 404, it means the Thread ID secret is definitely wrong
            if (status === 404) {
                console.log("❌ CRITICAL: Check your TARGET_THREAD_ID Secret!");
                process.exit(1);
            }
            await new Promise(r => setTimeout(r, 5000));
        }
        await new Promise(r => setTimeout(r, 60));
    }
}

for (let i = 1; i <= 8; i++) { sendStrike(i); }
