# -*- coding: utf-8 -*-
# متجر الخطاب - نظام زيادة المشاهدات والتفاعلات (رشق)
# جميع الحقوق محفوظة للمطور: @i_tth

import os
import sys
import time
import json
import random
import string
import threading
import webbrowser

from flask import Flask, render_template_string, request, jsonify
import requests
import urllib3
from user_agent import generate_user_agent
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

AUTHOR = "@i_tth"
PHONE = "0963958708905"
YEAR = "2026"

USER_AGENTS = [
    "Mozilla/5.0 (Linux; Android 13; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.4 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
]

def generate_random_string(length=8):
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(length))

# ===== TikTok Services =====
def tiktok_views(url):
    try:
        res = requests.get('https://leofame.com/ar/free-tiktok-views').cookies.get_dict()
        ci_session = res['ci_session']
        token = res['token']
        cookies = {'token': token, 'ci_session': ci_session}
        headers = {
            'authority': 'leofame.com',
            'accept': '*/*',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'https://leofame.com',
            'referer': 'https://leofame.com/ar/free-tiktok-views',
            'user-agent': str(generate_user_agent()),
        }
        params = {'api': '1'}
        data = {'token': token, 'timezone_offset': 'Asia/Baghdad', 'free_link': url}
        response = requests.post('https://leofame.com/ar/free-tiktok-views', 
                                params=params, cookies=cookies, 
                                headers=headers, data=data, verify=False).text
        return "success" in response.lower()
    except:
        return False

def tiktok_likes(url):
    try:
        res = requests.get('https://leofame.com/ar/free-tiktok-likes').cookies.get_dict()
        ci_session = res['ci_session']
        token = res['token']
        cookies = {'ci_session': ci_session, 'token': token}
        headers = {
            'authority': 'leofame.com',
            'accept': '*/*',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'https://leofame.com',
            'referer': 'https://leofame.com/ar/free-tiktok-likes',
            'user-agent': str(generate_user_agent())
        }
        params = {'api': '1'}
        data = {'token': token, 'timezone_offset': 'Asia/Baghdad', 'free_link': url}
        response = requests.post('https://leofame.com/ar/free-tiktok-likes', 
                                params=params, cookies=cookies, 
                                headers=headers, data=data, verify=False).text
        return "success" in response.lower()
    except:
        return False

# ===== Instagram Services =====
def instagram_views(url):
    try:
        res = requests.get('https://leofame.com/ar/free-instagram-views').cookies.get_dict()
        ci_session = res['ci_session']
        token = res['token']
        cookies = {'ci_session': ci_session, 'token': token}
        headers = {
            'authority': 'leofame.com',
            'accept': '*/*',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'https://leofame.com',
            'referer': 'https://leofame.com/ar/free-instagram-views',
            'user-agent': str(generate_user_agent())
        }
        params = {'api': '1'}
        data = {'token': token, 'timezone_offset': 'Asia/Baghdad', 'free_link': url, 'quantity': '200', 'speed': '5'}
        response = requests.post('https://leofame.com/ar/free-instagram-views', 
                                params=params, cookies=cookies, 
                                headers=headers, data=data, verify=False).text
        return "success" in response.lower()
    except:
        return False

def instagram_story_views(url):
    try:
        res = requests.get('https://leofame.com/ar/free-instagram-story-views').cookies.get_dict()
        ci_session = res['ci_session']
        token = res['token']
        cookies = {'ci_session': ci_session, 'token': token}
        headers = {
            'authority': 'leofame.com',
            'accept': '*/*',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'https://leofame.com',
            'referer': 'https://leofame.com/ar/free-instagram-story-views',
            'user-agent': str(generate_user_agent()),
        }
        params = {'api': '1'}
        data = {'token': token, 'timezone_offset': 'Asia/Baghdad', 'free_link': url}
        response = requests.post('https://leofame.com/ar/free-instagram-story-views',
                                params=params, cookies=cookies,
                                headers=headers, data=data, verify=False).text
        return "success" in response.lower()
    except:
        return False

