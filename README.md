# 💄 Makyaj Uygulaması (3D Makeup & Face Alignment)

Bu proje, kullanıcıların yüzlerine 3 boyutlu olarak sanal makyaj veya yüz analizi uygulayabildiği, **Flutter** tabanlı bir mobil arayüz ile **Python** tabanlı bir yapay zeka arka ucundan (backend) oluşmaktadır.

## 🧠 Kullanılan Yapay Zeka Modelleri ve Teknolojiler

Projenin görüntü işleme ve 3 boyutlu modelleme kısmında şu modern yapay zeka modelleri kullanılmıştır:

1. **FaceBoxes (Yüz Tespiti)**
   - Yüksek performanslı ve hafif bir yüz tespit modelidir. Fotoğraftaki yüzlerin konumunu (bounding box) yüksek doğrulukla bulmak için kullanılır. (ONNX ve PyTorch formatlarında ağırlıkları mevcuttur).

2. **3DDFA_V2 (3D Dense Face Alignment - MobileNet_V1)**
   - Yüzdeki 3 boyutlu derinliği ve yoğun özellik noktalarını (landmark) hesaplamak için kullanılır. Oldukça hızlı çalışan MobileNet mimarisi üzerine kuruludur. Yüzün 3 boyutlu yapısını kameradan alınan 2 boyutlu fotoğraftan yüksek hassasiyetle çıkarır.

3. **BFM (Basel Face Model)**
   - 3 boyutlu yüz ağı (mesh) ve topolojisini oluşturmak için kullanılan temel istatistiksel modeldir. Yüzün 3 boyutlu haritasının çıkarılmasına ve makyaj dokularının doğru koordinatlara yerleştirilmesine olanak tanır.

4. **Sim3DR**
   - Çıkarılan 3 boyutlu yüz haritasının üzerine ışıklandırma ve doku (texture) render işlemlerini uygulamak için kullanılan 3D render motorudur.

---

## 🚀 Kurulum ve Çalıştırma

Proje iki ana bileşenden oluşmaktadır: `mobiluygulama` (Frontend) ve `3boyutsonhal` (Backend).

### 1. Backend (Yapay Zeka Sunucusu)
Öncelikle bilgisayarınızda Python yüklü olmalıdır.

```bash
cd 3boyutsonhal
# Gerekli kütüphaneleri yükleyin
pip install -r requirements.txt

# Sunucuyu başlatın
python server.py
# (veya start_server.py)
```

### 2. Frontend (Flutter Mobil Uygulaması)
Bilgisayarınızda Flutter SDK yüklü olmalıdır.

```bash
cd mobiluygulama
# Gerekli paketleri indirin
flutter pub get

# Uygulamayı çalıştırın
flutter run
```

## 📝 Notlar
Bu repo, projenin tamamen çalışır halini içerir. Gereksiz derleme (build) önbellekleri, sanal ortamlar (venv) ve büyük sıkıştırılmış arşiv dosyaları projenin hafif ve temiz kalması amacıyla bilerek dışarıda bırakılmıştır. Kodunuzu klonladığınızda ilgili kurulum komutları (pip/flutter) çalışması için gereken her şeyi otomatik indirecektir.
