# pages.py
# TK-SX - تمام صفحات HTML (پنل اصلی + مینی‌اپ Cyrus Bot)

# ── لوگو و برندینگ ──────────────────────────────────────────────────────────
LOGO_HTML = '<span style="font-weight:900;font-size:22px;color:var(--accent);">TK-SX</span>'
LOGO_HTML_SMALL = '<span style="font-weight:900;font-size:16px;color:var(--accent);">TK-SX</span>'

# ── صفحه ورود پنل اصلی (تم نارنجی-مشکی - TITI) ─────────────────────────────
LOGIN_HTML = r"""<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>ورود · TK-SX</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@3.19.0/dist/tabler-icons.min.css">
<style>
*{margin:0;padding:0;box-sizing:border-box}
:root{--bg:#0a0a0a;--card:rgba(20,20,20,0.92);--accent:#F97316;--text:#F5F5F5;--dim:#6B6B6B;--mid:#B0B0B0;--border:rgba(249,115,22,0.25)}
html,body{height:100%;overflow:hidden}
body{font-family:'Vazirmatn',sans-serif;background:var(--bg);display:flex;align-items:center;justify-content:center;padding:20px}
.bg{position:fixed;inset:0;background:radial-gradient(ellipse 80% 60% at 50% 0%,rgba(249,115,22,0.08),transparent 70%),var(--bg);z-index:0}
.grid{position:fixed;inset:0;background-image:linear-gradient(rgba(249,115,22,0.04) 1px,transparent 1px),linear-gradient(90deg,rgba(249,115,22,0.04) 1px,transparent 1px);background-size:44px 44px;z-index:0}
.orb{position:fixed;border-radius:50%;filter:blur(90px);z-index:0;animation:fl 9s ease-in-out infinite}
.o1{width:380px;height:380px;background:rgba(249,115,22,0.07);top:-100px;right:-80px}
.o2{width:280px;height:280px;background:rgba(249,115,22,0.04);bottom:-60px;left:-60px;animation-delay:4s}
@keyframes fl{0%,100%{transform:translateY(0)}50%{transform:translateY(-18px)}}
.wrap{position:relative;z-index:10;width:100%;max-width:400px}
.card{background:var(--card);border:1px solid var(--border);border-radius:20px;padding:38px 34px 34px;backdrop-filter:blur(24px);box-shadow:0 0 80px rgba(249,115,22,0.07),0 20px 60px rgba(0,0,0,.5)}
.brand{display:flex;align-items:center;gap:14px;margin-bottom:28px}
.brand-img{width:48px;height:48px;border-radius:50%;overflow:hidden;border:1px solid var(--border);box-shadow:0 0 20px rgba(249,115,22,0.35),0 0 12px rgba(249,115,22,0.3);flex-shrink:0;display:flex;align-items:center;justify-content:center;background:var(--bg);color:var(--accent);font-weight:900;font-size:18px}
.brand-name{font-size:16px;font-weight:700;color:var(--text)}
.brand-sub{font-size:11px;color:var(--dim);margin-top:2px}
h1{font-size:21px;font-weight:700;color:var(--text);margin-bottom:5px;letter-spacing:-.02em}
.sub{font-size:12px;color:var(--mid);margin-bottom:24px;line-height:1.6}
.hint{display:flex;align-items:center;gap:10px;background:rgba(249,115,22,0.07);border:1px solid rgba(249,115,22,0.15);border-radius:10px;padding:10px 14px;margin-bottom:20px}
.hint-label{font-size:11px;color:var(--dim);flex:1}
.hint-val{font-family:ui-monospace,monospace;font-size:14px;font-weight:700;color:var(--accent);background:rgba(249,115,22,0.1);border:1px solid rgba(249,115,22,0.25);padding:3px 11px;border-radius:7px;cursor:pointer;transition:.15s;letter-spacing:.08em}
.hint-val:hover{background:rgba(249,115,22,0.22)}
.field{margin-bottom:18px}
.field label{display:block;font-size:10.5px;font-weight:600;color:var(--mid);margin-bottom:7px;text-transform:uppercase;letter-spacing:.06em}
.inp-wrap{position:relative}
input[type=password]{width:100%;padding:13px 44px 13px 16px;border-radius:11px;border:1px solid var(--border);background:rgba(0,0,0,.3);color:var(--text);font-family:inherit;font-size:14px;outline:none;transition:.2s}
input[type=password]:focus{border-color:rgba(249,115,22,.55);background:rgba(0,0,0,.4);box-shadow:0 0 0 3px rgba(249,115,22,.1)}
.ic{position:absolute;left:14px;top:50%;transform:translateY(-50%);color:var(--dim);font-size:18px;pointer-events:none;transition:.2s}
input:focus+.ic{color:var(--accent)}
.err{display:none;background:rgba(239,68,68,.08);border:1px solid rgba(239,68,68,.2);border-radius:10px;padding:10px 14px;margin-bottom:14px;font-size:12px;color:#F87171;align-items:center;gap:8px}
.err.show{display:flex}
.btn{width:100%;padding:13px;border-radius:11px;border:none;cursor:pointer;background:linear-gradient(135deg,#F97316,#EA580C);color:#fff;font-family:inherit;font-size:14px;font-weight:600;display:flex;align-items:center;justify-content:center;gap:8px;box-shadow:0 4px 20px rgba(249,115,22,.35);transition:.2s;position:relative;overflow:hidden}
.btn::before{content:'';position:absolute;inset:0;background:rgba(255,255,255,.08);opacity:0;transition:.2s}
.btn:hover::before{opacity:1}
.btn:disabled{opacity:.5;cursor:not-allowed}
.footer{margin-top:22px;padding-top:18px;border-top:1px solid var(--border);display:flex;align-items:center;justify-content:center;gap:8px;font-size:11px;color:var(--dim);flex-wrap:wrap}
.footer a{color:var(--accent);font-weight:600;text-decoration:none;display:flex;align-items:center;gap:4px}
@keyframes spin{to{transform:rotate(360deg)}}
</style>
</head>
<body>
<div class="bg"></div><div class="grid"></div>
<div class="orb o1"></div><div class="orb o2"></div>
<div class="wrap">
  <div class="card">
    <div class="brand">
      <div class="brand-img">TK</div>
      <div><div class="brand-name">TK-SX</div><div class="brand-sub">v3.0</div></div>
    </div>
    <h1>ورود به پنل</h1>
    <p class="sub">رمز عبور را برای دسترسی به داشبورد وارد کنید</p>
    <div class="err" id="err"><i class="ti ti-alert-circle"></i><span id="err-text"></span></div>
    <div class="hint">
      <span class="hint-label">رمز پیش‌فرض سیستم</span>
      <span class="hint-val" onclick="document.getElementById('pw').value='taakaa';document.getElementById('pw').focus()">taakaa</span>
    </div>
    <form id="form">
      <div class="field">
        <label>رمز عبور</label>
        <div class="inp-wrap">
          <input type="password" id="pw" placeholder="رمز عبور را وارد کنید" autofocus required>
          <i class="ti ti-lock ic"></i>
        </div>
      </div>
      <button class="btn" type="submit" id="btn"><i class="ti ti-login-2"></i> ورود به داشبورد</button>
    </form>
    <div class="footer">
      <span>پشتیبانی: <a href="https://t.me/ItzJustEren" target="_blank"><i class="ti ti-brand-telegram"></i>@ItzJustEren</a></span>
      <span>کانال: <a href="https://t.me/TaaKaaOrg" target="_blank"><i class="ti ti-brand-telegram"></i>@TaaKaaOrg</a></span>
    </div>
  </div>
</div>
<script>
document.getElementById('form').addEventListener('submit',async e=>{
  e.preventDefault();
  const btn=document.getElementById('btn'),err=document.getElementById('err'),et=document.getElementById('err-text');
  err.classList.remove('show');btn.disabled=true;
  btn.innerHTML='<i class="ti ti-loader-2" style="animation:spin 1s linear infinite"></i> در حال ورود...';
  try{
    const r=await fetch('/api/login',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({password:document.getElementById('pw').value})});
    if(!r.ok){const d=await r.json().catch(()=>({}));throw new Error(d.detail||'خطا');}
    location.href='/dashboard';
  }catch(e){
    et.textContent=e.message;err.classList.add('show');
    btn.disabled=false;btn.innerHTML='<i class="ti ti-login-2"></i> ورود به داشبورد';
  }
});
</script>
</body></html>"""


# ── مینی‌اپ Cyrus Bot (تم آبی-یخی-مشکی + لوگوی عقاب) ────────────────────────
CYRUS_MINIAPP_HTML = r"""<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<title>Cyrus Bot · پنل مدیریت</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@3.19.0/dist/tabler-icons.min.css">
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Vazirmatn',sans-serif;background:#0B0F1A;color:#F0F4FF;min-height:100vh;display:flex;align-items:center;justify-content:center;overflow:hidden}
.bg-fx{position:fixed;inset:0;background:radial-gradient(ellipse 70% 50% at 50% 0%,rgba(56,189,248,0.08),transparent 70%),radial-gradient(ellipse 40% 40% at 80% 90%,rgba(37,99,235,0.05),transparent 60%),#0B0F1A;z-index:0}
.grid-fx{position:fixed;inset:0;background-image:linear-gradient(rgba(56,189,248,0.025) 1px,transparent 1px),linear-gradient(90deg,rgba(56,189,248,0.025) 1px,transparent 1px);background-size:48px 48px;z-index:0}
.glow-orb{position:fixed;border-radius:50%;filter:blur(100px);z-index:0}
.go1{width:300px;height:300px;background:rgba(56,189,248,0.06);top:-80px;right:-80px;animation:float1 12s ease-in-out infinite}
.go2{width:200px;height:200px;background:rgba(37,99,235,0.04);bottom:-40px;left:-40px;animation:float2 14s ease-in-out infinite}
@keyframes float1{0%,100%{transform:translate(0,0)}50%{transform:translate(-30px,20px)}}
@keyframes float2{0%,100%{transform:translate(0,0)}50%{transform:translate(30px,-20px)}}
.wrap{position:relative;z-index:10;width:100%;max-width:420px;padding:16px}
.card{background:linear-gradient(160deg,rgba(17,24,39,0.95),rgba(11,15,26,0.98));border:1px solid rgba(56,189,248,0.15);border-radius:24px;padding:0;backdrop-filter:blur(20px);box-shadow:0 20px 60px rgba(0,0,0,0.7),0 0 80px rgba(56,189,248,0.04);overflow:hidden;position:relative}
.card::before{content:'';position:absolute;top:0;left:0;right:0;height:2px;background:linear-gradient(90deg,transparent,rgba(56,189,248,0.4),transparent)}
.card::after{content:'';position:absolute;top:-50%;right:-50%;width:100%;height:100%;background:radial-gradient(circle,rgba(56,189,248,0.02),transparent 70%);pointer-events:none}
.header{background:linear-gradient(160deg,rgba(56,189,248,0.04),transparent);padding:30px 28px 22px;position:relative;border-bottom:1px solid rgba(56,189,248,0.06)}
.eagle-logo{display:flex;align-items:center;gap:16px;position:relative;z-index:1}
.eagle-icon{width:60px;height:60px;border-radius:50%;background:linear-gradient(135deg,#0EA5E9,#2563EB);display:flex;align-items:center;justify-content:center;font-size:28px;color:#fff;flex-shrink:0;box-shadow:0 0 40px rgba(56,189,248,0.25);position:relative}
.eagle-icon::after{content:'';position:absolute;inset:-3px;border-radius:50%;border:1px solid rgba(56,189,248,0.2);animation:pulse-ring 3s ease-in-out infinite}
@keyframes pulse-ring{0%,100%{transform:scale(1);opacity:0.5}50%{transform:scale(1.1);opacity:0}}
.eagle-text .name{font-size:22px;font-weight:900;color:#F0F4FF;letter-spacing:-.02em;background:linear-gradient(90deg,#F0F4FF,#94A3B8);-webkit-background-clip:text;-webkit-text-fill-color:transparent}
.eagle-text .name span{background:linear-gradient(90deg,#38BDF8,#0EA5E9);-webkit-background-clip:text;-webkit-text-fill-color:transparent}
.eagle-text .sub-title{font-size:11px;color:#94A3B8;margin-top:2px;display:flex;align-items:center;gap:6px}
.eagle-text .sub-title i{color:#38BDF8;font-size:13px}
.welcome-box{background:rgba(56,189,248,0.04);border-right:3px solid #38BDF8;border-radius:12px;padding:14px 18px;margin:0 24px 22px;font-size:12.5px;color:#94A3B8;line-height:1.9;position:relative;z-index:1}
.welcome-box i{color:#38BDF8;margin-left:6px;font-size:14px}
.body{padding:0 24px 28px;position:relative;z-index:1}
.err{display:none;background:rgba(239,68,68,0.08);border:1px solid rgba(239,68,68,0.2);border-radius:12px;padding:10px 14px;margin-bottom:16px;font-size:12px;color:#F87171;align-items:center;gap:8px}
.err.show{display:flex}
.field{margin-bottom:16px}
.field label{display:block;font-size:10px;font-weight:700;color:#94A3B8;text-transform:uppercase;letter-spacing:.06em;margin-bottom:6px}
.inp-wrap{position:relative}
.inp-wrap input{width:100%;padding:13px 44px 13px 16px;border-radius:12px;border:1px solid rgba(56,189,248,0.15);background:rgba(0,0,0,0.4);color:#F0F4FF;font-family:inherit;font-size:13px;outline:none;transition:.2s}
.inp-wrap input::placeholder{color:#64748B}
.inp-wrap input:focus{border-color:#38BDF8;box-shadow:0 0 0 3px rgba(56,189,248,0.08)}
.inp-wrap i{position:absolute;left:14px;top:50%;transform:translateY(-50%);color:#64748B;font-size:18px;transition:.2s}
.inp-wrap input:focus + i{color:#38BDF8}
.btn-login{width:100%;padding:13px;border-radius:12px;border:none;cursor:pointer;background:linear-gradient(135deg,#0EA5E9,#2563EB);color:#fff;font-family:inherit;font-size:14px;font-weight:700;display:flex;align-items:center;justify-content:center;gap:8px;box-shadow:0 4px 20px rgba(56,189,248,0.3);transition:.2s;position:relative;overflow:hidden}
.btn-login::before{content:'';position:absolute;inset:0;background:rgba(255,255,255,.08);opacity:0;transition:.2s}
.btn-login:hover::before{opacity:1}
.btn-login:disabled{opacity:.5;cursor:not-allowed}
.footer-mini{margin-top:20px;padding-top:16px;border-top:1px solid rgba(56,189,248,0.08);display:flex;align-items:center;justify-content:center;gap:8px;font-size:10px;color:#64748B;flex-wrap:wrap}
.footer-mini a{color:#38BDF8;font-weight:600;text-decoration:none}
.cert-badge{display:flex;align-items:center;gap:6px;background:rgba(56,189,248,0.06);border:1px solid rgba(56,189,248,0.08);border-radius:20px;padding:4px 12px;font-size:9px;color:#94A3B8;margin-top:14px;justify-content:center}
.cert-badge i{color:#10B981;font-size:12px}
@keyframes spin{to{transform:rotate(360deg)}}
</style>
</head>
<body>
<div class="bg-fx"></div><div class="grid-fx"></div>
<div class="glow-orb go1"></div><div class="glow-orb go2"></div>
<div class="wrap">
  <div class="card">
    <div class="header">
      <div class="eagle-logo">
        <div class="eagle-icon"><i class="ti ti-brand-cyrus"></i></div>
        <div class="eagle-text">
          <div class="name">Cyrus <span>Bot</span></div>
          <div class="sub-title"><i class="ti ti-crown"></i> پنل مدیریت پیشرفته · TK-SX</div>
        </div>
      </div>
    </div>
    <div class="welcome-box">
      <i class="ti ti-message-2"></i>
      درود به پنل Cyrus Bot خوش اومدید<br>
      این پنل متعلق به تیم تاکا است و سازگاری کامل با پنل TK-SX دارد
    </div>
    <div class="body">
      <div class="err" id="err"><i class="ti ti-alert-circle"></i><span id="err-text"></span></div>
      <div class="field">
        <label>رمز عبور ادمین</label>
        <div class="inp-wrap">
          <input type="password" id="pw" placeholder="رمز عبور را وارد کنید" autofocus>
          <i class="ti ti-lock"></i>
        </div>
      </div>
      <button class="btn-login" id="btn" onclick="login()"><i class="ti ti-login-2"></i> ورود به پنل</button>
      <div class="cert-badge"><i class="ti ti-shield-check"></i> اتصال امن · TLS 1.3 · TK-SX v3.0</div>
      <div class="footer-mini">
        <span>پشتیبانی: <a href="https://t.me/ItzJustEren">@ItzJustEren</a></span>
        <span>|</span>
        <span>کانال: <a href="https://t.me/TaaKaaOrg">@TaaKaaOrg</a></span>
      </div>
    </div>
  </div>
</div>
<script>
let token = null;
async function login() {
  const pw = document.getElementById('pw').value;
  const btn = document.getElementById('btn');
  const err = document.getElementById('err');
  const et = document.getElementById('err-text');
  err.classList.remove('show'); btn.disabled = true;
  btn.innerHTML = '<i class="ti ti-loader-2" style="animation:spin 1s linear infinite"></i> در حال ورود...';
  try {
    const r = await fetch('/api/miniapp/login', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({password: pw})
    });
    if (!r.ok) { const d = await r.json(); throw new Error(d.detail || 'خطا'); }
    const data = await r.json();
    token = data.token;
    await loadDashboard();
  } catch(e) {
    et.textContent = e.message; err.classList.add('show');
    btn.disabled = false; btn.innerHTML = '<i class="ti ti-login-2"></i> ورود به پنل';
  }
}
async function loadDashboard() {
  const btn = document.getElementById('btn');
  try {
    const r = await fetch('/api/miniapp/stats?token=' + encodeURIComponent(token));
    if (!r.ok) { await login(); return; }
    const data = await r.json();
    document.querySelector('.welcome-box').innerHTML = `
      <i class="ti ti-chart-bar"></i>
      <b>📊 داشبورد Cyrus Bot</b><br>
      🔗 کانفیگ‌ها: ${data.links_count} | 🔌 اتصالات: ${data.active_connections} | 📦 محصولات: ${data.products_count}<br>
      📋 سفارشات در انتظار: ${data.orders_pending} | 💳 کارت‌های در انتظار: ${data.cards_pending}<br>
      🚀 آپتایم: ${data.uptime} | ⚡ Sing-box: ${data.singbox_status.running ? 'فعال ✅' : 'غیرفعال ❌'}
    `;
    document.querySelector('.body').innerHTML += `
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:14px">
        <div style="background:rgba(56,189,248,0.05);border:1px solid rgba(56,189,248,0.1);border-radius:12px;padding:14px;text-align:center">
          <div style="font-size:24px;font-weight:900;color:#38BDF8">${data.links_count}</div>
          <div style="font-size:10px;color:#94A3B8">کانفیگ</div>
        </div>
        <div style="background:rgba(16,185,129,0.05);border:1px solid rgba(16,185,129,0.1);border-radius:12px;padding:14px;text-align:center">
          <div style="font-size:24px;font-weight:900;color:#34D399">${data.active_connections}</div>
          <div style="font-size:10px;color:#94A3B8">اتصال زنده</div>
        </div>
        <div style="background:rgba(245,158,11,0.05);border:1px solid rgba(245,158,11,0.1);border-radius:12px;padding:14px;text-align:center">
          <div style="font-size:24px;font-weight:900;color:#F59E0B">${data.products_count}</div>
          <div style="font-size:10px;color:#94A3B8">محصول</div>
        </div>
        <div style="background:rgba(139,92,246,0.05);border:1px solid rgba(139,92,246,0.1);border-radius:12px;padding:14px;text-align:center">
          <div style="font-size:24px;font-weight:900;color:#A78BFA">${data.subs_count}</div>
          <div style="font-size:10px;color:#94A3B8">گروه ساب</div>
        </div>
      </div>
      <div style="margin-top:12px;display:flex;gap:8px;flex-wrap:wrap">
        <button onclick="window.location.href='/dashboard'" style="flex:1;padding:10px;border-radius:10px;border:1px solid rgba(56,189,248,0.2);background:rgba(56,189,248,0.05);color:#38BDF8;font-family:inherit;font-weight:700;cursor:pointer;font-size:12px">
          <i class="ti ti-layout-dashboard"></i> پنل اصلی
        </button>
        <button onclick="window.location.href='https://t.me/'+encodeURIComponent('CyrusBot')" style="flex:1;padding:10px;border-radius:10px;border:1px solid rgba(56,189,248,0.2);background:rgba(56,189,248,0.05);color:#38BDF8;font-family:inherit;font-weight:700;cursor:pointer;font-size:12px">
          <i class="ti ti-brand-telegram"></i> ربات
        </button>
      </div>
    `;
    btn.style.display = 'none';
    document.getElementById('pw').style.display = 'none';
    document.querySelector('.field label').style.display = 'none';
  } catch(e) { alert('خطا در بارگذاری داشبورد'); }
}
document.getElementById('pw').addEventListener('keydown', e => { if(e.key === 'Enter') login(); });
</script>
</body></html>"""