def instagram_shares(url):
    try:
        res = requests.get('https://leofame.com/ar/free-instagram-shares').cookies.get_dict()
        ci_session = res['ci_session']
        token = res['token']
        cookies = {'ci_session': ci_session, 'token': token}
        headers = {
            'authority': 'leofame.com',
            'accept': '*/*',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'https://leofame.com',
            'referer': 'https://leofame.com/ar/free-instagram-shares',
            'user-agent': str(generate_user_agent()),
        }
        params = {'api': '1'}
        data = {'token': token, 'timezone_offset': 'Asia/Baghdad', 'free_link': url, 'quantity': '98', 'speed': '5'}
        response = requests.post('https://leofame.com/ar/free-instagram-shares', 
                                params=params, cookies=cookies, 
                                headers=headers, data=data, verify=False).text
        return "success" in response.lower()
    except:
        return False

# ===== Telegram Service =====
def telegram_boost(channel):
    try:
        session = requests.Session()
        session.headers.update({'User-Agent': random.choice(USER_AGENTS)})
        
        sig_url = "https://www.teljoiner.com/accounts/sign-up/"
        res = session.get(sig_url)
        soup = BeautifulSoup(res.text, 'html.parser')
        token_input = soup.find('input', {'name': 'csrfmiddlewaretoken'})
        if not token_input:
            return False, "لم يتم العثور على توكن"
        token = token_input['value']
        email = f"{generate_random_string()}@ujoice.com"
        password = f"Pass_{generate_random_string(4)}!"
        session.post(sig_url, data={
            'csrfmiddlewaretoken': token,
            'email': email,
            'password': password,
            'confirm_password': password
        }, headers={'Referer': sig_url})
        
        login_url = "https://www.teljoiner.com/accounts/sign-in/"
        res_login = session.get(login_url)
        soup_login = BeautifulSoup(res_login.text, 'html.parser')
        token_login = soup_login.find('input', {'name': 'csrfmiddlewaretoken'})['value']
        session.post(login_url, data={
            'csrfmiddlewaretoken': token_login,
            'email': email,
            'password': password
        }, headers={'Referer': login_url})
        
        boost_url = "https://www.teljoiner.com/telegram/free-service-request/"
        res_boost = session.post(boost_url, json={
            "request_type": "free-member",
            "channel_id": channel,
            "member_count": 221,
            "channel_info": {"name": "BotService", "username": channel, "id": channel}
        }, headers={
            'x-csrftoken': session.cookies.get('csrftoken'),
            'Referer': "https://www.teljoiner.com/telegram/sessions/",
            'Content-Type': 'application/json'
        })
        if res_boost.status_code in [200, 201]:
            return True, "✅ تم الإرسال بنجاح - ستبدأ الزيادة خلال 29 دقيقة"
        else:
            return False, f"❌ فشل: {res_boost.status_code}"
    except Exception as e:
        return False, f"❌ خطأ: {str(e)}"

