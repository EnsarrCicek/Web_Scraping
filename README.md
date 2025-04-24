# TradingView Veri Çekme Projesi

Bu proje, TradingView web sitesinden Selenium, BeautifulSoup ve Pandas kullanarak veri çekmek için oluşturulmuştur.

## Gereksinimler

- Python 3.8 veya üzeri
- Chrome tarayıcısı

## Kurulum

1. Gerekli paketleri yükleyin:
```bash
pip install -r requirements.txt
```

2. Chrome tarayıcısının yüklü olduğundan emin olun.

## Kullanım

Programı çalıştırmak için:
```bash
python tradingview_scraper.py
```

Varsayılan olarak Bitcoin/USD (BTCUSD) çiftinin verilerini çeker ve `tradingview_data.csv` dosyasına kaydeder.

## Özelleştirme

Farklı bir sembol için veri çekmek isterseniz, `main()` fonksiyonundaki `symbol` değişkenini değiştirebilirsiniz.

## Notlar

- TradingView'ın HTML yapısı değişebilir, bu durumda kodun güncellenmesi gerekebilir.
- Veri çekme işlemi için TradingView hesabı gerekebilir.
- Çok sık istek göndermekten kaçının, IP adresiniz engellenebilir. 