# ── صفحه پابلیک گروه‌ها (رفع کامل خطای SyntaxError) ──────────────────────
def get_public_page_html(uuid_key: str) -> str:
    return (
        r"""<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0">
<title>TK-SX Sub</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@3.19.0/dist/tabler-icons.min.css">
<style>
*{margin:0;padding:0;box-sizing:border-box;-webkit-tap-highlight-color:transparent}
:root{--bg:#0a0a0a;--bg2:#141414;--bg3:#1e1e1e;--card:#1a1a1a;--card-b:rgba(249,115,22,0.15);--card-bh:rgba(249,115,22,0.35);--accent:#F97316;--accent2:#FB923C;--accent-d:rgba(249,115,22,0.1);--green:#10B981;--green-bg:rgba(16,185,129,0.1);--green-t:#34D399;--red:#EF4444;--red-bg:rgba(239,68,68,0.1);--red-t:#F87171;--amber:#F59E0B;--amber-bg:rgba(245,158,11,0.1);--amber-t:#FCD34D;--purple:#9D7BF0;--purple-bg:rgba(157,123,240,0.1);--purple-t:#BCA4F7;--t1:#F5F5F5;--t2:#B0B0B0;--t3:#6B6B6B;--radius:18px;--shadow:0 12px 40px rgba(0,0,0,0.5);--serif:'Vazirmatn',sans-serif;}
[data-theme="light"]{--bg:#F5F5F5;--bg2:#E8E8E8;--bg3:#DCDCDC;--card:#FFFFFF;--card-b:rgba(249,115,22,0.2);--card-bh:rgba(249,115,22,0.4);--accent:#EA580C;--accent2:#F97316;--accent-d:rgba(234,88,12,0.08);--green:#059669;--green-bg:rgba(5,150,105,0.08);--green-t:#065F46;--red:#DC2626;--red-bg:rgba(220,38,38,0.08);--red-t:#991B1B;--amber:#D97706;--amber-bg:rgba(217,119,6,0.08);--amber-t:#92400E;--purple:#7C3AED;--purple-bg:rgba(124,58,237,0.08);--t1:#1a1a1a;--t2:#444444;--t3:#777777;--shadow:0 12px 36px rgba(20,40,90,0.12);}
html,body{min-height:100%;background:var(--bg);font-family:var(--serif);color:var(--t1);font-size:14px;transition:background .35s,color .35s}
.bg-fx{position:fixed;inset:0;background:radial-gradient(ellipse 70% 45% at 50% -8%,rgba(249,115,22,0.13),transparent 62%),var(--bg);z-index:0;pointer-events:none}
.wrap{position:relative;z-index:10;max-width:800px;margin:0 auto;padding:24px 16px 64px}
.brand{display:flex;align-items:center;gap:12px;margin-bottom:20px}
.brand-img{width:40px;height:40px;border-radius:50%;overflow:hidden;border:1px solid var(--card-b);box-shadow:0 0 14px rgba(249,115,22,.3);flex-shrink:0;display:flex;align-items:center;justify-content:center;background:var(--bg);color:var(--accent);font-weight:900;font-size:18px}
.brand-text{font-size:18px;font-weight:800;color:var(--t1)}
.brand-text span{color:var(--accent)}
.sub-box{background:var(--card);border:1px solid var(--card-b);border-radius:18px;padding:22px 24px;margin-bottom:16px;box-shadow:var(--shadow)}
.sub-name{font-size:20px;font-weight:800;margin-bottom:4px}
.sub-desc{font-size:12px;color:var(--t3);margin-bottom:12px}
.sub-url{font-family:ui-monospace,monospace;font-size:10.5px;color:var(--accent2);word-break:break-all;background:var(--accent-d);padding:10px 14px;border-radius:10px;border:1px solid var(--card-b);display:flex;align-items:center;gap:8px;flex-wrap:wrap}
.sub-url span{flex:1;min-width:120px}
.stats{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-bottom:16px}
.stat{background:var(--card);border:1px solid var(--card-b);border-radius:14px;padding:14px 16px;text-align:center}
.stat-val{font-size:20px;font-weight:800}
.stat-label{font-size:9.5px;color:var(--t3);margin-top:4px}
.cfg-list{display:flex;flex-direction:column;gap:10px}
.cfg-item{background:var(--card);border:1px solid var(--card-b);border-radius:14px;padding:14px 18px;transition:.2s}
.cfg-item:hover{border-color:var(--card-bh)}
.cfg-head{display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:6px}
.cfg-label{font-weight:700;font-size:13.5px}
.cfg-status{font-size:10px;font-weight:700;padding:3px 10px;border-radius:20px}
.cfg-status.on{background:var(--green-bg);color:var(--green-t)}
.cfg-status.off{background:var(--red-bg);color:var(--red-t)}
.cfg-usage{font-size:10px;color:var(--t3);margin-top:6px}
.cfg-actions{display:flex;gap:6px;margin-top:8px;flex-wrap:wrap}
.btn{font-family:inherit;font-size:10.5px;font-weight:700;padding:6px 12px;border-radius:8px;border:none;cursor:pointer;display:inline-flex;align-items:center;gap:4px;transition:.15s}
.btn-p{background:linear-gradient(135deg,#F97316,#EA580C);color:#fff}
.btn-g{background:var(--accent-d);color:var(--accent2);border:1px solid rgba(249,115,22,.15)}
.btn-g:hover{background:rgba(249,115,22,.2)}
.toast{position:fixed;bottom:20px;left:50%;transform:translateX(-50%) translateY(40px);background:var(--card);border:1px solid var(--card-b);color:var(--t1);border-radius:10px;padding:8px 18px;font-size:12px;opacity:0;transition:.25s;z-index:999;box-shadow:var(--shadow);white-space:nowrap}
.toast.show{opacity:1;transform:translateX(-50%) translateY(0)}
.toast.ok{border-color:rgba(16,185,129,.3);background:var(--green-bg);color:var(--green-t)}
.empty{text-align:center;padding:50px 20px;color:var(--t3)}
.empty i{font-size:36px;opacity:.3;display:block;margin-bottom:12px}
</style>
</head>
<body>
<div class="bg-fx"></div>
<div class="toast" id="toast"></div>
<div class="wrap">
  <div class="brand">
    <div class="brand-img">TK</div>
    <div class="brand-text">TK<span>SX</span></div>
  </div>
  <div id="root">
    <div class="empty"><i class="ti ti-loader-2" style="animation:spin 1s linear infinite"></i>در حال بارگذاری...</div>
  </div>
</div>
<script>
const UUID_KEY='""" + uuid_key + """';
function esc(s){return String(s||'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));}
function fmtB(b){if(!b||b===0)return '0 B';if(b<1024)return b+' B';if(b<1024**2)return (b/1024).toFixed(1)+' KB';if(b<1024**3)return (b/1024**2).toFixed(2)+' MB';return (b/1024**3).toFixed(2)+' GB';}
function toast(msg,type=''){const t=document.getElementById('toast');t.textContent=msg;t.className='toast show'+(type?' '+type:'');setTimeout(()=>t.classList.remove('show'),2200);}
async function loadData(){const r=await fetch('/api/public/sub/'+UUID_KEY);return r.json();}
async function init(){try{const data=await loadData();if(data.locked){document.getElementById('root').innerHTML='<div class="empty"><i class="ti ti-lock"></i>این گروه با رمز محافظت شده است</div>';return}
const links=data.links||[];const active=links.filter(l=>l.active).length;const totalUsed=links.reduce((s,l)=>s+(l.used_bytes||0),0);
let html='<div class="sub-box"><div class="sub-name">' + esc(data.name) + '</div><div class="sub-desc">' + esc(data.desc||'') + '</div><div class="sub-url"><span>' + esc(data.sub_url) + '</span><button class="btn btn-g" onclick="navigator.clipboard.writeText(\'' + esc(data.sub_url) + '\').then(()=>toast(\'کپی شد ✓\',\'ok\'))"><i class="ti ti-copy"></i></button></div></div>';
html += '<div class="stats"><div class="stat"><div class="stat-val">' + active + '</div><div class="stat-label">کانفیگ فعال</div></div>';
html += '<div class="stat"><div class="stat-val">' + (data.active_connections||0) + '</div><div class="stat-label">اتصال زنده</div></div>';
html += '<div class="stat"><div class="stat-val">' + fmtB(totalUsed) + '</div><div class="stat-label">کل مصرف</div></div></div>';
html += '<div class="cfg-list">';
for (var i=0; i<links.length; i++) { var l=links[i];
    var pct = l.limit_bytes ? Math.min(100, l.used_bytes / l.limit_bytes * 100) : 0;
    var lim = l.limit_bytes ? fmtB(l.limit_bytes) : '∞';
    var statusClass = l.active ? 'on' : 'off';
    var statusText = l.active ? 'فعال' : 'غیرفعال';
    html += '<div class="cfg-item"><div class="cfg-head"><span class="cfg-label">' + esc(l.label) + '</span><span class="cfg-status ' + statusClass + '">' + statusText + '</span></div>';
    html += '<div style="font-size:10px;color:var(--t3);margin:4px 0">' + fmtB(l.used_bytes) + ' / ' + lim + '</div>';
    html += '<div class="cfg-actions"><button class="btn btn-p" onclick="navigator.clipboard.writeText(\'' + esc(l.link_url) + '\').then(()=>toast(\'کپی شد ✓\',\'ok\'))"><i class="ti ti-copy"></i> کپی</button>';
    html += '<button class="btn btn-g" onclick="window.open(\'https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=\' + encodeURIComponent(\'' + esc(l.link_url) + '\'),\'_blank\')"><i class="ti ti-qrcode"></i></button></div></div>';
}
html += '</div>';
document.getElementById('root').innerHTML = html;
} catch(e) { document.getElementById('root').innerHTML = '<div class="empty"><i class="ti ti-alert-circle"></i>خطا در بارگذاری</div>'; }}
init();
</script>
</body></html>"""
    )