# ===== قالب HTML المطور والمعدل بالألوان والأقسام =====
HTML_TEMPLATE = """
<!DOCTYPE html>
<html dir="rtl" lang="ar">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>منصة الخطاب للرشق الذكي © {{ year }}</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
        
        :root {
            --bg-primary: #070a13;
            --bg-secondary: #0f1322;
            --bg-card: #151b30;
            --border-color: #1e294b;
            --text-primary: #ffffff;
            --text-secondary: #a0aec0;
            --text-muted: #64748b;
            --shadow: rgba(0, 0, 0, 0.5);
        }

        body {
            background: var(--bg-primary);
            color: var(--text-primary);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 20px;
        }
        
        .container { max-width: 750px; width: 100%; margin-top: 20px; }

        /* ===== Header ===== */
        .header {
            text-align: center;
            padding: 20px 0;
            border-bottom: 2px solid var(--border-color);
            margin-bottom: 30px;
        }
        .logo { 
            font-size: 32px; 
            font-weight: 800; 
            color: #fff;
            letter-spacing: -0.5px;
        }
        .logo span { color: #38bdf8; }
        .subtitle {
            font-size: 14px;
            color: var(--text-secondary);
            margin-top: 5px;
        }

        /* ===== Home Grid ===== */
        .home-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 20px;
            margin: 20px 0 30px 0;
        }
        
        .home-btn {
            padding: 35px 15px;
            border: none;
            border-radius: 20px;
            color: #fff;
            font-size: 20px;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.3s ease;
            text-align: center;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            gap: 12px;
        }
        
        .btn-tiktok {
            background: linear-gradient(135deg, #ee1d52 0%, #69c9d0 100%);
        }
        .btn-instagram {
            background: linear-gradient(135deg, #fccc63 0%, #fbad50 15%, #cd486b 50%, #4c68d7 100%);
        }
        .btn-telegram {
            background: linear-gradient(135deg, #0088cc 0%, #24a1de 100%);
        }

        .home-btn:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 25px rgba(255,255,255,0.1);
            filter: brightness(1.1);
        }
        
        .home-btn .icon { font-size: 45px; }
        .home-btn .label { font-size: 18px; font-weight: bold; }

        /* ===== Service Area ===== */
        .service-area {
            background: var(--bg-secondary);
            border-radius: 20px;
            padding: 30px;
            border: 1px solid var(--border-color);
            display: none;
            box-shadow: 0 10px 30px var(--shadow);
        }
        .service-area.active { display: block; animation: fadeIn 0.4s ease; }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }

        .back-btn {
            background: #334155;
            border: none;
            color: #fff;
            font-size: 14px;
            cursor: pointer;
            margin-bottom: 20px;
            padding: 8px 16px;
            border-radius: 10px;
            font-weight: 600;
            transition: 0.2s;
        }
        .back-btn:hover { background: #475569; }

        .platform-title { font-size: 24px; font-weight: 700; margin-bottom: 5px; display: flex; align-items: center; gap: 10px; }
        .platform-sub { font-size: 14px; color: var(--text-secondary); margin-bottom: 20px; }

        /* ===== Service Buttons ===== */
        .service-btns { display: flex; flex-wrap: wrap; gap: 12px; margin-bottom: 25px; }
        .service-btn {
            padding: 12px 24px;
            border: 2px solid var(--border-color);
            border-radius: 12px;
            background: var(--bg-primary);
            color: var(--text-secondary);
            font-size: 14px;
            font-weight: 600;
            cursor: pointer;
            transition: 0.2s;
        }
        .service-btn:hover { border-color: #38bdf8; color: #fff; }
        .service-btn.active { border-color: #38bdf8; background: #38bdf8; color: #000; font-weight: bold; }

        /* ===== Input Area ===== */
        .input-area { display: flex; gap: 12px; background: var(--bg-card); border: 1px solid var(--border-color); border-radius: 15px; padding: 6px; }
        .input-area input {
            flex: 1; padding: 14px; border: none; background: transparent; color: #fff; font-size: 16px; outline: none; text-align: right;
        }
        .input-area input::placeholder { color: var(--text-muted); }
        .input-area .btn-submit {
            padding: 12px 28px; border: none; border-radius: 12px; background: #38bdf8; color: #000; font-size: 16px; font-weight: 700; cursor: pointer; transition: 0.2s;
        }
        .input-area .btn-submit:hover { background: #0ea5e9; }

        .result-box {
            margin-top: 20px; padding: 15px; border-radius: 12px; background: var(--bg-primary); border: 1px solid var(--border-color); font-size: 14px; text-align: center; color: var(--text-secondary);
        }
        .result-box.success { border-color: #4ade80; color: #4ade80; background: rgba(74, 222, 128, 0.05); }
        .result-box.error { border-color: #f87171; color: #f87171; background: rgba(248, 113, 113, 0.05); }

        /* ===== Footer ===== */
        .footer {
            margin-top: 50px; padding: 20px 0; border-top: 1px solid var(--border-color); text-align: center; font-size: 14px; color: var(--text-secondary); width: 100%;
        }
        .footer-links { display: flex; justify-content: center; gap: 20px; margin-top: 10px; flex-wrap: wrap; }
        .footer-links a {
            color: #38bdf8; text-decoration: none; padding: 6px 16px; background: var(--bg-secondary); border: 1px solid var(--border-color); border-radius: 20px; font-size: 13px; transition: 0.2s;
        }
        .footer-links a:hover { background: #38bdf8; color: #000; }

        @media (max-width: 600px) {
            .home-grid { grid-template-columns: 1fr; gap: 15px; }
            .home-btn { padding: 25px; }
            .input-area { flex-direction: column; background: transparent; border: none; padding: 0; }
            .input-area input { background: var(--bg-card); border: 1px solid var(--border-color); border-radius: 12px; margin-bottom: 10px; width: 100%; }
            .input-area .btn-submit { width: 100%; }
        }
    </style>
</head>
<body>
<div class="container">

    <!-- ===== Header ===== -->
    <div class="header">
        <div class="logo">منصة <span>الخطاب</span></div>
        <div class="subtitle">سكربت رشق الخدمات وتكبير الحسابات التلقائي الآمن</div>
    </div>

    <!-- ===== HOME ===== -->
    <div id="homeScreen">
        <div class="home-grid">
            <button class="home-btn btn-tiktok" onclick="showPlatform('tiktok')">
                <span class="icon">🎵</span>
                <span class="label">قسم تيك توك</span>
            </button>
            <button class="home-btn btn-instagram" onclick="showPlatform('instagram')">
                <span class="icon">📸</span>
                <span class="label">قسم انستجرام</span>
            </button>
            <button class="home-btn btn-telegram" onclick="showPlatform('telegram')">
                <span class="icon">🔹</span>
                <span class="label">قسم تلجرام</span>
            </button>
        </div>
    </div>

    <!-- ===== TikTok Section ===== -->
    <div id="platform-tiktok" class="service-area">
        <button class="back-btn" onclick="goHome()">🏡 العودة للرئيسية</button>
        <div class="platform-title">🎵 رشق تيك توك</div>
        <div class="platform-sub">اختر إحدى الخدمات المجانية المتوفرة أدناه:</div>
        <div class="service-btns">
            <button class="service-btn active" data-service="likes" data-platform="tiktok">❤️ رشق لايكات</button>
            <button class="service-btn" data-service="views" data-platform="tiktok">👁️ رشق مشاهدات</button>
        </div>
        <div class="input-area">
            <input type="text" id="input-tiktok" placeholder="ضع رابط فيديو التيك توك هنا...">
            <button class="btn-submit" onclick="sendRequest('tiktok')">إرسال الطلب</button>
        </div>
        <div class="result-box" id="result-tiktok">📌 الحالة: في انتظار إدخال الرابط...</div>
    </div>

    <!-- ===== Instagram Section ===== -->
    <div id="platform-instagram" class="service-area">
        <button class="back-btn" onclick="goHome()">🏡 العودة للرئيسية</button>
        <div class="platform-title">📸 رشق انستجرام</div>
        <div class="platform-sub">اختر إحدى الخدمات المجانية المتوفرة أدناه:</div>
        <div class="service-btns">
            <button class="service-btn active" data-service="views" data-platform="instagram">👁️ رشق مشاهدات</button>
            <button class="service-btn" data-service="story" data-platform="instagram">📖 مشاهدات ستوري</button>
            <button class="service-btn" data-service="shares" data-platform="instagram">🔁 رشق مشاركات</button>
        </div>
        <div class="input-area">
            <input type="text" id="input-instagram" placeholder="ضع رابط المنشور أو الستوري هنا...">
            <button class="btn-submit" onclick="sendRequest('instagram')">إرسال الطلب</button>
        </div>
        <div class="result-box" id="result-instagram">📌 الحالة: في انتظار إدخال الرابط...</div>
    </div>

    <!-- ===== Telegram Section ===== -->
    <div id="platform-telegram" class="service-area">
        <button class="back-btn" onclick="goHome()">🏡 العودة للرئيسية</button>
        <div class="platform-title">🔹 رشق تلجرام</div>
        <div class="platform-sub">اختر إحدى الخدمات المجانية المتوفرة أدناه:</div>
        <div class="service-btns">
            <button class="service-btn active" data-service="members" data-platform="telegram">👥 رشق أعضاء القنوات</button>
        </div>
        <div class="input-area">
            <input type="text" id="input-telegram" placeholder="أدخل معرف القناة بدون @ أو الرابط">
            <button class="btn-submit" onclick="sendRequest('telegram')">إرسال الطلب</button>
        </div>
        <div class="result-box" id="result-telegram">📌 الحالة: في انتظار إدخال المعرف...</div>
    </div>

    <!-- ===== Footer ===== -->
    <div class="footer">
        <p>جميع الحقوق محفوظة للمطور المعتمد © {{ year }}</p>
        <div class="footer-links">
            <a href="https://t.me/i_tth" target="_blank">💬 تليجرام المطور: {{ author }}</a>
            <a href="https://wa.me/963958708905" target="_blank">📞 هاتف/واتساب: 0963958708905</a>
        </div>
    </div>

</div>

<script>
function showPlatform(platform) {
    document.getElementById('homeScreen').style.display = 'none';
    document.querySelectorAll('.service-area').forEach(a => a.classList.remove('active'));
    document.getElementById('platform-' + platform).classList.add('active');
}

function goHome() {
    document.getElementById('homeScreen').style.display = 'block';
    document.querySelectorAll('.service-area').forEach(a => a.classList.remove('active'));
}

document.querySelectorAll('.service-btn').forEach(btn => {
    btn.addEventListener('click', function() {
        const parent = this.closest('.service-area');
        parent.querySelectorAll('.service-btn').forEach(b => b.classList.remove('active'));
        this.classList.add('active');
    });
});

function sendRequest(platform) {
    const inputMap = { 'tiktok': 'input-tiktok', 'instagram': 'input-instagram', 'telegram': 'input-telegram' };
    const resultMap = { 'tiktok': 'result-tiktok', 'instagram': 'result-instagram', 'telegram': 'result-telegram' };

    const input = document.getElementById(inputMap[platform]);
    const result = document.getElementById(resultMap[platform]);
    const url = input.value.trim();

    if (!url) {
        result.className = 'result-box error';
        result.textContent = '❌ الرجاء إدخال الرابط أو المعرف المطلوب أولاً!';
        return;
    }

    const activeBtn = document.querySelector('#platform-' + platform + ' .service-btn.active');
    const service = activeBtn ? activeBtn.dataset.service : '';

    result.className = 'result-box';
    result.textContent = '⏳ جاري معالجة طلب الرشق، يرجى الانتظار دون إغلاق الصفحة...';

    const endpoint = '/api/' + platform + '_' + service;

    fetch(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url: url })
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            result.className = 'result-box success';
            result.textContent = data.message;
        } else {
            result.className = 'result-box error';
            result.textContent = data.message;
        }
    })
    .catch(() => {
        result.className = 'result-box error';
        result.textContent = '❌ حدث خطأ غير متوقع أثناء الاتصال بالخادم الرئيسي.';
    });
}
</script>
</body>
</html>
"""

