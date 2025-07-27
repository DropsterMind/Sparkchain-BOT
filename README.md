<h1>🔥 Sparkchain AutoBot by DropsterMind</h1>

<p>
  Bot otomatis untuk melakukan <strong>heartbeat</strong> setiap 15 menit dan memantau <strong>earning poin</strong> dari Sparkchain.<br>
  Dilengkapi dengan <strong>proxy support (opsional)</strong>, <strong>auto reconnect</strong>, <strong>log warna CLI</strong>, dan <strong>statistik real-time</strong>.
</p>

<hr>

<h2>✨ Fitur Utama</h2>
<ul>
  <li>✅ Auto WebSocket connect & register SID</li>
  <li>✅ Ping heartbeat tiap 15 menit (96x sehari)</li>
  <li>✅ Statistik poin & uptime (heartbeat)</li>
  <li>✅ Auto reconnect jika disconnect</li>
  <li>✅ Countdown ping di terminal</li>
  <li>✅ Proxy support (rotasi random dari <code>proxy.txt</code>)</li>
  <li>✅ CLI log berwarna dengan watermark <code>by DropsterMind</code></li>
</ul>

<hr>

<h2>📁 Struktur File</h2>
<pre><code>
📦 sparkchain-bot/
├── bot.py               # File utama bot
├── tokens.txt           # List token Sparkchain (1 per baris)
├── proxy.txt            # (Opsional) List proxy (1 per baris)
└── README.md            # Dokumentasi ini
</code></pre>

<hr>

<h2>🧠 Cara Install & Jalankan</h2>

<h3>1. Clone Repo (atau download zip)</h3>
<pre><code>git clone https://github.com/DropsterMind/Sparkchain-BOT.git
cd Sparkchain-BOT</code></pre>

<h3>2. Install dependencies</h3>
<pre><code>pip3 install -r requirements.txt</code></pre>

<p><em>Atau manual:</em></p>
<pre><code>pip3 install aiohttp fake-useragent colorama pytz</code></pre>

<h3>3. Siapkan file <code>tokens.txt</code></h3>
<p>Isi dengan 1 token Bearer per baris:</p>
<pre><code>eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...</code></pre>

<h3>4. (Opsional) Siapkan <code>proxy.txt</code></h3>
<p>Format:</p>
<pre><code>http://username:password@host:port
http://host:port</code></pre>

<h3>5. Jalankan bot</h3>
<pre><code>python3 bot.py</code></pre>

<p>
  Saat diminta:<br>
  <code>Gunakan proxy? (y/n):</code><br>
  Jawab <strong>y</strong> jika ingin pakai proxy dari <code>proxy.txt</code>, atau <strong>n</strong> jika ingin koneksi langsung.
</p>

<hr>

<h2>📊 Contoh Tampilan</h2>

<pre><code>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🧠 Sparkchain AutoBot by DropsterMind
🚀 Auto Heartbeat | 24 Jam Nonstop | v1.0
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[12:01:23] ✅ WebSocket connected
[12:01:23] ✅ Registered SID: mGMgMAONVGr3eP873Ge7
[12:01:23] ⏳ Next ping in 15 menit...
[12:16:24] 💓 Sent heartbeat #1
📊 Stats: Poin: 9055201.5 | Uptime: 1x heartbeat
</code></pre>

<hr>

<h2>💬 FAQ</h2>

<p><strong>Q: Apakah aman menjalankan lebih dari 1 akun?</strong><br>
✅ Ya, bot ini mendukung multi-token dan akan menjalankan semuanya secara paralel.</p>

<p><strong>Q: Apakah proxy wajib?</strong><br>
❌ Tidak. Proxy hanya opsional. Kamu bisa memilih saat bot dijalankan.</p>

<p><strong>Q: Apakah saya bisa menjalankan di VPS?</strong><br>
✅ Bisa. Gunakan VPS berbasis Ubuntu/Debian dan install Python 3.7+</p>

<hr>

<h2>💖 Credit</h2>

<p>
  Developed by: <strong>DropsterMind</strong><br>
  Telegram: <a href="https://t.me/dropstermind">@DropsterMind</a>
</p>

<hr>

<h2>📜 Lisensi</h2>

<p>
  MIT License – bebas digunakan, dimodifikasi, atau disebarluaskan selama mencantumkan kredit.
</p>
