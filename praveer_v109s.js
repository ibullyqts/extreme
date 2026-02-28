const axios = require('axios');

const COOKIE = process.env.INSTA_COOKIE;
const THREAD_ID = '2859755064232019'; 
const MESSAGE_BODY = process.env.MESSAGES;

function getCsrf(cookieString) {
    const match = cookieString.match(/csrftoken=([^;]+)/);
    return match ? match[1] : null;
}

// 🔄 KEEP-ALIVE: Pings the server to maintain the 6-month expiry
async function maintainSession() {
    try {
        const csrftoken = getCsrf(COOKIE);
        await axios.get('https://www.instagram.com/api/v1/web/accounts/login/ajax/', {
            headers: { 'cookie': COOKIE, 'x-csrftoken': csrftoken }
        });
    } catch (e) { /* silent fail */ }
}
setInterval(maintainSession, 1800000); 

async function sendStrike(agentId) {
    const csrftoken = getCsrf(COOKIE);
    if (!csrftoken) return;

    const headers = {
        'cookie': COOKIE,
        'x-csrftoken': csrftoken,
        'x-ig-app-id': '936619743392459',
        'content-type': 'application/x-www-form-urlencoded',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
        'referer': `https://www.instagram.com/direct/t/${THREAD_ID}/`
    };

    while (true) {
        try {
            const params = new URLSearchParams({
                'text': MESSAGE_BODY + " " + Math.random().toString(36).substring(7),
                'client_context': Date.now().toString(),
                'thread_ids': `[${THREAD_ID}]`
            });

            await axios.post('https://www.instagram.com/api/v1/direct_messages/threads/broadcast/text/', params.toString(), { headers });
            process.stdout.write(`✅ [Agent ${agentId}] Active\r`);
        } catch (e) {
            const s = e.response ? e.response.status : 'ERR';
            if (s === 429) await new Promise(r => setTimeout(r, 60000));
            else await new Promise(r => setTimeout(r, 5000));
        }
        await new Promise(r => setTimeout(r, 1000 + Math.random() * 500));
    }
}

for (let i = 1; i <= 8; i++) { sendStrike(i); }
