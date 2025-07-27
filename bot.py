import asyncio, json, base64, os, pytz, random
from datetime import datetime
from aiohttp import ClientSession, ClientTimeout, TCPConnector
from fake_useragent import FakeUserAgent
from colorama import Fore, Style, init as colorama_init

colorama_init(autoreset=True)
wib = pytz.timezone("Asia/Jakarta")

class SparkBot:
    def __init__(self):
        self.headers = {
            "Accept": "application/json",
            "Origin": "https://sparkchain.ai",
            "Referer": "https://sparkchain.ai/",
            "User-Agent": FakeUserAgent().random,
        }
        self.heartbeat_counter = {}
        self.points_latest = {}
        self.use_proxy = False
        self.proxies = []

    def log(self, message, level="info"):
        now = datetime.now().astimezone(wib).strftime('%H:%M:%S')
        icons = {
            "info": f"{Fore.CYAN}ℹ️",
            "success": f"{Fore.GREEN}✅",
            "warn": f"{Fore.YELLOW}⚠️",
            "error": f"{Fore.RED}❌",
            "ping": f"{Fore.MAGENTA}💓",
            "stat": f"{Fore.BLUE}📊",
            "countdown": f"{Fore.YELLOW}⏱",
        }
        print(f"{Fore.LIGHTBLACK_EX}[{now}]{Style.RESET_ALL} {icons.get(level, '')} {Style.BRIGHT}{message}{Style.RESET_ALL}")

    def show_banner(self):
        print("""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🧠 Sparkchain AutoBot by DropsterMind
🚀 Auto Heartbeat | 24 Jam Nonstop | v1.0
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")

    def decode_token_email(self, token):
        try:
            payload = token.split('.')[1]
            padded = payload + '=' * (4 - len(payload) % 4)
            data = json.loads(base64.urlsafe_b64decode(padded))
            return data.get("email", "unknown")
        except:
            return "unknown"

    def load_proxies(self):
        if not os.path.exists("proxy.txt"):
            return []
        with open("proxy.txt") as f:
            return [line.strip() for line in f if line.strip()]

    def get_rotated_proxy(self):
        return random.choice(self.proxies) if self.proxies else None

    async def get_device_id(self, session, token, proxy):
        url = "https://api.sparkchain.ai/devices"
        headers = {**self.headers, "Authorization": f"Bearer {token}"}
        async with session.get(url, headers=headers, proxy=proxy) as res:
            data = await res.json()
            return data[0]["device_id"] if data else None

    async def get_earning(self, token, email):
        url = "https://api.sparkchain.ai/profile"
        headers = {**self.headers, "Authorization": f"Bearer {token}"}
        connector = TCPConnector(ssl=False)
        async with ClientSession(timeout=ClientTimeout(total=30), connector=connector) as session:
            while True:
                try:
                    proxy = self.get_rotated_proxy() if self.use_proxy else None
                    async with session.get(url, headers=headers, proxy=proxy) as res:
                        data = await res.json()
                        points = data.get("total_points", 0)
                        self.points_latest[email] = points
                        self.show_stats(email)
                except Exception as e:
                    self.log(f"{email} | Gagal ambil poin: {e}", "warn")
                await asyncio.sleep(900)

    def show_stats(self, email):
        heartbeat = self.heartbeat_counter.get(email, 0)
        points = self.points_latest.get(email, 0)
        self.log(f"{email}\n  📈 Poin    : {points}\n  💓 Uptime  : {heartbeat}x heartbeat", "stat")

    async def websocket_once(self, token, device_id, email):
        proxy = self.get_rotated_proxy() if self.use_proxy else None
        ws_url = (
            f"wss://ws-v2.sparkchain.ai/socket.io/?token={token}&device_id={device_id}"
            f"&device_version=0.9.2&EIO=4&transport=websocket"
        )
        headers = {
            "Connection": "Upgrade",
            "Upgrade": "websocket",
            "User-Agent": "Mozilla/5.0",
        }
        session = ClientSession(timeout=ClientTimeout(total=180))
        try:
            async with session.ws_connect(ws_url, headers=headers, proxy=proxy) as ws:
                self.log(f"{email} | ✅ WebSocket connected", "success")
                sid = None
                self.heartbeat_counter[email] = 0
                async for msg in ws:
                    if msg.type.name == "TEXT":
                        text = msg.data
                        if text == "2":
                            await ws.send_str("3")
                        elif text.startswith("0"):
                            await ws.send_str("40")
                        elif text.startswith("40") and not sid:
                            try:
                                parsed = json.loads(text[2:])
                                sid = parsed.get("sid")
                                if sid:
                                    self.log(f"{email} | ✅ Registered SID: {sid}", "success")
                                    break
                            except Exception as e:
                                self.log(f"{email} | Gagal parse SID: {e}", "warn")
                for i in range(96):
                    for remaining in range(900, 0, -60):
                        mins = remaining // 60
                        self.log(f"{email} | ⏳ Next ping in {mins} menit...", "countdown")
                        await asyncio.sleep(60)
                    msg = f'42{json.dumps(["up", {"id": sid}])}'
                    try:
                        await ws.send_str(msg)
                        self.heartbeat_counter[email] += 1
                        self.log(f"{email} | 💓 Sent heartbeat #{self.heartbeat_counter[email]}", "ping")
                        self.show_stats(email)
                    except Exception as e:
                        self.log(f"{email} | Ping gagal: {e}", "warn")
                        break
        except Exception as e:
            raise e
        finally:
            await session.close()

    async def run_account(self, token):
        email = self.decode_token_email(token)
        proxy = self.get_rotated_proxy() if self.use_proxy else None
        connector = TCPConnector(ssl=False)
        session = ClientSession(timeout=ClientTimeout(total=120), connector=connector)
        try:
            device_id = await self.get_device_id(session, token, proxy)
            await session.close()
            if not device_id:
                self.log(f"{email} | ❌ Device ID tidak ditemukan.", "error")
                return
            while True:
                try:
                    await self.websocket_once(token, device_id, email)
                    self.log(f"{email} | ℹ️ 24 jam selesai.", "info")
                    break
                except Exception as e:
                    self.log(f"{email} | ⚠️ Disconnect, coba lagi 10 detik... [{e}]", "warn")
                    await asyncio.sleep(10)
        except Exception as e:
            self.log(f"{email} | ❌ Error fatal: {e}", "error")
            await session.close()

    async def main(self):
        self.show_banner()
        jawab = input("Gunakan proxy? (y/n): ").lower()
        self.use_proxy = jawab == 'y'
        if self.use_proxy:
            self.proxies = self.load_proxies()
            if not self.proxies:
                self.log("Proxy dipilih tapi file proxy.txt kosong!", "error")
                return
            self.log(f"Mode proxy aktif ({len(self.proxies)} proxy tersedia)", "info")
        else:
            self.log("Mode proxy nonaktif (direct connection)", "info")

        if not os.path.exists("tokens.txt"):
            self.log("File tokens.txt tidak ditemukan.", "error")
            return
        with open("tokens.txt") as f:
            tokens = [line.strip() for line in f if line.strip()]
        if not tokens:
            self.log("Isi file tokens.txt kosong.", "error")
            return
        self.log(f"🎯 Menjalankan {len(tokens)} akun Sparkchain...", "info")
        tasks = [asyncio.create_task(self.run_account(token)) for token in tokens]
        earning_tasks = [asyncio.create_task(self.get_earning(token, self.decode_token_email(token))) for token in tokens]
        await asyncio.gather(*tasks, *earning_tasks)

if __name__ == "__main__":
    try:
        bot = SparkBot()
        asyncio.run(bot.main())
    except KeyboardInterrupt:
        print(f"{Fore.RED}⛔ Bot dihentikan oleh pengguna.")
