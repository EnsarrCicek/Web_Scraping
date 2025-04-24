from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
import os
import platform
import pyautogui
import sys

# PyAutoGUI güvenlik ayarları
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.5

def setup_driver():
    try:
        # Sistem bilgisini kontrol et
        print(f"Python versiyonu: {platform.python_version()}")
        print(f"Sistem mimarisi: {platform.architecture()[0]}")
        
        # Chrome sürücüsünü manuel olarak belirtelim
        driver_path = os.path.join(os.getcwd(), "chromedriver.exe")
        print(f"Chrome sürücüsü yolu: {driver_path}")
        
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--start-maximized")  # Pencereyi tam ekran yap
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        service = Service(executable_path=driver_path)
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # Bot tespitini engelleme
        driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
            'source': '''
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                })
            '''
        })
        
        return driver
    except Exception as e:
        print(f"Chrome sürücüsü yüklenirken hata oluştu: {str(e)}")
        return None

def move_mouse_smoothly(x, y):
    try:
        # Mevcut fare konumunu al
        current_x, current_y = pyautogui.position()
        
        # Hedef noktaya doğru yavaşça hareket et
        steps = 2  # Hareket adımı sayısı
        
        for i in range(steps + 1):
            # Her adımda gidilecek noktayı hesapla
            next_x = current_x + (x - current_x) * i / steps
            next_y = current_y + (y - current_y) * i / steps
            
            # Fareyi hareket ettir
            pyautogui.moveTo(next_x, next_y, duration=0.1)
            
            # Rastgele küçük sapmalar ekle
            if i != steps:  # Son adımda sapma ekleme
                next_x += random.uniform(-5, 5)
                next_y += random.uniform(-5, 5)
            
            # Küçük bekleme ekle
            time.sleep(random.uniform(0.05, 0.1))
        
        return True
    except Exception as e:
        print(f"Fare hareketi sırasında hata: {str(e)}")
        return False

def handle_cloudflare(driver):
    try:
        print("Cloudflare doğrulaması bekleniyor...")
        time.sleep(3)
        
        # Tarayıcı penceresinin konumunu al
        window_rect = driver.get_window_rect()
        print(f"Pencere konumu: x={window_rect['x']}, y={window_rect['y']}")
        
        # Checkbox'ın tarayıcı penceresine göre koordinatları
        checkbox_x = window_rect['x'] + 425
        checkbox_y = window_rect['y'] + 475
        
        print(f"Hedef koordinatlar: x={checkbox_x}, y={checkbox_y}")
        
        # 3 kez tıklama yap, her tıklama arasında 15 saniye bekle
        for i in range(3):
            print(f"\nTıklama {i+1}/3 yapılıyor...")
            
            # Fareyi hareket ettir ve tıkla
            if move_mouse_smoothly(checkbox_x, checkbox_y):
                print("Fare hedef konuma ulaştı, tıklanıyor...")
                time.sleep(0.5)
                pyautogui.click()
                print(f"{i+1}. tıklama gerçekleştirildi!")
                
                if i < 2:  # Son tıklamadan sonra beklemeye gerek yok
                    print("Sonraki tıklama için 15 saniye bekleniyor...")
                    time.sleep(15)
        
        # Son tıklamadan sonra 10 saniye daha bekle
        print("\nDoğrulama tamamlandı, yönlendirme bekleniyor...")
        time.sleep(10)
        return True
        
    except Exception as e:
        print(f"Cloudflare doğrulaması sırasında hata: {str(e)}")
        return False

def scrape_appointments():
    driver = setup_driver()
    if not driver:
        return None
        
    try:
        # Randevu sayfasını aç
        url = "https://it-tr-appointment.idata.com.tr/tr"
        driver.get(url)
        
        # Sayfanın yüklenmesini bekle
        time.sleep(5)
        
        # Cloudflare doğrulamasını yap
        if not handle_cloudflare(driver):
            print("Cloudflare doğrulaması başarısız!")
            return None
            
        print("Cloudflare doğrulaması başarılı!")
        
        # Doğrulama sonrası uzun bekleme ekle
        print("Yönlendirme bekleniyor...")
        time.sleep(30)  # 30 saniye bekle
        
        # Sayfa kaynağını al
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        
        # Verileri çek
        appointments = []
        
        # Örnek olarak müsait randevuları çekelim
        available_slots = soup.find_all('div', {'class': 'appointment-slot'})
        
        for slot in available_slots:
            appointment_data = {
                'Tarih': slot.find('span', {'class': 'date'}).text if slot.find('span', {'class': 'date'}) else 'Bilinmiyor',
                'Saat': slot.find('span', {'class': 'time'}).text if slot.find('span', {'class': 'time'}) else 'Bilinmiyor',
                'Durum': 'Müsait'
            }
            appointments.append(appointment_data)
        
        return appointments
        
    except Exception as e:
        print(f"Hata oluştu: {str(e)}")
        return None
        
    finally:
        if driver and len(appointments) == 0:  # Veri çekilemezse tarayıcıyı açık tut
            print("Tarayıcı açık bırakılıyor...")
            time.sleep(3600)  # 1 saat açık tut
        elif driver:
            driver.quit()

def main():
    # Kullanıcıya hazır olması için süre ver
    print("Program 5 saniye içinde başlayacak...")
    print("Lütfen fareyi hareket ettirmeyin!")
    time.sleep(5)
    
    appointments = scrape_appointments()
    
    if appointments:
        df = pd.DataFrame(appointments)
        print(df)
        # DataFrame'i CSV dosyasına kaydet
        df.to_csv('randevu_verileri.csv', index=False, encoding='utf-8-sig')
        print("Veriler başarıyla kaydedildi.")
    else:
        print("Veri çekilemedi.")

if __name__ == "__main__":
    main() 