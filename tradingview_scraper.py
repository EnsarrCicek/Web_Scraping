from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import time

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Tarayıcıyı arka planda çalıştır
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def scrape_tradingview(symbol):
    driver = setup_driver()
    try:
        # TradingView sayfasını aç
        url = f"https://www.tradingview.com/symbols/{symbol}/"
        driver.get(url)
        
        # Sayfanın yüklenmesini bekle
        time.sleep(5)  # Sayfanın tam yüklenmesi için bekle
        
        # Sayfa kaynağını al
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        
        # Verileri çek
        # Not: TradingView'ın HTML yapısına göre bu kısmı güncellemeniz gerekebilir
        data = {
            'Sembol': symbol,
            'Fiyat': soup.find('div', {'class': 'tv-symbol-price-quote__value'}).text,
            'Değişim': soup.find('div', {'class': 'tv-symbol-price-quote__change'}).text
        }
        
        return data
        
    except Exception as e:
        print(f"Hata oluştu: {str(e)}")
        return None
        
    finally:
        driver.quit()

def main():
    # Örnek kullanım
    symbol = "BTCUSD"  # Bitcoin/USD çifti
    data = scrape_tradingview(symbol)
    
    if data:
        df = pd.DataFrame([data])
        print(df)
        # DataFrame'i CSV dosyasına kaydet
        df.to_csv('tradingview_data.csv', index=False)
        print("Veriler başarıyla kaydedildi.")
    else:
        print("Veri çekilemedi.")

if __name__ == "__main__":
    main() 