# ── داشبورد پنل اصلی (کامل) ───────────────────────────────────────────────────
DASHBOARD_HTML = r"""<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>TK-SX · پنل مدیریت</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@3.19.0/dist/tabler-icons.min.css">
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.js"></script>
<style>
*{margin:0;padding:0;box-sizing:border-box}
:root{--bg:#0a0a0a;--bg2:#141414;--bg3:#1e1e1e;--card:#1a1a1a;--card-b:rgba(249,115,22,0.15);--card-bh:rgba(249,115,22,0.35);--accent:#F97316;--accent2:#FB923C;--accent-d:rgba(249,115,22,0.12);--green:#10B981;--green-bg:rgba(16,185,129,0.1);--green-t:#34D399;--red:#EF4444;--red-bg:rgba(239,68,68,0.1);--red-t:#F87171;--amber:#F59E0B;--amber-bg:rgba(245,158,11,0.1);--amber-t:#FCD34D;--purple:#9D7BF0;--purple-bg:rgba(157,123,240,0.1);--t1:#F5F5F5;--t2:#B0B0B0;--t3:#6B6B6B;--sidebar-w:248px;--radius:16px;--shadow:0 4px 24px rgba(0,0,0,0.5);}
[data-theme="light"]{--bg:#F5F5F5;--bg2:#E8E8E8;--bg3:#DCDCDC;--card:#FFFFFF;--card-b:rgba(249,115,22,0.2);--card-bh:rgba(249,115,22,0.4);--accent:#EA580C;--accent2:#F97316;--accent-d:rgba(234,88,12,0.08);--green:#059669;--green-bg:rgba(5,150,105,0.08);--green-t:#065F46;--red:#DC2626;--red-bg:rgba(220,38,38,0.08);--red-t:#991B1B;--amber:#D97706;--amber-bg:rgba(217,119,6,0.08);--amber-t:#92400E;--purple:#7C3AED;--purple-bg:rgba(124,58,237,0.08);--t1:#1a1a1a;--t2:#444444;--t3:#777777;--shadow:0 4px 20px rgba(0,0,0,0.1);}
html,body{height:100%}
body{font-family:'Vazirmatn',sans-serif;background:var(--bg);color:var(--t1);min-height:100vh;display:flex;font-size:14px;transition:background .3s,color .3s}
::-webkit-scrollbar{width:5px;height:5px}
::-webkit-scrollbar-track{background:var(--bg)}
::-webkit-scrollbar-thumb{background:var(--bg3);border-radius:3px}
a{color:inherit;text-decoration:none}
.sidebar{width:var(--sidebar-w);min-height:100vh;background:var(--bg2);border-left:1px solid var(--card-b);display:flex;flex-direction:column;flex-shrink:0;position:fixed;right:0;top:0;bottom:0;z-index:200;transition:transform .25s cubic-bezier(.4,0,.2,1),background .3s,border-color .3s}
.logo{display:flex;align-items:center;gap:12px;padding:20px 16px 16px;border-bottom:1px solid var(--card-b)}
.logo-img{width:38px;height:38px;border-radius:50%;overflow:hidden;border:1px solid var(--card-b);box-shadow:0 0 14px rgba(249,115,22,.3);flex-shrink:0;display:flex;align-items:center;justify-content:center;background:var(--bg);color:var(--accent);font-weight:900;font-size:16px}
.logo-name{font-size:13.5px;font-weight:700;color:var(--t1)}
.logo-sub{font-size:10px;color:var(--t3);margin-top:1px}
.sb-close{display:none;position:absolute;left:12px;top:20px;background:var(--accent-d);border:1px solid var(--card-b);color:var(--t2);width:30px;height:30px;border-radius:8px;font-size:16px;align-items:center;justify-content:center;cursor:pointer}
.nav-wrap{flex:1;overflow-y:auto;padding:6px 0 8px}
.nav-sec{padding:14px 14px 4px;font-size:9px;letter-spacing:.14em;text-transform:uppercase;color:var(--t3);font-weight:700}
.nav-it{display:flex;align-items:center;gap:9px;padding:9px 14px;color:var(--t3);font-size:12.5px;cursor:pointer;border-right:2px solid transparent;transition:all .15s;margin:1px 6px}
.nav-it i{font-size:16px;width:18px;text-align:center;flex-shrink:0}
.nav-it:hover{background:var(--accent-d);color:var(--t2)}
.nav-it.on{background:var(--accent-d);color:var(--t1);border-right-color:var(--accent);font-weight:600}
.nav-badge{margin-right:auto;background:rgba(249,115,22,0.15);color:var(--accent2);font-size:9px;padding:1px 6px;border-radius:20px;font-weight:700}
.sb-foot{padding:12px 14px;border-top:1px solid var(--card-b)}
.theme-btn{display:flex;align-items:center;justify-content:center;gap:7px;background:var(--accent-d);color:var(--t2);border-radius:9px;padding:8px;font-size:12px;font-weight:500;font-family:inherit;border:1px solid var(--card-b);cursor:pointer;width:100%;transition:.15s;margin-bottom:7px}
.theme-btn:hover{background:var(--card-b);color:var(--t1)}
.logout-btn{display:flex;align-items:center;justify-content:center;gap:7px;background:var(--red-bg);color:var(--red-t);border-radius:9px;padding:8px;font-size:12px;font-weight:500;font-family:inherit;border:1px solid rgba(239,68,68,0.2);cursor:pointer;width:100%;transition:.15s;margin-top:6px}
.logout-btn:hover{background:rgba(239,68,68,0.2)}
.mob-top{display:none;position:fixed;top:0;right:0;left:0;height:52px;background:var(--bg2);border-bottom:1px solid var(--card-b);z-index:150;align-items:center;justify-content:space-between;padding:0 14px}
.mob-top .ml{display:flex;align-items:center;gap:9px}
.mob-logo{width:28px;height:28px;border-radius:50%;overflow:hidden;box-shadow:0 0 8px rgba(249,115,22,.35);display:flex;align-items:center;justify-content:center;background:var(--bg);color:var(--accent);font-weight:900;font-size:14px}
.mob-title{color:var(--t1);font-size:13px;font-weight:700}
.mob-right{display:flex;gap:6px}
.menu-btn,.theme-mob{background:var(--accent-d);border:1px solid var(--card-b);color:var(--t2);width:34px;height:34px;border-radius:8px;font-size:17px;display:flex;align-items:center;justify-content:center;cursor:pointer;transition:.15s}
.overlay{display:none;position:fixed;inset:0;background:rgba(0,0,0,.55);z-index:190;backdrop-filter:blur(3px)}
.overlay.show{display:block}
.main{margin-right:var(--sidebar-w);flex:1;padding:28px 28px 60px;min-width:0;transition:margin .25s}
.pg{display:none}
.pg.on{display:block;animation:fi .2s ease}
@keyframes fi{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:none}}
.topbar{display:flex;align-items:flex-start;justify-content:space-between;margin-bottom:22px;flex-wrap:wrap;gap:12px}
.tb-title{font-size:18px;font-weight:700;color:var(--t1);display:flex;align-items:center;gap:8px;letter-spacing:-.02em}
.tb-title i{color:var(--accent);font-size:20px}
.tb-sub{font-size:11px;color:var(--t3);margin-top:4px}
.tb-right{display:flex;align-items:center;gap:8px;flex-wrap:wrap}
.badge{font-size:10px;padding:3px 10px;border-radius:20px;font-weight:700;display:inline-flex;align-items:center;gap:5px;white-space:nowrap}
.bg-green{background:var(--green-bg);color:var(--green-t)}
.bg-blue{background:var(--accent-d);color:var(--accent2)}
.bg-amber{background:var(--amber-bg);color:var(--amber-t)}
.bg-red{background:var(--red-bg);color:var(--red-t)}
.bg-purple{background:var(--purple-bg);color:#A78BFA}
.dot{width:6px;height:6px;border-radius:50%;flex-shrink:0;display:inline-block}
.dg{background:var(--green)}.dr{background:var(--red)}.da{background:var(--amber)}.db{background:var(--accent)}
.pulse{animation:pulse 2s infinite}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.25}}
.metrics{display:grid;grid-template-columns:repeat(4,1fr);gap:13px;margin-bottom:18px}
.metric{background:var(--card);border:1px solid var(--card-b);border-radius:var(--radius);padding:17px 17px 14px;transition:all .2s;position:relative;overflow:hidden;cursor:default}
.metric::after{content:'';position:absolute;top:0;right:0;width:3px;height:100%;background:var(--accent);opacity:0;transition:.2s}
.metric:hover{border-color:var(--card-bh);transform:translateY(-2px);box-shadow:var(--shadow)}
.metric:hover::after{opacity:1}
.metric.suc::after{background:var(--green)}
.metric.dan::after{background:var(--red)}
.m-icon{width:34px;height:34px;border-radius:8px;background:var(--accent-d);display:flex;align-items:center;justify-content:center;margin-bottom:11px;color:var(--accent);font-size:17px}
.m-icon.suc{background:var(--green-bg);color:var(--green)}
.m-icon.dan{background:var(--red-bg);color:var(--red)}
.m-icon.pur{background:var(--purple-bg);color:var(--purple)}
.m-label{font-size:10px;color:var(--t3);margin-bottom:4px;font-weight:600;text-transform:uppercase;letter-spacing:.05em}
.m-val{font-size:25px;font-weight:700;color:var(--t1);line-height:1;letter-spacing:-.02em}
.m-unit{font-size:12px;font-weight:400;color:var(--t3)}
.m-sub{font-size:10px;color:var(--t3);margin-top:6px;display:flex;align-items:center;gap:3px}
.vless-box{background:linear-gradient(135deg,var(--bg3) 0%,var(--bg2) 100%);border:1px solid var(--card-b);border-radius:18px;padding:20px 22px;margin-bottom:18px;box-shadow:var(--shadow);position:relative;overflow:hidden}
.vless-box::before{content:'';position:absolute;top:-50px;left:-50px;width:180px;height:180px;background:radial-gradient(circle,var(--accent-d),transparent 70%);pointer-events:none}
.vl-header{display:flex;align-items:center;justify-content:space-between;margin-bottom:13px;flex-wrap:wrap;gap:8px}
.vl-title{color:var(--t2);font-size:11px;display:flex;align-items:center;gap:6px;font-weight:700;text-transform:uppercase;letter-spacing:.06em}
.vl-title i{color:var(--accent);font-size:15px}
.vl-code{background:rgba(0,0,0,.18);border:1px solid var(--card-b);border-radius:9px;padding:13px 15px;font-size:11px;font-family:ui-monospace,monospace;color:var(--accent2);word-break:break-all;line-height:1.8}
[data-theme="light"] .vl-code{background:rgba(0,0,0,.04)}
.vl-actions{display:flex;gap:8px;margin-top:13px;flex-wrap:wrap}
.btn{font-family:inherit;font-size:12px;font-weight:500;border-radius:9px;padding:8px 14px;cursor:pointer;display:inline-flex;align-items:center;gap:5px;border:none;transition:all .15s;white-space:nowrap}
.btn i{font-size:13px}
.btn:disabled{opacity:.4;cursor:not-allowed}
.btn-p{background:linear-gradient(135deg,#F97316,#EA580C);color:#fff;box-shadow:0 2px 14px rgba(249,115,22,.35)}
.btn-p:hover{background:#EA580C;box-shadow:0 4px 18px rgba(249,115,22,.4)}
.btn-o{background:transparent;border:1px solid var(--card-b);color:var(--t2)}
.btn-o:hover{background:var(--accent-d);border-color:rgba(249,115,22,.3)}
.btn-g{background:var(--accent-d);color:var(--accent2);border:1px solid rgba(249,115,22,.15)}
.btn-g:hover{background:rgba(249,115,22,.22)}
.btn-d{background:var(--red-bg);color:var(--red-t);border:1px solid rgba(239,68,68,.2)}
.btn-d:hover{background:rgba(239,68,68,.2)}
.btn-pur{background:var(--purple-bg);color:#A78BFA;border:1px solid rgba(157,123,240,.2)}
.btn-pur:hover{background:rgba(157,123,240,.22)}
.btn-sm{padding:5px 9px;font-size:10.5px;border-radius:7px}
.btn-icon{width:30px;height:30px;padding:0;justify-content:center;border-radius:5px}
.card{background:var(--card);border:1px solid var(--card-b);border-radius:var(--radius);padding:18px 20px;transition:border-color .2s,background .3s}
.card:hover{border-color:var(--card-bh)}
.card-title{font-size:12.5px;font-weight:700;color:var(--t1);margin-bottom:15px;display:flex;align-items:center;gap:7px}
.card-title i{font-size:16px;color:var(--accent)}
.ml-auto{margin-right:auto}
.g2{display:grid;grid-template-columns:1fr 1fr;gap:13px;margin-bottom:16px}
.g3{display:grid;grid-template-columns:2fr 1fr;gap:13px;margin-bottom:16px}
.mb16{margin-bottom:16px}
.sr{display:flex;align-items:center;justify-content:space-between;padding:9px 0;border-bottom:1px solid rgba(249,115,22,0.05);font-size:12px}
.sr:last-child{border-bottom:none}
.sr-k{color:var(--t2);display:flex;align-items:center;gap:6px}
.sr-k i{font-size:13px;color:var(--t3)}
.sr-v{color:var(--t1);font-weight:600;font-size:11.5px}
.ch{position:relative;height:230px}
.ch-lg{position:relative;height:330px}
.ch-sm{position:relative;height:185px}
.spbar{height:4px;border-radius:3px;background:var(--accent-d);margin-top:5px;overflow:hidden}
.spfill{height:100%;border-radius:3px;background:linear-gradient(90deg,var(--accent),var(--accent2));transition:width 1s}
.exp-chip{font-size:9px;padding:3px 8px;border-radius:6px;font-weight:700;display:inline-flex;align-items:center;gap:3px}
.ec-ok{background:var(--green-bg);color:var(--green-t)}
.ec-warn{background:var(--amber-bg);color:var(--amber-t)}
.ec-exp{background:var(--red-bg);color:var(--red-t)}
.ec-inf{background:var(--accent-d);color:var(--accent2)}
.tog{width:19px;height:34px;border-radius:19px;background:rgba(100,116,139,0.25);position:relative;cursor:pointer;transition:.2s;flex-shrink:0;border:none}
.tog::after{content:'';position:absolute;width:13px;height:13px;border-radius:50%;background:#fff;left:3px;bottom:3px;transition:.2s;box-shadow:0 1px 3px rgba(0,0,0,.3)}
.tog.on{background:var(--green)}
.tog.on::after{bottom:18px}
.create-panel{background:linear-gradient(155deg,var(--bg3) 0%,var(--card) 55%);border:1px solid var(--card-b);border-radius:22px;padding:0;overflow:hidden;box-shadow:var(--shadow);margin-bottom:16px;position:relative}
.create-panel::before{content:'';position:absolute;top:-60px;left:-60px;width:220px;height:220px;background:radial-gradient(circle,var(--accent-d),transparent 70%);pointer-events:none}
.cp-head{display:flex;align-items:center;gap:13px;padding:22px 24px 18px;position:relative;z-index:1}
.cp-head-icon{width:44px;height:44px;border-radius:13px;background:linear-gradient(135deg,var(--accent),var(--accent2));display:flex;align-items:center;justify-content:center;color:#fff;font-size:20px;flex-shrink:0;box-shadow:0 6px 18px rgba(249,115,22,.35)}
.cp-head-text{flex:1;min-width:0}
.cp-head-title{font-size:15px;font-weight:800;color:var(--t1);letter-spacing:-.01em}
.cp-head-sub{font-size:11px;color:var(--t3);margin-top:2px}
.cp-body{padding:2px 24px 22px;position:relative;z-index:1}
.cp-row{display:grid;grid-template-columns:1.3fr 1fr;gap:14px;margin-bottom:16px}
.cp-block{background:rgba(0,0,0,.14);border:1px solid var(--card-b);border-radius:14px;padding:14px 16px}
[data-theme="light"] .cp-block{background:rgba(234,88,12,.03)}
.cp-block-label{font-size:10px;font-weight:800;color:var(--t2);text-transform:uppercase;letter-spacing:.08em;display:flex;align-items:center;gap:6px;margin-bottom:11px}
.cp-block-label i{color:var(--accent);font-size:14px}
.cp-input-full{width:100%;padding:10px 13px;border-radius:10px;border:1px solid var(--card-b);background:rgba(0,0,0,.18);color:var(--t1);font-family:inherit;font-size:12.5px;outline:none;transition:.15s}
[data-theme="light"] .cp-input-full{background:#fff}
.cp-input-full:focus{border-color:rgba(249,115,22,.5);box-shadow:0 0 0 3px rgba(249,115,22,.1)}
.cp-input-full::placeholder{color:var(--t3)}
.cp-mini-row{display:flex;gap:8px;margin-top:9px}
.cp-quota-inputs{display:flex;gap:8px}
.cp-quota-inputs .cp-input-full{flex:1}
.cp-quota-inputs select.cp-input-full{flex:0 0 76px}
.chip-row{display:flex;gap:6px;flex-wrap:wrap;margin-top:9px}
.chip{font-size:10.5px;font-weight:700;padding:5px 12px;border-radius:8px;background:var(--accent-d);color:var(--t2);border:1px solid var(--card-b);cursor:pointer;transition:.15s;white-space:nowrap}
.chip:hover{background:rgba(249,115,22,.18);color:var(--accent2)}
.chip.active{background:var(--accent);color:#fff;border-color:var(--accent);box-shadow:0 3px 10px rgba(249,115,22,.35)}
.proto-cards{display:grid;grid-template-columns:repeat(3,1fr);gap:9px}
.proto-card{border:1.5px solid var(--card-b);border-radius:13px;padding:13px 12px;cursor:pointer;transition:.18s;text-align:center;position:relative;background:rgba(0,0,0,.1)}
[data-theme="light"] .proto-card{background:#fff}
.proto-card:hover{border-color:var(--card-bh);transform:translateY(-1px)}
.proto-card.active{border-color:var(--accent);background:var(--accent-d);box-shadow:0 0 0 3px rgba(249,115,22,.1)}
.proto-card.active .proto-card-check{opacity:1;transform:scale(1)}
.proto-card-check{position:absolute;top:7px;left:7px;width:16px;height:16px;border-radius:50%;background:var(--accent);color:#fff;font-size:10px;display:flex;align-items:center;justify-content:center;opacity:0;transform:scale(.5);transition:.18s}
.proto-card-icon{width:32px;height:32px;border-radius:9px;background:var(--accent-d);color:var(--accent);display:flex;align-items:center;justify-content:center;font-size:16px;margin:0 auto 8px}
.proto-card.active .proto-card-icon{background:var(--accent);color:#fff}
.proto-card-title{font-size:11px;font-weight:800;color:var(--t1)}
.proto-card-desc{font-size:9px;color:var(--t3);margin-top:3px;line-height:1.5}
.cp-footer{display:flex;align-items:center;justify-content:space-between;gap:12px;padding-top:16px;border-top:1px solid var(--card-b);flex-wrap:wrap}
.cp-footer-note{display:flex;align-items:center;gap:8px;font-size:10.5px;color:var(--t3);line-height:1.7;flex:1;min-width:220px}
.cp-footer-note i{color:var(--accent);font-size:15px;flex-shrink:0}
.cp-submit-btn{background:linear-gradient(135deg,var(--accent),var(--accent2));color:#fff;border:none;border-radius:13px;padding:13px 26px;font-family:inherit;font-size:13px;font-weight:800;cursor:pointer;display:flex;align-items:center;gap:8px;box-shadow:0 6px 20px rgba(249,115,22,.35);transition:.18s;white-space:nowrap}
.cp-submit-btn:hover{transform:translateY(-2px);box-shadow:0 10px 26px rgba(249,115,22,.45)}
.cp-submit-btn:active{transform:translateY(0) scale(.98)}
@media(max-width:760px){
  .cp-row{grid-template-columns:1fr}
  .proto-cards{grid-template-columns:1fr}
  .cp-footer{flex-direction:column;align-items:stretch}
  .cp-submit-btn{justify-content:center}
}
.empty{text-align:center;padding:50px 20px;color:var(--t3)}
.empty i{font-size:40px;opacity:.3;margin-bottom:12px;display:block}
.empty p{font-size:12.5px;margin-top:4px}
.cfg-grid{display:flex;flex-direction:column;gap:10px}
.cfg-card{background:var(--card);border:1px solid var(--card-b);border-radius:14px;padding:0;transition:all .2s;position:relative;overflow:hidden}
.cfg-card:hover{border-color:var(--card-bh);box-shadow:0 6px 24px rgba(0,0,0,.18)}
.cfg-card.is-off{opacity:.6}
.cfg-card.is-exp{opacity:.78}
.cfg-row{display:flex;align-items:center;gap:16px;padding:14px 18px;flex-wrap:wrap}
.cfg-status-dot{width:9px;height:9px;border-radius:50%;background:var(--green);flex-shrink:0;box-shadow:0 0 0 3px var(--green-bg)}
.cfg-card.is-off .cfg-status-dot{background:var(--red);box-shadow:0 0 0 3px var(--red-bg)}
.cfg-card.is-exp .cfg-status-dot{background:var(--amber);box-shadow:0 0 0 3px var(--amber-bg)}
.cfg-identity{display:flex;flex-direction:column;gap:3px;min-width:150px;flex-shrink:0}
.cfg-label{font-size:13.5px;font-weight:700;color:var(--t1);display:flex;align-items:center;gap:7px}
.cfg-sub-meta{display:flex;align-items:center;gap:8px;font-size:10px;color:var(--t3)}
.cfg-uuid-mini{font-family:ui-monospace,monospace;font-size:9.5px;color:var(--accent2);background:var(--accent-d);padding:2px 7px;border-radius:5px;cursor:pointer}
.cfg-divider-v{width:1px;align-self:stretch;background:var(--card-b);flex-shrink:0}
.cfg-usage-col{flex:1;min-width:160px;display:flex;flex-direction:column;gap:5px}
.ubar{height:5px;border-radius:4px;background:rgba(249,115,22,0.1);overflow:hidden}
.ubar-f{height:100%;border-radius:4px;transition:width .4s ease}
.utxt{font-size:10px;color:var(--t3);display:flex;justify-content:space-between}
.cfg-exp-col{flex-shrink:0;min-width:110px}
.cfg-badges-col{display:flex;flex-direction:column;gap:5px;flex-shrink:0;align-items:flex-end}
.cfg-actions{display:flex;gap:5px;flex-shrink:0;flex-wrap:wrap}
.proto-chip{font-size:9px;padding:3px 8px;border-radius:6px;font-weight:700;white-space:nowrap}
.pc-ws{background:var(--accent-d);color:var(--accent2)}
.pc-xhttp{background:var(--purple-bg);color:#A78BFA}
.pc-ultra{background:var(--green-bg);color:var(--green-t)}
.cfg-sub-tag{font-size:9.5px;color:var(--t3);display:flex;align-items:center;gap:4px;white-space:nowrap}
.cfg-sub-tag i{color:var(--purple);font-size:11px}
.toast{position:fixed;bottom:22px;left:50%;transform:translateX(-50%) translateY(40px);background:var(--card);border:1px solid var(--card-b);color:var(--t1);border-radius:10px;padding:10px 18px;font-size:12.5px;opacity:0;transition:all .25s;z-index:999;pointer-events:none;display:flex;align-items:center;gap:8px;box-shadow:var(--shadow);white-space:nowrap}
.toast.show{opacity:1;transform:translateX(-50%) translateY(0)}
.toast.ok{border-color:rgba(16,185,129,.3);background:var(--green-bg);color:var(--green-t)}
.toast.err{border-color:rgba(239,68,68,.3);background:var(--red-bg);color:var(--red-t)}
.modal-bg{display:none;position:fixed;inset:0;background:rgba(0,0,0,.6);z-index:500;align-items:center;justify-content:center;backdrop-filter:blur(4px)}
.modal-bg.open{display:flex}
.modal{background:var(--card);border:1px solid var(--card-b);border-radius:20px;padding:28px 26px;max-width:520px;width:calc(100% - 32px);max-height:90vh;overflow-y:auto;position:relative;animation:fi .2s ease}
.modal-close{position:absolute;top:14px;left:14px;background:var(--accent-d);border:1px solid var(--card-b);color:var(--t2);width:30px;height:30px;border-radius:8px;font-size:16px;display:flex;align-items:center;justify-content:center;cursor:pointer;border:none}
.modal-title{font-size:16px;font-weight:700;color:var(--t1);margin-bottom:18px;display:flex;align-items:center;gap:8px}
.modal-title i{color:var(--accent)}
.modal-v2{background:var(--card);border:1px solid var(--card-b);border-radius:22px;padding:0;max-width:430px;width:calc(100% - 32px);max-height:92vh;overflow-y:auto;position:relative;animation:fi .2s ease;box-shadow:0 24px 70px rgba(0,0,0,.5)}
.modal-v2-head{background:linear-gradient(155deg,rgba(157,123,240,.14) 0%,transparent 65%);padding:18px 22px 14px;position:relative;overflow:hidden}
.modal-v2-close{position:absolute;top:14px;left:14px;background:var(--accent-d);border:1px solid var(--card-b);color:var(--t2);width:30px;height:30px;border-radius:9px;font-size:15px;display:flex;align-items:center;justify-content:center;cursor:pointer;z-index:2;transition:.15s}
.modal-v2-close:hover{background:var(--red-bg);color:var(--red-t);border-color:rgba(239,68,68,.25)}
.modal-v2-icon{width:42px;height:42px;border-radius:13px;background:linear-gradient(135deg,var(--purple),#6D48D6);display:flex;align-items:center;justify-content:center;color:#fff;font-size:19px;margin-bottom:10px;position:relative;z-index:1;box-shadow:0 8px 18px rgba(157,123,240,.4)}
.modal-v2-title{font-size:15.5px;font-weight:800;color:var(--t1);position:relative;z-index:1;letter-spacing:-.01em}
.modal-v2-sub{font-size:10.5px;color:var(--t3);margin-top:3px;position:relative;z-index:1;line-height:1.6}
.modal-v2-body{padding:16px 22px 20px;border-top:1px solid var(--card-b)}
.modal-v2-field{margin-bottom:11px}
.modal-v2-field label{display:flex;align-items:center;gap:5px;font-size:9.5px;font-weight:800;color:var(--t2);text-transform:uppercase;letter-spacing:.06em;margin-bottom:6px}
.modal-v2-field label i{color:var(--purple);font-size:13px}
.modal-v2-input{width:100%;padding:9px 38px 9px 13px;border-radius:11px;border:1px solid var(--card-b);background:rgba(0,0,0,.2);color:var(--t1);font-family:inherit;font-size:12.5px;outline:none;transition:.18s}
.modal-v2-input:focus{border-color:rgba(157,123,240,.55);box-shadow:0 0 0 3px rgba(157,123,240,.12)}
.modal-v2-footer{display:flex;gap:8px;margin-top:15px}
.modal-v2-btn-cancel{flex:.75;justify-content:center;padding:10px;border-radius:11px;background:transparent;border:1px solid var(--card-b);color:var(--t2);font-family:inherit;font-size:12px;font-weight:700;cursor:pointer;transition:.15s;display:flex;align-items:center}
.modal-v2-btn-cancel:hover{background:var(--accent-d);color:var(--t1)}
.modal-v2-btn-submit{flex:1;justify-content:center;padding:10px;border-radius:11px;background:linear-gradient(135deg,var(--purple),#6D48D6);color:#fff;border:none;font-family:inherit;font-size:12px;font-weight:800;cursor:pointer;display:flex;align-items:center;gap:6px;box-shadow:0 6px 18px rgba(157,123,240,.4);transition:.18s}
.modal-v2-btn-submit:hover{transform:translateY(-2px);box-shadow:0 10px 24px rgba(157,123,240,.5)}
@media(max-width:1050px){
  .sidebar{transform:translateX(100%)}
  .sidebar.open{transform:translateX(0);box-shadow:-10px 0 40px rgba(0,0,0,.4)}
  .sb-close{display:flex}
  .main{margin-right:0;padding-top:70px}
  .mob-top{display:flex}
  .metrics{grid-template-columns:1fr 1fr}
  .g2,.g3{grid-template-columns:1fr}
}
@media(max-width:500px){
  .metrics{grid-template-columns:1fr}
  .main{padding:62px 12px 50px}
}
</style>
</head>
<body>
<div class="toast" id="toast"></div>
<div class="modal-bg" id="modal-links"><div class="modal-v2"><div class="modal-v2-head"><button class="modal-v2-close" onclick="closeModal('modal-links')"><i class="ti ti-x"></i></button><div class="modal-v2-icon"><i class="ti ti-link-plus"></i></div><div class="modal-v2-title">مدیریت کانفیگ‌های <span id="modal-sub-name">—</span></div><div class="modal-v2-sub">کانفیگ‌هایی که می‌خواهید در این گروه باشند را انتخاب کنید</div></div><div class="modal-v2-body" id="modal-links-body"></div><div class="modal-v2-footer"><button class="modal-v2-btn-cancel" onclick="closeModal('modal-links')">بستن</button><button class="modal-v2-btn-submit" onclick="saveSubLinks()"><i class="ti ti-check"></i> ذخیره</button></div></div></div>
<div class="modal-bg" id="modal-create-sub"><div class="modal-v2"><div class="modal-v2-head"><button class="modal-v2-close" onclick="closeModal('modal-create-sub')"><i class="ti ti-x"></i></button><div class="modal-v2-icon"><i class="ti ti-folder-plus"></i></div><div class="modal-v2-title">ساخت گروه جدید</div><div class="modal-v2-sub">یک صفحه پابلیک مجزا برای مدیریت کانفیگ‌ها بسازید</div></div><div class="modal-v2-body"><div class="modal-v2-field"><label><i class="ti ti-tag"></i> نام گروه</label><input class="modal-v2-input" id="ns-name" placeholder="مثلاً: کانال تلگرام"></div><div class="modal-v2-field"><label><i class="ti ti-align-left"></i> توضیحات</label><input class="modal-v2-input" id="ns-desc" placeholder="توضیح کوتاه"></div><div class="modal-v2-field"><label><i class="ti ti-lock"></i> رمز صفحه</label><input class="modal-v2-input" id="ns-pw" type="password" placeholder="خالی = بدون رمز"></div><div class="modal-v2-footer"><button class="modal-v2-btn-cancel" onclick="closeModal('modal-create-sub')">انصراف</button><button class="modal-v2-btn-submit" onclick="createSub()"><i class="ti ti-folder-plus"></i> ساخت</button></div></div></div></div>
<div class="modal-bg" id="modal-edit-link"><div class="modal"><button class="modal-close" onclick="closeModal('modal-edit-link')"><i class="ti ti-x"></i></button><div class="modal-title"><i class="ti ti-edit"></i> ویرایش کانفیگ</div><input type="hidden" id="el-uuid"><div class="fg" style="margin-bottom:13px"><label>عنوان</label><input class="fi" id="el-label" style="width:100%"></div><div class="form-row" style="margin-bottom:13px"><div class="fg" style="flex:1"><label>سهمیه</label><input class="fi" id="el-val" type="number" min="0" step="0.1" style="width:100%"></div><div class="fg"><label>واحد</label><select class="fs" id="el-unit"><option value="GB">GB</option><option value="MB">MB</option></select></div></div><div class="fg" style="margin-bottom:13px"><label>انقضا (روز از الان)</label><input class="fi" id="el-exp" type="number" min="0" step="1" style="width:100%"></div><div class="fg" style="margin-bottom:13px"><label>یادداشت</label><input class="fi" id="el-note" style="width:100%"></div><div class="form-row" style="margin-bottom:13px"><div class="fg" style="flex:1"><label>Fingerprint</label><select class="fs" id="el-fp"><option value="chrome">chrome</option><option value="firefox">firefox</option><option value="safari">safari</option><option value="ios">ios</option><option value="android">android</option><option value="edge">edge</option><option value="360">360</option><option value="qq">qq</option><option value="random">random</option></select></div><div class="fg" style="flex:1"><label>ALPN</label><input class="fi" id="el-alpn" placeholder="h2,http/1.1" style="width:100%"></div></div><div class="form-row" style="margin-bottom:16px"><div class="fg" style="flex:1"><label>پورت</label><input class="fi" id="el-port" type="number" min="1" max="65535" style="width:100%"></div><div class="fg" style="flex:1"><label>محدودیت آی‌پی</label><input class="fi" id="el-iplimit" type="number" min="0" step="1" style="width:100%"></div></div><div class="form-row" style="margin-bottom:16px"><div class="fg" style="flex:1"><label>محدودیت سرعت</label><input class="fi" id="el-speed" type="number" min="0" step="0.5" style="width:100%"></div><div class="fg"><label>واحد</label><select class="fs" id="el-speed-unit"><option value="MBIT">Mbps</option><option value="KB">KB/s</option><option value="MB">MB/s</option></select></div></div><div style="margin-top:16px;display:flex;gap:8px;justify-content:flex-end"><button class="btn btn-o" onclick="closeModal('modal-edit-link')">انصراف</button><button class="btn btn-p" onclick="saveEditLink()"><i class="ti ti-check"></i> ذخیره</button></div></div></div>
<div class="mob-top"><div class="ml"><div class="mob-logo">TK</div><span class="mob-title">TK-SX</span></div><div class="mob-right"><button class="theme-mob" id="theme-mob-btn" onclick="toggleTheme()"><i class="ti ti-sun" id="theme-mob-icon"></i></button><button class="menu-btn" id="open-sb"><i class="ti ti-menu-2"></i></button></div></div>
<div class="overlay" id="overlay"></div>
<aside class="sidebar" id="sb"><button class="sb-close" id="close-sb"><i class="ti ti-x"></i></button><div class="logo"><div class="logo-img">TK</div><div><div class="logo-name">TK-SX</div><div class="logo-sub">v3.0</div></div></div><div class="nav-wrap"><div class="nav-sec">پنل</div><div class="nav-it on" data-pg="overview"><i class="ti ti-layout-dashboard"></i> داشبورد</div><div class="nav-it" data-pg="links"><i class="ti ti-link-plus"></i> کانفیگ‌ها <span class="nav-badge" id="links-nb">0</span></div><div class="nav-it" data-pg="subgroups"><i class="ti ti-folders"></i> گروه‌های ساب <span class="nav-badge" id="subs-nb">0</span></div><div class="nav-it" data-pg="subscriptions"><i class="ti ti-rss"></i> سابسکریپشن</div><div class="nav-it" data-pg="traffic"><i class="ti ti-chart-area"></i> ترافیک</div><div class="nav-it" data-pg="connections"><i class="ti ti-plug-connected"></i> اتصالات <span class="nav-badge" id="conns-nb">0</span></div><div class="nav-it" data-pg="bot"><i class="ti ti-robot"></i> ربات</div><div class="nav-sec">سیستم</div><div class="nav-it" data-pg="security"><i class="ti ti-shield-lock"></i> امنیت</div><div class="nav-it" data-pg="logs"><i class="ti ti-history"></i> لاگ</div><div class="nav-it" data-pg="errors"><i class="ti ti-alert-triangle"></i> خطاها</div><div class="nav-it" data-pg="settings"><i class="ti ti-settings"></i> تنظیمات</div><div class="nav-it" data-pg="support"><i class="ti ti-headset"></i> پشتیبانی</div></div><div class="sb-foot"><button class="theme-btn" onclick="toggleTheme()"><i class="ti ti-moon" id="theme-icon"></i> <span id="theme-label">تم روشن</span></button><button class="logout-btn" id="logout-btn"><i class="ti ti-logout"></i> خروج</button></div></aside>
<main class="main">
<section class="pg on" id="pg-overview"><div class="topbar"><div><div class="tb-title"><i class="ti ti-layout-dashboard"></i> داشبورد</div><div class="tb-sub" id="last-upd">در حال بارگذاری...</div></div><div class="tb-right"><span class="badge bg-green"><span class="dot dg pulse"></span> فعال</span><span class="badge bg-blue" id="uptime-badge">—</span><button class="btn btn-p btn-sm" onclick="refreshAll()"><i class="ti ti-refresh"></i> رفرش</button></div></div>
<div class="metrics"><div class="metric"><div class="m-icon"><i class="ti ti-plug-connected"></i></div><div class="m-label">اتصالات فعال</div><div class="m-val" id="m-conns">—</div></div><div class="metric"><div class="m-icon"><i class="ti ti-transfer"></i></div><div class="m-label">کل ترافیک</div><div class="m-val" id="m-traffic">—<span class="m-unit">MB</span></div></div><div class="metric suc"><div class="m-icon suc"><i class="ti ti-link"></i></div><div class="m-label">کانفیگ فعال</div><div class="m-val" id="m-alinks">—</div></div><div class="metric pur"><div class="m-icon pur"><i class="ti ti-folders"></i></div><div class="m-label">گروه‌های ساب</div><div class="m-val" id="m-subs">—</div></div></div>
<div class="vless-box"><div class="vl-header"><div class="vl-title"><i class="ti ti-link"></i> لینک پیش‌فرض</div><span class="badge bg-blue"><span class="dot db"></span> TLS 443 · WS</span></div><div class="vl-code" id="vless-main">در حال دریافت...</div><div class="vl-actions"><button class="btn btn-p" onclick="cpText('vless-main')"><i class="ti ti-copy"></i> کپی</button><button class="btn btn-g" onclick="qrFor('vless-main')"><i class="ti ti-qrcode"></i> QR</button><button class="btn btn-o" onclick="navTo('links')"><i class="ti ti-link-plus"></i> کانفیگ‌ها</button></div></div>
<div class="g3"><div class="card"><div class="card-title"><i class="ti ti-chart-area"></i> ترافیک ساعتی</div><div class="ch"><canvas id="ch1"></canvas></div></div><div class="card"><div class="card-title"><i class="ti ti-chart-donut"></i> توزیع</div><div class="ch-sm"><canvas id="ch2"></canvas></div></div></div>
<div class="g2"><div class="card"><div class="card-title"><i class="ti ti-activity"></i> وضعیت سرویس</div><div class="sr"><span class="sr-k"><i class="ti ti-shield-check"></i> UUID Auth</span><span class="sr-v" style="color:var(--green-t)">● فعال</span></div><div class="sr"><span class="sr-k"><i class="ti ti-circle-check"></i> VLESS / WS</span><span class="sr-v" style="color:var(--green-t)">● فعال</span></div><div class="sr"><span class="sr-k"><i class="ti ti-bolt"></i> XHTTP Ultra</span><span class="sr-v" style="color:var(--green-t)">● فعال</span></div><div class="sr"><span class="sr-k"><i class="ti ti-folders"></i> Sub Groups</span><span class="sr-v" style="color:var(--green-t)">● فعال</span></div><div class="sr"><span class="sr-k"><i class="ti ti-rss"></i> Subscription</span><span class="sr-v" style="color:var(--green-t)">● فعال</span></div><div class="sr"><span class="sr-k"><i class="ti ti-clock"></i> آپتایم</span><span class="sr-v" id="uptime-inline">—</span></div></div><div class="card"><div class="card-title"><i class="ti ti-list"></i> خلاصه کانفیگ‌ها <span class="ml-auto badge bg-blue" id="lsummary-badge">۰</span></div><div id="lsummary">—</div></div></div></section>
<section class="pg" id="pg-links"><div class="topbar"><div><div class="tb-title"><i class="ti ti-link-plus"></i> کانفیگ‌ها</div><div class="tb-sub">ساخت و مدیریت کانفیگ با سهمیه، انقضا و گروه‌بندی</div></div><div class="tb-right"><span class="badge bg-blue" id="links-pg-cnt">۰ کانفیگ</span></div></div>
<div class="create-panel"><div class="cp-head"><div class="cp-head-icon"><i class="ti ti-square-rounded-plus"></i></div><div class="cp-head-text"><div class="cp-head-title">ساخت کانفیگ جدید</div><div class="cp-head-sub">UUID تصادفی · سهمیه، انقضا و پروتکل</div></div></div><div class="cp-body"><div class="cp-row"><div class="cp-block"><div class="cp-block-label"><i class="ti ti-id-badge-2"></i> شناسه</div><input class="cp-input-full" id="nl-label" placeholder="مثلاً: کاربر علی"><div class="cp-mini-row"><input class="cp-input-full" id="nl-note" placeholder="یادداشت (اختیاری)"></div></div><div class="cp-block"><div class="cp-block-label"><i class="ti ti-folders"></i> گروه و انقضا</div><select class="cp-input-full fs" id="nl-sub"><option value="">— بدون گروه —</option></select><div class="cp-mini-row"><input class="cp-input-full" id="nl-exp" type="number" min="0" step="1" placeholder="انقضا (روز) · 0 = نامحدود"></div><div class="chip-row"><span class="chip" onclick="setExpiry(0,this)">نامحدود</span><span class="chip" onclick="setExpiry(7,this)">۷ روز</span><span class="chip active" onclick="setExpiry(30,this)">۳۰ روز</span><span class="chip" onclick="setExpiry(90,this)">۹۰ روز</span></div></div></div>
<div class="cp-block mb16"><div class="cp-block-label"><i class="ti ti-gauge"></i> سهمیه ترافیک</div><div class="cp-quota-inputs"><input class="cp-input-full" id="nl-val" type="number" min="0" step="0.1" placeholder="0 = نامحدود"><select class="cp-input-full fs" id="nl-unit"><option value="GB">GB</option><option value="MB" selected>MB</option></select></div><div class="chip-row"><span class="chip" onclick="setQuota(0,'GB',this)">نامحدود</span><span class="chip" onclick="setQuota(500,'MB',this)">۵۰۰ MB</span><span class="chip active" onclick="setQuota(1,'GB',this)">۱ GB</span><span class="chip" onclick="setQuota(5,'GB',this)">۵ GB</span><span class="chip" onclick="setQuota(10,'GB',this)">۱۰ GB</span><span class="chip" onclick="setQuota(50,'GB',this)">۵۰ GB</span></div></div>
<div class="cp-block mb16"><div class="cp-block-label"><i class="ti ti-plug-connected"></i> پروتکل</div><select id="nl-proto" style="display:none"><option value="vless">VLESS</option><option value="vmess">VMess</option><option value="trojan">Trojan</option><option value="shadowsocks">Shadowsocks</option><option value="socks5">SOCKS5</option><option value="http">HTTP</option><option value="wireguard">WireGuard</option><option value="hysteria2">Hysteria2</option><option value="tun">TUN</option><option value="dokodemo">Dokodemo-door</option><option value="snell">Snell</option></select><div class="proto-cards"><div class="proto-card active" data-val="vless" onclick="selectProto('vless',this)"><div class="proto-card-check"><i class="ti ti-check"></i></div><div class="proto-card-icon"><i class="ti ti-link"></i></div><div class="proto-card-title">VLESS</div><div class="proto-card-desc">پایدار و همه‌منظوره</div></div><div class="proto-card" data-val="vmess" onclick="selectProto('vmess',this)"><div class="proto-card-check"><i class="ti ti-check"></i></div><div class="proto-card-icon"><i class="ti ti-shield"></i></div><div class="proto-card-title">VMess</div><div class="proto-card-desc">استاندارد V2Ray</div></div><div class="proto-card" data-val="trojan" onclick="selectProto('trojan',this)"><div class="proto-card-check"><i class="ti ti-check"></i></div><div class="proto-card-icon"><i class="ti ti-shield-lock"></i></div><div class="proto-card-title">Trojan</div><div class="proto-card-desc">شبیه‌سازی HTTPS</div></div><div class="proto-card" data-val="shadowsocks" onclick="selectProto('shadowsocks',this)"><div class="proto-card-check"><i class="ti ti-check"></i></div><div class="proto-card-icon"><i class="ti ti-lock"></i></div><div class="proto-card-title">Shadowsocks</div><div class="proto-card-desc">سبک و سریع</div></div><div class="proto-card" data-val="wireguard" onclick="selectProto('wireguard',this)"><div class="proto-card-check"><i class="ti ti-check"></i></div><div class="proto-card-icon"><i class="ti ti-vpn"></i></div><div class="proto-card-title">WireGuard</div><div class="proto-card-desc">UDP over TCP فعال</div></div><div class="proto-card" data-val="hysteria2" onclick="selectProto('hysteria2',this)"><div class="proto-card-check"><i class="ti ti-check"></i></div><div class="proto-card-icon"><i class="ti ti-rocket"></i></div><div class="proto-card-title">Hysteria2</div><div class="proto-card-desc">UDP over TCP فعال</div></div></div></div>
<div class="cp-row"><div class="cp-block"><div class="cp-block-label"><i class="ti ti-fingerprint"></i> Fingerprint</div><select class="cp-input-full fs" id="nl-fp"><option value="chrome" selected>chrome</option><option value="firefox">firefox</option><option value="safari">safari</option><option value="ios">ios</option><option value="android">android</option><option value="edge">edge</option><option value="360">360</option><option value="qq">qq</option><option value="random">random</option></select></div><div class="cp-block"><div class="cp-block-label"><i class="ti ti-antenna-bars-5"></i> ALPN</div><select class="cp-input-full fs" id="nl-alpn-preset" onchange="onAlpnPresetChange()"><option value="">پیش‌فرض</option><option value="h2,http/1.1">h2,http/1.1</option><option value="http/1.1">http/1.1</option><option value="h2">h2</option><option value="__custom__">دستی...</option></select><div class="cp-mini-row"><input class="cp-input-full" id="nl-alpn" placeholder="مقدار دستی ALPN" style="display:none"></div></div></div>
<div class="cp-row mb16"><div class="cp-block"><div class="cp-block-label"><i class="ti ti-route"></i> پورت</div><input class="cp-input-full" id="nl-port" type="number" min="1" max="65535" placeholder="443" value="443"></div><div class="cp-block"><div class="cp-block-label"><i class="ti ti-users"></i> محدودیت آی‌پی</div><input class="cp-input-full" id="nl-iplimit" type="number" min="0" step="1" placeholder="0 = نامحدود" value="0"><div class="chip-row"><span class="chip active" onclick="setIpLimit(0,this)">نامحدود</span><span class="chip" onclick="setIpLimit(1,this)">۱</span><span class="chip" onclick="setIpLimit(2,this)">۲</span><span class="chip" onclick="setIpLimit(5,this)">۵</span></div></div></div>
<div class="cp-row mb16"><div class="cp-block" style="flex:1"><div class="cp-block-label"><i class="ti ti-gauge"></i> محدودیت سرعت</div><div class="form-row"><input class="cp-input-full" id="nl-speed" type="number" min="0" step="0.5" placeholder="0 = نامحدود" value="0" style="flex:1"><select class="fs" id="nl-speed-unit" style="flex:0 0 100px"><option value="MBIT" selected>Mbps</option><option value="KB">KB/s</option><option value="MB">MB/s</option></select></div><div class="chip-row"><span class="chip active" onclick="setSpeedLimit(0,this)">نامحدود</span><span class="chip" onclick="setSpeedLimit(1,this)">۱</span><span class="chip" onclick="setSpeedLimit(5,this)">۵</span><span class="chip" onclick="setSpeedLimit(10,this)">۱۰</span><span class="chip" onclick="setSpeedLimit(25,this)">۲۵</span></div></div></div>
<div class="cp-footer"><div class="cp-footer-note"><i class="ti ti-info-circle"></i> UUID رندوم · فقط UUIDهای ثبت‌شده اتصال دارند</div><button class="cp-submit-btn" onclick="createLink()"><i class="ti ti-link-plus"></i> ساخت</button></div></div></div>
<div class="cfg-grid" id="links-grid"></div><div class="empty" id="links-empty" style="display:none"><i class="ti ti-link-off"></i><p>هنوز کانفیگی وجود ندارد</p></div></section>
<section class="pg" id="pg-subgroups"><div class="topbar"><div><div class="tb-title"><i class="ti ti-folders"></i> گروه‌های ساب</div><div class="tb-sub">هر گروه یک صفحه پابلیک مجزا دارد</div></div><div class="tb-right"><span class="badge bg-purple" id="subs-pg-cnt">۰ گروه</span><button class="btn btn-pur" onclick="openModal('modal-create-sub')"><i class="ti ti-folder-plus"></i> گروه جدید</button></div></div><div class="sub-grid" id="subs-grid"></div></section>
<section class="pg" id="pg-subscriptions"><div class="topbar"><div><div class="tb-title"><i class="ti ti-rss"></i> سابسکریپشن</div><div class="tb-sub">لینک‌های اشتراک برای اپ‌های v2ray</div></div></div><div class="g2"><div class="card"><div class="card-title"><i class="ti ti-rss"></i> سابسکریپشن تکی</div><p style="font-size:11.5px;color:var(--t3);line-height:1.8;margin-bottom:12px">هر کانفیگ URL سابسکریپشن مخصوص دارد</p></div><div class="card"><div class="card-title"><i class="ti ti-database"></i> سابسکریپشن کامل</div><div class="sub-box"><span class="sub-url" id="sub-all-url">در حال دریافت...</span><div style="display:flex;gap:6px"><button class="btn btn-sm btn-g" onclick="cpSubAll()"><i class="ti ti-copy"></i></button><button class="btn btn-sm btn-g" onclick="window.open(location.protocol+'//'+location.host+'/sub-all')"><i class="ti ti-external-link"></i></button></div></div></div></div><div class="card"><div class="card-title"><i class="ti ti-folders"></i> لینک ساب گروه‌ها</div><div id="sub-groups-list">در حال بارگذاری...</div></div></section>
<section class="pg" id="pg-traffic"><div class="topbar"><div><div class="tb-title"><i class="ti ti-chart-area"></i> ترافیک</div><div class="tb-sub">تحلیل و مانیتورینگ مصرف</div></div><div class="tb-right"><button class="btn btn-p btn-sm" onclick="refreshAll()"><i class="ti ti-refresh"></i> رفرش</button></div></div><div class="traf-hero"><div class="traf-main-stat"><div class="traf-main-label"><i class="ti ti-database"></i> کل ترافیک</div><div class="traf-main-val" id="t-traffic">—<span>MB</span></div></div><div class="traf-mini"><div><div class="traf-mini-val" id="t-avg">—</div><div class="traf-mini-sub">MB در ساعت</div></div></div><div class="traf-mini"><div><div class="traf-mini-val" id="t-peak">—</div><div class="traf-mini-sub">پیک</div></div></div><div class="traf-mini"><div><div class="traf-mini-val" id="t-low">—</div><div class="traf-mini-sub">کمترین</div></div></div></div><div class="traf-chart-card"><div class="traf-chart-head"><div><div class="traf-chart-title"><i class="ti ti-activity"></i> روند مصرف</div></div></div><div class="traf-chart-body"><canvas id="ch3"></canvas></div></div></section>
<section class="pg" id="pg-connections"><div class="topbar"><div><div class="tb-title"><i class="ti ti-plug-connected"></i> اتصالات فعال</div><div class="tb-sub">مانیتورینگ زنده</div></div><div class="tb-right"><span class="badge bg-green" id="conns-live">—</span><button class="btn btn-p btn-sm" onclick="refreshAll()"><i class="ti ti-refresh"></i> رفرش</button></div></div><div class="conn-hero"><div class="conn-hero-tile"><div class="conn-hero-icon"><i class="ti ti-plug-connected"></i></div><div class="conn-hero-label">اتصالات</div><div class="conn-hero-val" id="ch-count">—</div></div><div class="conn-hero-tile"><div class="conn-hero-icon"><i class="ti ti-transfer"></i></div><div class="conn-hero-label">ترافیک</div><div class="conn-hero-val" id="ch-traffic">—</div></div><div class="conn-hero-tile"><div class="conn-hero-icon"><i class="ti ti-clock"></i></div><div class="conn-hero-label">میانگین مدت</div><div class="conn-hero-val" id="ch-avgdur">—</div></div><div class="conn-hero-tile"><div class="conn-hero-icon"><i class="ti ti-map-pin"></i></div><div class="conn-hero-label">آی‌پی‌های یکتا</div><div class="conn-hero-val" id="ch-uniq">—</div></div></div><div class="conn-grid-v2" id="conns-grid"></div><div class="conn-empty-v2" id="conns-empty" style="display:none"><div class="conn-empty-v2-icon"><i class="ti ti-plug-off"></i></div><div class="conn-empty-v2-title">هیچ اتصال فعالی نیست</div></div></section>
<section class="pg" id="pg-bot"><div class="topbar"><div><div class="tb-title"><i class="ti ti-robot"></i> مدیریت ربات</div><div class="tb-sub">تنظیمات، محصولات، ادمین‌ها و سفارشات</div></div></div><div class="metrics"><div class="metric"><div class="m-icon"><i class="ti ti-package"></i></div><div class="m-label">محصولات</div><div class="m-val" id="bot-products-count">—</div></div><div class="metric"><div class="m-icon"><i class="ti ti-shopping-cart"></i></div><div class="m-label">سفارشات</div><div class="m-val" id="bot-orders-count">—</div></div><div class="metric"><div class="m-icon"><i class="ti ti-users"></i></div><div class="m-label">ادمین‌ها</div><div class="m-val" id="bot-admins-count">—</div></div><div class="metric"><div class="m-icon"><i class="ti ti-credit-card"></i></div><div class="m-label">شماره کارت</div><div class="m-val" style="font-size:14px" id="bot-card-number">—</div></div></div>
<div class="traf-range-tabs" style="margin-bottom:16px;display:flex;gap:4px;background:var(--accent-d);padding:3px;border-radius:10px;border:1px solid var(--card-b);width:fit-content"><button class="traf-range-tab on" data-tab="bot-products" onclick="switchBotTab('products')">📦 محصولات</button><button class="traf-range-tab" data-tab="bot-orders" onclick="switchBotTab('orders')">📋 سفارشات</button><button class="traf-range-tab" data-tab="bot-admins" onclick="switchBotTab('admins')">👥 ادمین‌ها</button><button class="traf-range-tab" data-tab="bot-settings" onclick="switchBotTab('settings')">⚙️ تنظیمات</button></div>
<div id="bot-tab-products" class="bot-tab-content"><div class="create-panel" style="margin-bottom:16px"><div class="cp-head"><div class="cp-head-icon"><i class="ti ti-square-rounded-plus"></i></div><div class="cp-head-text"><div class="cp-head-title">افزودن محصول جدید</div></div></div><div class="cp-body"><div class="cp-row"><div class="cp-block"><div class="cp-block-label"><i class="ti ti-tag"></i> نام</div><input class="cp-input-full" id="bot-product-name" placeholder="مثلاً: کانفیگ استاندارد"></div><div class="cp-block"><div class="cp-block-label"><i class="ti ti-database"></i> حجم (GB)</div><input class="cp-input-full" id="bot-product-volume" type="number" placeholder="۵۰" value="50"></div></div><div class="cp-row"><div class="cp-block"><div class="cp-block-label"><i class="ti ti-clock"></i> مدت (روز)</div><input class="cp-input-full" id="bot-product-duration" type="number" placeholder="۳۰" value="30"></div><div class="cp-block"><div class="cp-block-label"><i class="ti ti-gauge"></i> سرعت (Mbps)</div><input class="cp-input-full" id="bot-product-speed" type="number" placeholder="۰ = نامحدود" value="0"></div></div><div class="cp-row"><div class="cp-block"><div class="cp-block-label"><i class="ti ti-currency-toman"></i> قیمت (تومان)</div><input class="cp-input-full" id="bot-product-price" type="number" placeholder="۱۵۰۰۰۰" value="150000"></div><div class="cp-block" style="display:flex;align-items:flex-end;padding-bottom:14px"><button class="cp-submit-btn" onclick="addProduct()" style="width:100%;justify-content:center"><i class="ti ti-plus"></i> افزودن</button></div></div></div></div><div id="bot-products-list" class="cfg-grid"></div></div>
<div id="bot-tab-orders" class="bot-tab-content" style="display:none"><div id="bot-orders-list" class="cfg-grid"></div></div>
<div id="bot-tab-admins" class="bot-tab-content" style="display:none"><div class="create-panel" style="margin-bottom:16px"><div class="cp-head"><div class="cp-head-icon"><i class="ti ti-user-plus"></i></div><div class="cp-head-text"><div class="cp-head-title">افزودن ادمین جدید</div></div></div><div class="cp-body"><div class="cp-row"><div class="cp-block"><div class="cp-block-label"><i class="ti ti-id-badge"></i> آیدی عددی</div><input class="cp-input-full" id="bot-admin-id" placeholder="۱۲۳۴۵۶۷۸۹"></div><div class="cp-block" style="display:flex;align-items:flex-end;padding-bottom:14px"><button class="cp-submit-btn" onclick="addAdmin()" style="width:100%;justify-content:center"><i class="ti ti-plus"></i> افزودن</button></div></div></div></div><div id="bot-admins-list" class="cfg-grid"></div></div>
<div id="bot-tab-settings" class="bot-tab-content" style="display:none"><div class="srv-panel" style="max-width:500px"><div class="srv-hero"><div class="srv-hero-icon"><i class="ti ti-credit-card"></i></div><div class="srv-hero-text"><div class="srv-hero-domain">شماره کارت</div></div></div><div class="srv-tiles"><div class="srv-tile" style="grid-column:1/-1"><div class="srv-tile-icon"><i class="ti ti-card"></i></div><div class="srv-tile-text"><div class="srv-tile-label">شماره کارت فعلی</div><div class="srv-tile-val" id="bot-card-display">—</div></div></div><div class="srv-tile" style="grid-column:1/-1"><div class="srv-tile-text" style="width:100%"><div class="srv-tile-label">تغییر شماره کارت</div><input class="cp-input-full" id="bot-new-card" placeholder="شماره کارت جدید" style="margin-top:6px"><button class="cp-submit-btn" onclick="updateCard()" style="margin-top:10px;width:100%;justify-content:center"><i class="ti ti-check"></i> به‌روزرسانی</button></div></div></div></div></div></section>
<section class="pg" id="pg-security"><div class="topbar"><div><div class="tb-title"><i class="ti ti-shield-lock"></i> امنیت</div></div></div><div class="g2"><div class="card"><div class="card-title"><i class="ti ti-lock"></i> رمزنگاری</div><div class="sr"><span class="sr-k"><i class="ti ti-certificate"></i> TLS/HTTPS</span><span class="sr-v" style="color:var(--green-t)">● فعال (443)</span></div><div class="sr"><span class="sr-k"><i class="ti ti-fingerprint"></i> Fingerprint</span><span class="sr-v">Chrome Spoof</span></div><div class="sr"><span class="sr-k"><i class="ti ti-key"></i> هش رمز</span><span class="sr-v">SHA-256+Salt</span></div></div><div class="card"><div class="card-title"><i class="ti ti-shield-check"></i> کنترل دسترسی</div><div class="sr"><span class="sr-k"><i class="ti ti-id-badge"></i> UUID Auth</span><span class="sr-v" style="color:var(--green-t)">● فعال</span></div><div class="sr"><span class="sr-k"><i class="ti ti-toggle-right"></i> فعال/غیرفعال</span><span class="sr-v" style="color:var(--green-t)">● فعال</span></div><div class="sr"><span class="sr-k"><i class="ti ti-gauge"></i> سهمیه ترافیک</span><span class="sr-v" style="color:var(--green-t)">● فعال</span></div></div></div></section>
<section class="pg" id="pg-logs"><div class="topbar"><div><div class="tb-title"><i class="ti ti-history"></i> لاگ فعالیت‌ها</div></div><div class="tb-right"><button class="btn btn-p btn-sm" onclick="loadActivity()"><i class="ti ti-refresh"></i></button></div></div><div class="card"><div class="log-timeline" id="logs-list">—</div></div></section>
<section class="pg" id="pg-errors"><div class="topbar"><div><div class="tb-title"><i class="ti ti-alert-triangle"></i> خطاها</div></div><div class="tb-right"><span class="badge bg-red" id="errs-badge">۰</span></div></div><div class="card"><div id="errs-full">—</div></div></section>
<section class="pg" id="pg-settings"><div class="topbar"><div><div class="tb-title"><i class="ti ti-settings"></i> تنظیمات</div></div></div><div class="g2"><div class="srv-panel"><div class="srv-hero"><div class="srv-hero-icon"><i class="ti ti-server-2"></i></div><div class="srv-hero-text"><div class="srv-hero-domain" id="set-host">—</div><div class="srv-hero-sub"><span class="dot dg pulse"></span> آنلاین</div></div></div><div class="srv-tiles"><div class="srv-tile"><div class="srv-tile-icon"><i class="ti ti-route"></i></div><div class="srv-tile-text"><div class="srv-tile-label">پورت</div><div class="srv-tile-val">443</div></div></div><div class="srv-tile"><div class="srv-tile-icon"><i class="ti ti-versions"></i></div><div class="srv-tile-text"><div class="srv-tile-label">نسخه</div><div class="srv-tile-val">v3.0</div></div></div><div class="srv-tile"><div class="srv-tile-icon"><i class="ti ti-brand-fastapi"></i></div><div class="srv-tile-text"><div class="srv-tile-label">فریم‌ورک</div><div class="srv-tile-val">FastAPI</div></div></div><div class="srv-tile"><div class="srv-tile-icon"><i class="ti ti-cloud"></i></div><div class="srv-tile-text"><div class="srv-tile-label">پلتفرم</div><div class="srv-tile-val">Railway</div></div></div></div></div><div class="pw-panel"><div class="pw-hero"><div class="pw-hero-icon"><i class="ti ti-key"></i></div><div class="pw-hero-text"><div class="pw-hero-title">تغییر رمز</div></div></div><div class="pw-body"><div class="pw-field"><label>رمز فعلی</label><input class="pw-input" type="password" id="cp-cur" placeholder="رمز فعلی"></div><div class="pw-field"><label>رمز جدید</label><input class="pw-input" type="password" id="cp-new" placeholder="حداقل ۴ کاراکتر"></div><div class="pw-field"><label>تکرار رمز جدید</label><input class="pw-input" type="password" id="cp-cf" placeholder="تکرار"></div><button class="pw-submit" onclick="changePw()"><i class="ti ti-shield-check"></i> ذخیره</button></div></div></div></section>
<section class="pg" id="pg-support"><div class="topbar"><div><div class="tb-title"><i class="ti ti-headset"></i> پشتیبانی</div></div></div><div class="srv-panel"><div class="srv-hero"><div class="srv-hero-icon"><i class="ti ti-headset"></i></div><div class="srv-hero-text"><div class="srv-hero-domain">پشتیبانی TK-SX</div></div></div><div class="srv-tiles"><a class="srv-tile" href="https://t.me/ItzJustEren" target="_blank"><div class="srv-tile-icon"><i class="ti ti-brand-telegram"></i></div><div class="srv-tile-text"><div class="srv-tile-label">آیدی</div><div class="srv-tile-val">@ItzJustEren</div></div></a><a class="srv-tile" href="https://t.me/TaaKaaOrg" target="_blank"><div class="srv-tile-icon"><i class="ti ti-users-group"></i></div><div class="srv-tile-text"><div class="srv-tile-label">کانال</div><div class="srv-tile-val">@TaaKaaOrg</div></div></a></div></div></section>
</main>
<script>
let isDark=localStorage.getItem('tksx-theme')!=='light';
function applyTheme(dark){document.documentElement.setAttribute('data-theme',dark?'dark':'light');const icon=dark?'ti-sun':'ti-moon';document.getElementById('theme-icon').className='ti '+icon;document.getElementById('theme-label').textContent=dark?'تم روشن':'تم تاریک';const mobI=document.getElementById('theme-mob-icon');if(mobI)mobI.className='ti '+icon;}
function toggleTheme(){isDark=!isDark;localStorage.setItem('tksx-theme',isDark?'dark':'light');applyTheme(isDark)}
applyTheme(isDark);
function toast(msg,type=''){const t=document.getElementById('toast');t.textContent=msg;t.className='toast show'+(type?' '+type:'');setTimeout(()=>t.classList.remove('show'),2400);}
function fmtB(b){if(!b||b===0)return '0 B';if(b<1024)return b+' B';if(b<1024**2)return (b/1024).toFixed(1)+' KB';if(b<1024**3)return (b/1024**2).toFixed(2)+' MB';return (b/1024**3).toFixed(2)+' GB'}
function toFa(n){return String(n).replace(/\d/g,d=>'۰۱۲۳۴۵۶۷۸۹'[d])}
function esc(s){return String(s||'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]))}
function daysLeft(exp){if(!exp)return null;return Math.ceil((new Date(exp)-Date.now())/(864e5));}
function expChip(exp,expired){if(expired)return '<span class="exp-chip ec-exp"><i class="ti ti-calendar-x"></i> منقضی</span>';if(!exp)return '<span class="exp-chip ec-inf"><i class="ti ti-infinity"></i> نامحدود</span>';const d=daysLeft(exp);if(d<=0)return '<span class="exp-chip ec-exp"><i class="ti ti-calendar-x"></i> منقضی</span>';if(d<=3)return `<span class="exp-chip ec-warn"><i class="ti ti-alert-triangle"></i> ${toFa(d)} روز</span>`;return `<span class="exp-chip ec-ok"><i class="ti ti-calendar-check"></i> ${toFa(d)} روز</span>`;}
function protoBadge(p){const m={'vless':['VLESS','pc-ws'],'vmess':['VMess','pc-ws'],'trojan':['Trojan','pc-ws'],'shadowsocks':['Shadowsocks','pc-ws'],'socks5':['SOCKS5','pc-ws'],'http':['HTTP','pc-ws'],'wireguard':['WireGuard','pc-ultra'],'hysteria2':['Hysteria2','pc-ultra'],'tun':['TUN','pc-xhttp'],'dokodemo':['Dokodemo','pc-xhttp'],'snell':['Snell','pc-xhttp']};const v=m[p]||m['vless'];return `<span class="proto-chip ${v[1]}">${v[0]}</span>`;}
async function checkAuth(){try{const r=await fetch('/api/me');const d=await r.json();if(!d.authenticated)location.href='/login';}catch(e){location.href='/login'}}
async function logout(){try{await fetch('/api/logout',{method:'POST'})}catch(e){}location.href='/login'}
document.getElementById('logout-btn').addEventListener('click',logout);
async function authF(url,opts={}){const r=await fetch(url,opts);if(r.status===401){location.href='/login';throw new Error('unauthorized')}return r;}
function setQuota(val,unit,el){document.getElementById('nl-val').value=val===0?'':val;document.getElementById('nl-unit').value=unit;document.querySelectorAll('#quota-chips .chip').forEach(c=>c.classList.remove('active'));el.classList.add('active');}
function setExpiry(days,el){document.getElementById('nl-exp').value=days===0?'':days;document.querySelectorAll('#exp-chips .chip').forEach(c=>c.classList.remove('active'));el.classList.add('active');}
function selectProto(val,el){document.getElementById('nl-proto').value=val;document.querySelectorAll('.proto-card').forEach(c=>c.classList.remove('active'));el.classList.add('active');}
function setIpLimit(n,el){document.getElementById('nl-iplimit').value=n;document.querySelectorAll('#iplimit-chips .chip').forEach(c=>c.classList.remove('active'));el.classList.add('active');}
function setSpeedLimit(n,el){document.getElementById('nl-speed').value=n;document.getElementById('nl-speed-unit').value='MBIT';document.querySelectorAll('#speed-chips .chip').forEach(c=>c.classList.remove('active'));el.classList.add('active');}
function onAlpnPresetChange(){const p=document.getElementById('nl-alpn-preset').value;const inp=document.getElementById('nl-alpn');if(p==='__custom__'){inp.style.display='block';inp.value='';inp.focus();}else{inp.style.display='none';inp.value=p;}}
const sb=document.getElementById('sb'),overlay=document.getElementById('overlay');
function openSb(){sb.classList.add('open');overlay.classList.add('show')}
function closeSb(){sb.classList.remove('open');overlay.classList.remove('show')}
document.getElementById('open-sb').addEventListener('click',openSb);
document.getElementById('close-sb').addEventListener('click',closeSb);
overlay.addEventListener('click',closeSb);
function navTo(name){document.querySelectorAll('.nav-it').forEach(n=>n.classList.toggle('on',n.dataset.pg===name));document.querySelectorAll('.pg').forEach(p=>p.classList.toggle('on',p.id==='pg-'+name));const loaders={links:loadLinks,connections:loadConns,errors:loadErrs,subscriptions:loadSubsPage,subgroups:loadSubs,logs:loadActivity};if(loaders[name])loaders[name]();closeSb();window.scrollTo({top:0,behavior:'smooth'});}
document.querySelectorAll('.nav-it').forEach(el=>el.addEventListener('click',()=>navTo(el.dataset.pg)));
function openModal(id){document.getElementById(id).classList.add('open')}
function closeModal(id){document.getElementById(id).classList.remove('open')}
let prevTraf=0,ch1,ch2,ch3;
async function fetchStats(){try{const r=await authF('/stats'),d=await r.json();document.getElementById('m-conns').textContent=d.active_connections;document.getElementById('conns-nb').textContent=d.active_connections;document.getElementById('m-traffic').innerHTML=d.total_traffic_mb.toFixed(1)+'<span class="m-unit">MB</span>';document.getElementById('m-alinks').textContent=d.active_links??'—';document.getElementById('m-subs').textContent=d.subs_count??'—';document.getElementById('errs-badge').textContent=d.total_errors+' خطا';document.getElementById('uptime-inline').textContent=d.uptime;document.getElementById('uptime-badge').textContent='Railway · '+d.uptime;document.getElementById('last-upd').textContent='آخرین بروزرسانی: '+new Date().toLocaleTimeString('fa-IR');document.getElementById('conns-live').innerHTML='<span class="dot dg pulse"></span> '+d.active_connections+' اتصال';document.getElementById('t-traffic').innerHTML=d.total_traffic_mb.toFixed(1)+'<span class="m-unit">MB</span>';prevTraf=d.total_traffic_mb;if(d.hourly){const labels=Object.keys(d.hourly).sort(),vals=labels.map(k=>+(d.hourly[k]/1024**2).toFixed(2));[ch1,ch3].forEach(c=>{if(!c)return;c.data.labels=labels;c.data.datasets[0].data=vals;c.update()});if(vals.length){const avg=vals.reduce((a,b)=>a+b,0)/vals.length,peak=Math.max(...vals);document.getElementById('t-avg').innerHTML=avg.toFixed(2)+'<span class="m-unit">MB</span>';document.getElementById('t-peak').innerHTML=peak.toFixed(2)+'<span class="m-unit">MB</span>';}}
renderErrs(d.recent_errors||[]);}catch(e){console.error(e)}}
function renderErrs(errs){const el=document.getElementById('errs-full');if(!el)return;if(!errs.length){el.innerHTML='<div style="color:var(--green-t);padding:10px;font-size:12px"><i class="ti ti-circle-check"></i> بدون خطا</div>';return}el.innerHTML=errs.slice().reverse().map(e=>`<div class="erow"><div class="etime"><i class="ti ti-clock"></i>${new Date(e.time).toLocaleString('fa-IR')}</div><div class="emsg">${esc(e.error)}${e.url?' — '+esc(e.url):''}</div></div>`).join('');}
async function loadActivity(){try{const r=await authF('/api/activity'),d=await r.json();const logs=(d.logs||[]).slice().reverse();const el=document.getElementById('logs-list');if(!logs.length){el.innerHTML='<div style="color:var(--t3);padding:10px;font-size:12px">هنوز لاگی ثبت نشده</div>';return}el.innerHTML=logs.map(l=>`<div class="log-item"><div class="log-ic ${l.level}"><i class="ti ${l.level==='ok'?'ti-circle-check':l.level==='err'?'ti-circle-x':'ti-info-circle'}"></i></div><div class="log-body"><div class="log-msg">${esc(l.message)}</div><div class="log-time">${new Date(l.time).toLocaleString('fa-IR')}</div></div></div>`).join('');}catch(e){}}
let allSubsList=[],allLinksList=[],currentSubId=null;
async function loadLinks(){try{const [lr,sr]=await Promise.all([authF('/api/links'),authF('/api/subs')]);const {links=[]}=await lr.json();const {subs=[]}=await sr.json();allSubsList=subs;allLinksList=links;const nlSub=document.getElementById('nl-sub');nlSub.innerHTML='<option value="">— بدون گروه —</option>'+subs.map(s=>`<option value="${esc(s.sub_id)}">${esc(s.name)}</option>`).join('');document.getElementById('links-nb').textContent=links.length;document.getElementById('links-pg-cnt').textContent=toFa(links.length)+' کانفیگ';document.getElementById('lsummary-badge').textContent=toFa(links.length);const grid=document.getElementById('links-grid'),empty=document.getElementById('links-empty');if(!links.length){grid.innerHTML='';empty.style.display='block';document.getElementById('lsummary').innerHTML='<div class="empty"><i class="ti ti-link-off"></i><p>کانفیگی وجود ندارد</p></div>';return}
empty.style.display='none';const subMap=Object.fromEntries(subs.map(s=>[s.sub_id,s.name]));grid.innerHTML=links.map(l=>{const lim=l.limit_bytes===0?'∞':fmtB(l.limit_bytes);const pct=l.limit_bytes===0?0:Math.min(100,l.used_bytes/l.limit_bytes*100);const bc=pct>90?'var(--red)':pct>70?'var(--amber)':'var(--accent)';const allowed=l.active&&!l.expired;const cardCls=!l.active?'is-off':(l.expired?'is-exp':'');return `<div class="cfg-card ${cardCls}"><div class="cfg-row"><span class="cfg-status-dot ${allowed?'pulse':''}"></span><div class="cfg-identity"><div class="cfg-label">${esc(l.label)}</div><div class="cfg-sub-meta"><span class="cfg-uuid-mini" onclick="navigator.clipboard.writeText('${l.uuid}').then(()=>toast('UUID کپی شد','ok'))" title="${l.uuid}"><i class="ti ti-fingerprint"></i> ${l.uuid.slice(0,10)}…</span><span>${new Date(l.created_at).toLocaleDateString('fa-IR')}</span></div></div><div class="cfg-divider-v"></div><div class="cfg-usage-col"><div class="ubar"><div class="ubar-f" style="width:${pct}%;background:${bc}"></div></div><div class="utxt"><span>${fmtB(l.used_bytes)}</span><span>از ${lim}</span></div></div><div class="cfg-divider-v"></div><div class="cfg-exp-col">${expChip(l.expires_at,l.expired)}</div><div class="cfg-divider-v"></div><div class="cfg-badges-col">${protoBadge(l.protocol)}<span class="cfg-sub-tag"><i class="ti ti-route"></i> :${l.port||443}</span><span class="cfg-sub-tag"><i class="ti ti-fingerprint"></i> ${esc(l.fingerprint||'chrome')}</span><span class="cfg-sub-tag"><i class="ti ti-users"></i> ${l.connected_ips||0}${l.ip_limit?('/'+l.ip_limit):' (∞)'}</span><span class="cfg-sub-tag"><i class="ti ti-gauge"></i> ${l.speed_limit_bytes?((l.speed_limit_bytes*8/1024/1024).toFixed(1)+' Mbps'):'نامحدود'}</span>${l.sub_id&&allSubsList.find(s=>s.sub_id===l.sub_id)?`<span class="cfg-sub-tag"><i class="ti ti-folder"></i> ${esc(allSubsList.find(s=>s.sub_id===l.sub_id).name)}</span>`:''}</div><div class="cfg-divider-v"></div><div class="cfg-actions"><button class="tog${allowed?' on':''}" onclick="toggleActive('${l.uuid}',${!l.active})"></button><button class="btn btn-sm btn-g btn-icon" onclick="navigator.clipboard.writeText('${esc(l.link_url)}').then(()=>toast('کپی شد','ok'))"><i class="ti ti-copy"></i></button><button class="btn btn-sm btn-g btn-icon" onclick="navigator.clipboard.writeText('${esc(l.sub_url)}').then(()=>toast('Sub کپی شد','ok'))"><i class="ti ti-rss"></i></button><button class="btn btn-sm btn-g btn-icon" onclick="showQR('${esc(l.link_url)}')"><i class="ti ti-qrcode"></i></button><button class="btn btn-sm btn-amber btn-icon" onclick="openEditLink('${l.uuid}')"><i class="ti ti-edit"></i></button><button class="btn btn-sm btn-g btn-icon" onclick="resetUsage('${l.uuid}')"><i class="ti ti-rotate"></i></button><button class="btn btn-sm btn-d btn-icon" onclick="deleteLink('${l.uuid}')"><i class="ti ti-trash"></i></button></div></div></div>`;}).join('');document.getElementById('lsummary').innerHTML=links.slice(0,6).map(l=>`<div class="sr"><span class="sr-k"><i class="ti ${l.expired?'ti-calendar-x':l.active?'ti-circle-check':'ti-circle-x'}" style="color:${l.expired?'var(--amber)':l.active?'var(--green)':'var(--red)'}"></i>${esc(l.label)}</span><span class="sr-v">${fmtB(l.used_bytes)} / ${l.limit_bytes===0?'∞':fmtB(l.limit_bytes)}</span></div>`).join('');}catch(e){console.error(e)}}
async function createLink(){const label=document.getElementById('nl-label').value.trim()||'کانفیگ جدید';const val=document.getElementById('nl-val').value;const unit=document.getElementById('nl-unit').value;const exp=document.getElementById('nl-exp').value;const note=document.getElementById('nl-note').value.trim();const sub_id=document.getElementById('nl-sub').value||null;const protocol=document.getElementById('nl-proto').value||'vless';const fingerprint=document.getElementById('nl-fp').value||'chrome';const alpn=document.getElementById('nl-alpn').value.trim();const port=Number(document.getElementById('nl-port').value)||443;const ip_limit=Number(document.getElementById('nl-iplimit').value)||0;const speed_limit_value=Number(document.getElementById('nl-speed').value)||0;const speed_limit_unit=document.getElementById('nl-speed-unit').value;try{const r=await authF('/api/links',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({label,limit_value:val||0,limit_unit:unit,expires_days:exp||0,note,sub_id,protocol,fingerprint,alpn,port,ip_limit,speed_limit_value,speed_limit_unit})});if(!r.ok)throw new Error('failed');toast('کانفیگ ساخته شد ✓','ok');loadLinks();}catch(e){toast('خطا در ساخت','err')}}
function openEditLink(uuid){const l=allLinksList.find(x=>x.uuid===uuid);if(!l)return;document.getElementById('el-uuid').value=uuid;document.getElementById('el-label').value=l.label;document.getElementById('el-note').value=l.note||'';if(l.limit_bytes===0){document.getElementById('el-val').value='';document.getElementById('el-unit').value='GB';}else{document.getElementById('el-val').value=(l.limit_bytes/1024/1024).toFixed(0);document.getElementById('el-unit').value='MB';}document.getElementById('el-exp').value='';document.getElementById('el-fp').value=l.fingerprint||'chrome';document.getElementById('el-alpn').value=l.alpn||'';document.getElementById('el-port').value=l.port||443;document.getElementById('el-iplimit').value=l.ip_limit||0;if(!l.speed_limit_bytes){document.getElementById('el-speed').value='0';document.getElementById('el-speed-unit').value='MBIT';}else{document.getElementById('el-speed').value=(l.speed_limit_bytes*8/1024/1024).toFixed(2);document.getElementById('el-speed-unit').value='MBIT';}openModal('modal-edit-link');}
async function saveEditLink(){const uuid=document.getElementById('el-uuid').value;const label=document.getElementById('el-label').value.trim();const note=document.getElementById('el-note').value.trim();const val=document.getElementById('el-val').value;const unit=document.getElementById('el-unit').value;const exp=document.getElementById('el-exp').value;const fingerprint=document.getElementById('el-fp').value||'chrome';const alpn=document.getElementById('el-alpn').value.trim();const port=Number(document.getElementById('el-port').value)||443;const ip_limit=Number(document.getElementById('el-iplimit').value)||0;const speed_limit_value=Number(document.getElementById('el-speed').value)||0;const speed_limit_unit=document.getElementById('el-speed-unit').value;const body={label,note,limit_value:val||0,limit_unit:unit,fingerprint,alpn,port,ip_limit,speed_limit_value,speed_limit_unit};if(exp&&Number(exp)>0)body.expires_days=Number(exp);try{const r=await authF('/api/links/'+uuid,{method:'PATCH',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)});if(!r.ok)throw new Error();closeModal('modal-edit-link');toast('ویرایش شد ✓','ok');loadLinks();}catch(e){toast('خطا','err')}}
async function toggleActive(uuid,newState){try{const r=await authF('/api/links/'+uuid,{method:'PATCH',headers:{'Content-Type':'application/json'},body:JSON.stringify({active:newState})});if(!r.ok)throw new Error();toast(newState?'فعال شد ✓':'غیرفعال شد','ok');loadLinks();}catch(e){toast('خطا','err')}}
async function resetUsage(uuid){try{const r=await authF('/api/links/'+uuid,{method:'PATCH',headers:{'Content-Type':'application/json'},body:JSON.stringify({reset_usage:true})});if(!r.ok)throw new Error();toast('مصرف ریست شد ✓','ok');loadLinks();}catch(e){toast('خطا','err')}}
async function deleteLink(uuid){if(!confirm('حذف این کانفیگ؟'))return;try{const r=await authF('/api/links/'+uuid,{method:'DELETE'});if(!r.ok)throw new Error();toast('حذف شد ✓','ok');loadLinks();}catch(e){toast('خطا','err')}}
function showQR(link){window.open('https://api.qrserver.com/v1/create-qr-code/?size=300x300&data='+encodeURIComponent(link),'_blank')}
let allSubsRaw=[];
async function loadSubs(){try{const r=await authF('/api/subs'),d=await r.json();const subs=d.subs||[];allSubsRaw=subs;document.getElementById('subs-nb').textContent=subs.length;document.getElementById('subs-pg-cnt').textContent=toFa(subs.length)+' گروه';renderSubsGrid(subs);}catch(e){}}
function renderSubsGrid(subs){const grid=document.getElementById('subs-grid');if(!subs.length){grid.innerHTML='<div class="subs-empty-v2"><div class="subs-empty-v2-icon"><i class="ti ti-folders"></i></div><div class="subs-empty-v2-title">هنوز گروهی وجود ندارد</div></div>';return}
grid.innerHTML=subs.map(s=>`<div class="sub-card"><div class="sub-card-top"><div class="sub-card-head-v2"><div class="sub-card-icon"><i class="ti ti-folder"></i></div><div class="sub-card-titles"><div class="sub-card-name-v2">${esc(s.name)}</div>${s.desc?`<div class="sub-card-desc-v2">${esc(s.desc)}</div>`:''}</div><div class="sub-card-lock-badge ${s.has_password?'locked':'open'}"><i class="ti ${s.has_password?'ti-lock':'ti-lock-open'}"></i></div></div><div class="sub-card-stats"><div class="sub-card-stat"><div class="sub-card-stat-val">${toFa(s.links_count)}</div><div class="sub-card-stat-label">کانفیگ</div></div><div class="sub-card-stat"><div class="sub-card-stat-val" style="color:var(--green-t)">${toFa(s.active_count)}</div><div class="sub-card-stat-label">فعال</div></div><div class="sub-card-stat"><div class="sub-card-stat-val" style="font-size:12px">${esc(s.total_used_fmt)}</div><div class="sub-card-stat-label">مصرف</div></div></div></div><div class="sub-card-url-row"><span class="sub-card-url-text">${esc(s.public_url)}</span><button class="sub-card-url-copy" onclick="navigator.clipboard.writeText('${esc(s.public_url)}').then(()=>toast('کپی شد','ok'))"><i class="ti ti-copy"></i></button></div><div class="sub-card-bottom"><button class="btn btn-sm btn-g" onclick="openSubLinks('${esc(s.sub_id)}','${esc(s.name)}')"><i class="ti ti-link-plus"></i> کانفیگ‌ها</button><button class="btn btn-sm btn-o" onclick="navigator.clipboard.writeText('${esc(s.sub_url)}').then(()=>toast('کپی شد','ok'))"><i class="ti ti-rss"></i> ساب</button><button class="btn btn-sm btn-g btn-icon" onclick="showQR('${esc(s.sub_url)}')"><i class="ti ti-qrcode"></i></button><button class="btn btn-sm btn-d btn-icon" onclick="deleteSub('${esc(s.sub_id)}')"><i class="ti ti-trash"></i></button></div></div>`).join('');}
async function createSub(){const name=document.getElementById('ns-name').value.trim()||'گروه جدید';const desc=document.getElementById('ns-desc').value.trim();const pw=document.getElementById('ns-pw').value;try{const r=await authF('/api/subs',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({name,desc,password:pw})});if(!r.ok)throw new Error('failed');closeModal('modal-create-sub');toast('گروه ساخته شد ✓','ok');loadSubs();}catch(e){toast('خطا','err')}}
async function deleteSub(sub_id){if(!confirm('حذف این گروه؟'))return;try{const r=await authF('/api/subs/'+sub_id,{method:'DELETE'});if(!r.ok)throw new Error();toast('گروه حذف شد ✓','ok');loadSubs();loadLinks();}catch(e){toast('خطا','err')}}
let lmodalLinks=[],lmodalInSub=new Set();
async function openSubLinks(sub_id,name){currentSubId=sub_id;document.getElementById('modal-sub-name').textContent=name;document.getElementById('modal-links-body').innerHTML='<div style="color:var(--t3);font-size:12px;padding:20px;text-align:center"><i class="ti ti-loader-2" style="animation:spin 1s linear infinite"></i></div>';openModal('modal-links');try{const [lr,sr]=await Promise.all([authF('/api/links'),authF('/api/subs')]);const {links=[]}=await lr.json();const {subs=[]}=await sr.json();const thisSub=subs.find(s=>s.sub_id===sub_id);lmodalInSub=new Set(thisSub?.link_ids||[]);lmodalLinks=links;renderLmodalList(links);}catch(e){toast('خطا','err')}}
function renderLmodalList(links){const body=document.getElementById('modal-links-body');if(!links.length){body.innerHTML='<div class="empty" style="padding:30px"><i class="ti ti-link-off"></i><p>کانفیگی وجود ندارد</p></div>';return}body.innerHTML=links.map(l=>{const checked=lmodalInSub.has(l.uuid);const on=l.active&&!l.expired;return `<div class="lrow-v2 ${checked?'checked':''}" data-uuid="${l.uuid}" onclick="toggleLrow('${l.uuid}',this)"><div class="lrow-v2-check"><i class="ti ti-check"></i></div><div class="lrow-v2-avatar"><i class="ti ti-key"></i></div><div class="lrow-v2-info"><div class="lrow-v2-name">${esc(l.label)}</div><div class="lrow-v2-meta"><i class="ti ti-database"></i> ${fmtB(l.used_bytes)}</div></div><span class="lrow-v2-status ${on?'on':'off'}">${on?'فعال':'غیرفعال'}</span></div>`;}).join('');}
function toggleLrow(uuid,el){if(lmodalInSub.has(uuid)){lmodalInSub.delete(uuid);el.classList.remove('checked')}else{lmodalInSub.add(uuid);el.classList.add('checked')}}
async function saveSubLinks(){if(!currentSubId)return;const link_ids=[...lmodalInSub];try{const r=await authF('/api/subs/'+currentSubId,{method:'PATCH',headers:{'Content-Type':'application/json'},body:JSON.stringify({link_ids})});if(!r.ok)throw new Error();await Promise.all(lmodalLinks.map(l=>authF('/api/links/'+l.uuid,{method:'PATCH',headers:{'Content-Type':'application/json'},body:JSON.stringify({sub_id:lmodalInSub.has(l.uuid)?currentSubId:null})})));closeModal('modal-links');toast('ذخیره شد ✓','ok');loadSubs();loadLinks();}catch(e){toast('خطا','err')}}
async function loadSubsPage(){document.getElementById('sub-all-url').textContent=location.protocol+'//'+location.host+'/sub-all';try{const r=await authF('/api/subs'),d=await r.json();const subs=d.subs||[];const el=document.getElementById('sub-groups-list');if(!subs.length){el.innerHTML='<div class="empty"><i class="ti ti-rss-off"></i><p>گروهی ندارید</p></div>';return}el.innerHTML=subs.map(s=>`<div style="padding:13px 15px;background:var(--accent-d);border:1px solid var(--card-b);border-radius:10px;margin-bottom:8px;display:flex;align-items:center;justify-content:space-between;gap:10px;flex-wrap:wrap"><div><div style="font-weight:700;font-size:13px;margin-bottom:3px">${esc(s.name)}</div><div style="font-family:ui-monospace,monospace;font-size:10px;color:#A78BFA">${esc(s.sub_url)}</div></div><div style="display:flex;gap:5px"><button class="btn btn-sm btn-pur" onclick="navigator.clipboard.writeText('${esc(s.sub_url)}').then(()=>toast('کپی شد','ok'))"><i class="ti ti-copy"></i></button><button class="btn btn-sm btn-pur" onclick="navigator.clipboard.writeText('${esc(s.public_url)}').then(()=>toast('کپی شد','ok'))"><i class="ti ti-globe"></i></button></div></div>`).join('');}catch(e){}}
function cpSubAll(){navigator.clipboard.writeText(location.protocol+'//'+location.host+'/sub-all').then(()=>toast('کپی شد ✓','ok'))}
async function loadConns(){try{const r=await authF('/api/connections'),d=await r.json();const grid=document.getElementById('conns-grid'),ce=document.getElementById('conns-empty');document.getElementById('conns-live').innerHTML='<span class="dot dg pulse"></span> '+d.count+' اتصال';document.getElementById('ch-count').textContent=toFa(d.count);const conns=d.connections||[];if(!d.count){grid.innerHTML='';ce.style.display='block';document.getElementById('ch-traffic').textContent='—';document.getElementById('ch-avgdur').textContent='—';document.getElementById('ch-uniq').textContent='—';return}
ce.style.display='none';const totalBytes=conns.reduce((s,c)=>s+parseBytesFmt(c.bytes_fmt),0);document.getElementById('ch-traffic').textContent=fmtB(totalBytes);const uniqIps=new Set(conns.map(c=>c.ip)).size;document.getElementById('ch-uniq').textContent=toFa(uniqIps);const durs=conns.map(c=>c.connected_at?Math.max(0,Math.floor((Date.now()-new Date(c.connected_at).getTime())/1000)):0);const avgSec=durs.length?Math.floor(durs.reduce((a,b)=>a+b,0)/durs.length):0;document.getElementById('ch-avgdur').textContent=avgSec<60?avgSec+' ث':avgSec<3600?Math.floor(avgSec/60)+' د':Math.floor(avgSec/3600)+' س';const maxDur=Math.max(...durs,1);grid.innerHTML=conns.map(c=>{const secs=c.connected_at?Math.max(0,Math.floor((Date.now()-new Date(c.connected_at).getTime())/1000)):0;const dur=secs<60?secs+' ثانیه':secs<3600?Math.floor(secs/60)+' دقیقه':Math.floor(secs/3600)+' ساعت';const durPct=Math.min(100,Math.round((secs/maxDur)*100));return `<div class="conn-card-v2"><div class="conn-card-v2-top"><div class="conn-avatar"><i class="ti ti-device-desktop"></i></div><div class="conn-card-v2-id"><div class="conn-ip-v2">${esc(c.ip)}</div><div class="conn-label-v2">${esc(c.label)}</div></div><span class="conn-status-pill"><span class="dot dg pulse"></span> زنده</span></div><div class="conn-card-v2-divider"></div><div class="conn-card-v2-body"><div class="conn-stat-row"><div class="conn-stat-box"><div class="conn-stat-icon"><i class="ti ti-transfer"></i></div><div><div class="conn-stat-text-label">ترافیک</div><div class="conn-stat-text-val">${esc(c.bytes_fmt)}</div></div></div><div class="conn-stat-box"><div class="conn-stat-icon time"><i class="ti ti-clock"></i></div><div><div class="conn-stat-text-label">مدت</div><div class="conn-stat-text-val">${dur}</div></div></div></div><div class="conn-duration-track"><div class="conn-duration-fill" style="width:${durPct}%"></div></div></div></div>`;}).join('');}catch(e){console.error(e)}}
function parseBytesFmt(s){if(!s)return 0;const m=String(s).match(/([\d.]+)\s*([A-Za-z]+)/);if(!m)return 0;const n=parseFloat(m[1]),u=m[2].toUpperCase();const mult={B:1,KB:1024,MB:1024**2,GB:1024**3};return n*(mult[u]||1);}
async function loadErrs(){try{const r=await authF('/stats'),d=await r.json();renderErrs(d.recent_errors||[]);}catch(e){}}
async function fetchDefaultVless(){try{const r=await authF('/api/links'),d=await r.json();const links=d.links||[];const def=links.find(l=>l.limit_bytes===0&&l.active&&!l.expired)||links.find(l=>l.active&&!l.expired)||links[0];document.getElementById('vless-main').textContent=def?def.link_url:'هنوز کانفیگی وجود ندارد';}catch(e){}}
function cpText(id){navigator.clipboard.writeText(document.getElementById(id).textContent).then(()=>toast('کپی شد ✓','ok'))}
function qrFor(id){showQR(document.getElementById(id).textContent)}
function refreshAll(){fetchStats();fetchDefaultVless();loadLinks();if(document.getElementById('pg-subgroups').classList.contains('on'))loadSubs();if(document.getElementById('pg-subscriptions').classList.contains('on'))loadSubsPage();if(document.getElementById('pg-connections').classList.contains('on'))loadConns();if(document.getElementById('pg-logs').classList.contains('on'))loadActivity();toast('رفرش شد','ok')}
async function changePw(){const cur=document.getElementById('cp-cur').value,nw=document.getElementById('cp-new').value,cf=document.getElementById('cp-cf').value;if(!cur||!nw||!cf){toast('همه فیلدها را پر کنید','err');return}if(nw.length<4){toast('حداقل ۴ کاراکتر','err');return}if(nw!==cf){toast('تکرار رمز اشتباه','err');return}try{const r=await authF('/api/change-password',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({current_password:cur,new_password:nw})});if(!r.ok){const d=await r.json();throw new Error(d.detail||'خطا')}toast('رمز تغییر کرد ✓','ok');['cp-cur','cp-new','cp-cf'].forEach(id=>document.getElementById(id).value='');}catch(e){toast('✗ '+e.message,'err')}}
function initCharts(){const c1=document.getElementById('ch1').getContext('2d');const grad1=c1.createLinearGradient(0,0,0,260);grad1.addColorStop(0,'rgba(249,115,22,.38)');grad1.addColorStop(1,'rgba(249,115,22,0)');ch1=new Chart(document.getElementById('ch1'),{type:'line',data:{labels:[],datasets:[{label:'MB',data:[],borderColor:'#F97316',backgroundColor:grad1,fill:true,tension:.42,pointRadius:0,pointHoverRadius:6,pointHoverBackgroundColor:'#F97316',pointHoverBorderColor:'#fff',pointHoverBorderWidth:2,borderWidth:2.5}]},options:{responsive:true,maintainAspectRatio:false,interaction:{mode:'index',intersect:false},plugins:{legend:{display:false},tooltip:{backgroundColor:'rgba(20,20,20,.96)',borderColor:'rgba(249,115,22,.3)',borderWidth:1,titleColor:'#F5F5F5',bodyColor:'#B0B0B0',padding:11,cornerRadius:10,displayColors:false,titleFont:{family:'Vazirmatn',size:11,weight:'700'},bodyFont:{family:'Vazirmatn',size:11},callbacks:{label:v=>`${v.parsed.y.toFixed(2)} مگابایت`}}},scales:{x:{grid:{display:false},border:{display:false},ticks:{color:'#6B6B6B',font:{size:9,family:'Vazirmatn'}}},y:{grid:{color:'rgba(249,115,22,.06)'},border:{display:false},ticks:{color:'#6B6B6B',font:{size:9,family:'Vazirmatn'},callback:v=>v+' MB'}}}}});
const c3ctx=document.getElementById('ch3').getContext('2d');const gradFill3=c3ctx.createLinearGradient(0,0,0,320);gradFill3.addColorStop(0,'rgba(249,115,22,.45)');gradFill3.addColorStop(.6,'rgba(249,115,22,.08)');gradFill3.addColorStop(1,'rgba(249,115,22,0)');ch3=new Chart(document.getElementById('ch3'),{type:'line',data:{labels:[],datasets:[{label:'مصرف',data:[],borderColor:'#F97316',backgroundColor:gradFill3,fill:true,tension:.45,pointRadius:0,pointHoverRadius:7,pointHoverBackgroundColor:'#fff',pointHoverBorderColor:'#F97316',pointHoverBorderWidth:3,borderWidth:3,order:2},{label:'میانگین',data:[],borderColor:'#F59E0B',borderDash:[6,5],borderWidth:1.6,pointRadius:0,fill:false,tension:0,order:1}]},options:{responsive:true,maintainAspectRatio:false,interaction:{mode:'index',intersect:false},plugins:{legend:{display:false},tooltip:{backgroundColor:'rgba(20,20,20,.97)',borderColor:'rgba(249,115,22,.35)',borderWidth:1,titleColor:'#F5F5F5',bodyColor:'#B0B0B0',padding:13,cornerRadius:12,displayColors:true,boxPadding:4,titleFont:{family:'Vazirmatn',size:11.5,weight:'700'},bodyFont:{family:'Vazirmatn',size:11},callbacks:{label:v=>` ${v.dataset.label}: ${v.parsed.y.toFixed(2)} MB`}}},scales:{x:{grid:{display:false},border:{display:false},ticks:{color:'#6B6B6B',font:{size:9.5,family:'Vazirmatn'},maxRotation:0}},y:{grid:{color:'rgba(249,115,22,.05)'},border:{display:false},ticks:{color:'#6B6B6B',font:{size:9.5,family:'Vazirmatn'},callback:v=>v+' MB'}}}}});
ch2=new Chart(document.getElementById('ch2'),{type:'doughnut',data:{labels:['VLESS','VMess/Trojan','WireGuard/Hysteria2'],datasets:[{data:[45,30,25],backgroundColor:['#F97316','#8B5CF6','#10B981'],borderColor:getComputedStyle(document.documentElement).getPropertyValue('--card')||'#1a1a1a',borderWidth:4,hoverOffset:10,borderRadius:6,spacing:3}]},options:{responsive:true,maintainAspectRatio:false,cutout:'72%',plugins:{legend:{position:'bottom',labels:{color:'var(--t2)',font:{size:10,family:'Vazirmatn'},padding:12,usePointStyle:true,pointStyle:'circle'}},tooltip:{backgroundColor:'rgba(20,20,20,.96)',borderColor:'rgba(249,115,22,.3)',borderWidth:1,padding:10,cornerRadius:10,bodyFont:{family:'Vazirmatn'},titleFont:{family:'Vazirmatn'}}}}});
}
let botData={};
async function loadBotPanel(){try{const [products,orders,admins,card]=await Promise.all([fetch('/api/products').then(r=>r.json()),fetch('/api/orders').then(r=>r.json()),fetch('/api/admins').then(r=>r.json()),fetch('/api/settings/card').then(r=>r.json())]);botData={products,orders,admins,card};document.getElementById('bot-products-count').textContent=products.products?.length||0;document.getElementById('bot-orders-count').textContent=orders.orders?.length||0;document.getElementById('bot-admins-count').textContent=admins.admins?.length||0;document.getElementById('bot-card-number').textContent=card.card_number||'—';document.getElementById('bot-card-display').textContent=card.card_number||'—';renderProducts(products.products||[]);renderOrders(orders.orders||[]);renderAdmins(admins.admins||[]);}catch(e){toast('خطا در بارگذاری','err')}}
function renderProducts(products){const el=document.getElementById('bot-products-list');if(!products.length){el.innerHTML='<div class="empty"><i class="ti ti-package-off"></i><p>محصولی وجود ندارد</p></div>';return}el.innerHTML=products.map(p=>`<div class="cfg-card"><div class="cfg-row"><div class="cfg-identity" style="flex:2"><div class="cfg-label">${esc(p.name)}</div><div class="cfg-sub-meta">${p.volume_gb} GB · ${p.duration_days} روز · ${p.speed_mbps} Mbps · ${p.price.toLocaleString()} تومان</div></div><button class="btn btn-d" onclick="deleteProduct('${p.product_id}')"><i class="ti ti-trash"></i></button></div></div>`).join('');}
function renderOrders(orders){const el=document.getElementById('bot-orders-list');const pending=orders.filter(o=>o.status==='pending');if(!pending.length){el.innerHTML='<div class="empty"><i class="ti ti-inbox"></i><p>سفارش در انتظاری وجود ندارد</p></div>';return}el.innerHTML=pending.map(o=>`<div class="cfg-card"><div class="cfg-row"><div class="cfg-identity" style="flex:2"><div class="cfg-label">#${o.order_id}</div><div class="cfg-sub-meta">کاربر: ${o.user_id} · ${o.volume}GB · ${o.duration} روز</div></div><div style="display:flex;gap:5px"><button class="btn btn-p" onclick="approveOrder('${o.order_id}')"><i class="ti ti-check"></i></button><button class="btn btn-d" onclick="rejectOrder('${o.order_id}')"><i class="ti ti-x"></i></button></div></div></div>`).join('');}
function renderAdmins(admins){const el=document.getElementById('bot-admins-list');if(!admins.length){el.innerHTML='<div class="empty"><i class="ti ti-users-off"></i><p>ادمینی وجود ندارد</p></div>';return}const owner=botData.admins?.owner_id;el.innerHTML=admins.map(id=>`<div class="cfg-card"><div class="cfg-row"><div class="cfg-identity" style="flex:2"><div class="cfg-label">${id} ${id===owner?'👑 (اونر)':''}</div></div>${id!==owner?`<button class="btn btn-d" onclick="removeAdmin('${id}')"><i class="ti ti-trash"></i></button>`:''}</div></div>`).join('');}
function switchBotTab(tab){document.querySelectorAll('.bot-tab-content').forEach(el=>el.style.display='none');document.getElementById(`bot-tab-${tab}`).style.display='block';document.querySelectorAll('.traf-range-tab').forEach(el=>el.classList.remove('on'));document.querySelector(`.traf-range-tab[data-tab="bot-${tab}"]`).classList.add('on');}
async function addProduct(){const name=document.getElementById('bot-product-name').value.trim();const volume_gb=parseFloat(document.getElementById('bot-product-volume').value)||0;const duration_days=parseInt(document.getElementById('bot-product-duration').value)||0;const speed_mbps=parseFloat(document.getElementById('bot-product-speed').value)||0;const price=parseFloat(document.getElementById('bot-product-price').value)||0;if(!name||volume_gb<=0||duration_days<=0||price<=0){toast('همه فیلدها را پر کنید','err');return}try{const r=await fetch('/api/products',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({name,volume_gb,duration_days,speed_mbps,price})});if(!r.ok)throw new Error();toast('محصول اضافه شد ✓','ok');loadBotPanel();}catch(e){toast('خطا','err')}}
async function deleteProduct(productId){if(!confirm('حذف این محصول؟'))return;try{await fetch(`/api/products/${productId}`,{method:'DELETE'});toast('حذف شد ✓','ok');loadBotPanel();}catch(e){toast('خطا','err')}}
async function addAdmin(){const user_id=document.getElementById('bot-admin-id').value.trim();if(!user_id){toast('آیدی را وارد کنید','err');return}try{const r=await fetch('/api/admins',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({user_id:parseInt(user_id)})});if(!r.ok)throw new Error();toast('ادمین اضافه شد ✓','ok');loadBotPanel();}catch(e){toast('خطا','err')}}
async function removeAdmin(userId){if(!confirm('حذف این ادمین؟'))return;try{await fetch(`/api/admins/${userId}`,{method:'DELETE'});toast('ادمین حذف شد ✓','ok');loadBotPanel();}catch(e){toast('خطا','err')}}
async function updateCard(){const card=document.getElementById('bot-new-card').value.trim();if(!card){toast('شماره کارت را وارد کنید','err');return}try{const r=await fetch('/api/settings/card',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({card_number:card})});if(!r.ok)throw new Error();toast('به‌روزرسانی شد ✓','ok');loadBotPanel();}catch(e){toast('خطا','err')}}
async function approveOrder(orderId){if(!confirm('تایید این سفارش؟'))return;try{await fetch(`/api/orders/${orderId}`,{method:'PATCH',headers:{'Content-Type':'application/json'},body:JSON.stringify({status:'confirmed'})});toast('سفارش تأیید شد ✓','ok');loadBotPanel();}catch(e){toast('خطا','err')}}
async function rejectOrder(orderId){if(!confirm('رد این سفارش؟'))return;try{await fetch(`/api/orders/${orderId}`,{method:'PATCH',headers:{'Content-Type':'application/json'},body:JSON.stringify({status:'rejected'})});toast('سفارش رد شد','ok');loadBotPanel();}catch(e){toast('خطا','err')}}
document.addEventListener('DOMContentLoaded',async()=>{await checkAuth();initCharts();document.getElementById('set-host').textContent=location.host;document.getElementById('sub-all-url')&&(document.getElementById('sub-all-url').textContent=location.protocol+'//'+location.host+'/sub-all');fetchStats();fetchDefaultVless();loadLinks();loadSubs();setInterval(fetchStats,4000);setInterval(()=>{if(document.getElementById('pg-links').classList.contains('on'))loadLinks();if(document.getElementById('pg-subgroups').classList.contains('on'))loadSubs();if(document.getElementById('pg-subscriptions').classList.contains('on'))loadSubsPage();if(document.getElementById('pg-connections').classList.contains('on'))loadConns();if(document.getElementById('pg-logs').classList.contains('on'))loadActivity();},5000);});
</script>
</body></html>"""