# ===== Flask App =====
app = Flask(__name__)

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE, author=AUTHOR, year=YEAR)

@app.route('/api/<service>', methods=['POST'])
def api_service(service):
    data = request.get_json()
    url = data.get('url', '').strip()
    if not url:
        return jsonify({'success': False, 'message': 'الرجاء إدخال البيانات المطلوبة'})
    
    services = {
        'tiktok_likes': (tiktok_likes, '✅ تم إرسال طلب لايكات التيك توك بنجاح!'),
        'tiktok_views': (tiktok_views, '✅ تم إرسال طلب مشاهدات التيك توك بنجاح!'),
        'instagram_views': (instagram_views, '✅ تم إرسال طلب مشاهدات الانستجرام بنجاح!'),
        'instagram_story': (instagram_story_views, '✅ تم إرسال طلب مشاهدات الستوري بنجاح!'),
        'instagram_shares': (instagram_shares, '✅ تم إرسال طلب مشاركات الانستجرام بنجاح!'),
        'telegram_members': (telegram_boost, '✅ تم إرسال طلب أعضاء التلجرام بنجاح! ستبدأ الزيادة تلقائياً خلال دقائق.'),
    }
    
    if service in services:
        func, msg = services[service]
        result = func(url)
        if isinstance(result, tuple):
            success, message = result
            return jsonify({'success': success, 'message': message if not success else msg})
        return jsonify({'success': result, 'message': msg if result else '❌ عذراً، فشل إرسال الرشق حالياً، المزود تحت الضغط.'})
    else:
        return jsonify({'success': False, 'message': 'الخدمة المطلوبة غير متوفرة حالياً.'})

def open_browser():
    time.sleep(1.5)
    webbrowser.open('http://127.0.0.1:5000')

if __name__ == '__main__':
    print("""
    ╔═══════════════════════════════════════════════╗
    ║   منصة الخطاب للرشق تعمل بنجاح!               ║
    ║   رابط الدخول المحلي: http://127.0.0.1:5000   ║
    ╚═══════════════════════════════════════════════╝
    """)
    threading.Thread(target=open_browser, daemon=True).start()
    app.run(host='127.0.0.1', port=5000, debug=False)
