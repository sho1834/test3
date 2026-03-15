import tkinter as tk
from tkinter import messagebox
import threading
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def log(msg):
    log_box.insert(tk.END, msg + "\n")
    log_box.see(tk.END)
    print(msg)

def run_login():
    u_id = id_entry.get()
    u_pw = pw_entry.get()

    def task():
        driver = None
        try:
            log("🚀 Seleniumを起動中...")
            options = Options()
            
            #options.add_argument('--headless')          # ヘッドレス指定
           # options.add_argument('--no-sandbox')        # 権限エラー対策（念のため）
           # options.add_argument('--disable-gpu')       # グラフィック負荷軽減
            
            # ブラウザの自動設定
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=options)

            log("🌐 ログインページへ移動...")
            driver.get("https://salonboard.com/login/")

            log("✍️ ID/PWを入力中...")
            driver.find_element(By.NAME, "userId").send_keys(u_id)
            driver.find_element(By.NAME, "password").send_keys(u_pw)

            log("🖱️ ログインボタンをクリック...")
            # 前回の失敗：複合クラス名は CSS_SELECTOR で指定するのが正解です
            login_btn = driver.find_element(By.CSS_SELECTOR, ".common-CNCcommon__primaryBtn.loginBtnSize")
            login_btn.click()

            log("✅ ログインボタンを押しました。5秒間待機します...")
            import time
            time.sleep(5)
            
            log(f"📍 現在のURL: {driver.current_url}")
            messagebox.showinfo("成功", "ブラウザ操作が完了しました")

        except Exception as e:
            log(f"⚠️ エラー発生: {str(e)}")
            messagebox.showerror("エラー", str(e))
        finally:
            if driver:
                driver.quit()
                log("🏁 ブラウザを閉じました")

    # Seleniumはスレッドで動かしてもNotImplementedErrorが出ません
    threading.Thread(target=task, daemon=True).start()

# --- GUI構築 (Tkinter) ---
root = tk.Tk()
root.title("SalonBoard Login - Selenium Version")
root.geometry("400x500")

tk.Label(root, text="ユーザーID").pack(pady=(20, 0))
id_entry = tk.Entry(root, width=30)
id_entry.pack()

tk.Label(root, text="パスワード").pack(pady=(10, 0))
pw_entry = tk.Entry(root, width=30, show="*")
pw_entry.pack()

start_btn = tk.Button(root, text="ログイン開始", command=run_login, bg="#0078d7", fg="white")
start_btn.pack(pady=20)

log_box = tk.Text(root, height=15, width=50)
log_box.pack(padx=10, pady=10)

root.mainloop()