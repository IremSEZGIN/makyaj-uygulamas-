# 3D Makyaj Uygulaması - Flutter Mobil Uygulama

Bu proje, web sitesi tasarımına dayalı bir Flutter mobil uygulamasıdır. AI destekli sanal makyaj deneyimi sunar.

## Özellikler

- ✅ Kullanıcı girişi ve kayıt sistemi
- ✅ Ana sayfa ile kategori ve öne çıkan ürünler
- ✅ Ürün listeleme ve filtreleme
- ✅ Ürün detay sayfaları
- ✅ Sepet yönetimi
- ✅ Profil ve ayarlar
- ✅ 3D yüz tarama simülasyonu
- ✅ Sanal makyaj deneme
- ✅ Beğenilen ürünler
- ✅ Alt navigasyon menüsü

## Kurulum

1. Flutter SDK'nın yüklü olduğundan emin olun
2. Proje dizinine gidin:
   ```bash
   cd makeup_app
   ```
3. Bağımlılıkları yükleyin:
   ```bash
   flutter pub get
   ```
4. Uygulamayı çalıştırın:
   ```bash
   flutter run
   ```

## Proje Yapısı

```
lib/
├── main.dart                 # Ana uygulama dosyası
├── models/
│   ├── app_state.dart       # Uygulama durumu yönetimi
│   └── product.dart         # Ürün modeli
├── screens/
│   ├── login_screen.dart
│   ├── signup_screen.dart
│   ├── home_screen.dart
│   ├── products_screen.dart
│   ├── product_detail_screen.dart
│   ├── cart_screen.dart
│   ├── profile_screen.dart
│   ├── settings_screen.dart
│   ├── face_scan_screen.dart
│   └── virtual_makeup_screen.dart
├── widgets/
│   ├── bottom_nav.dart      # Alt navigasyon menüsü
│   └── logo.dart            # Logo widget'ı
└── data/
    └── products_data.dart   # Ürün verileri
```

## Kullanılan Paketler

- `shared_preferences`: Yerel veri saklama
- `cached_network_image`: Resim önbellekleme
- `flutter_svg`: SVG desteği (opsiyonel)

## Ekranlar

### Giriş ve Kayıt
- Kullanıcı girişi ve kayıt ekranları
- Şifre sıfırlama (simüle edilmiş)

### Ana Sayfa
- Hero bölümü
- Hızlı erişim butonları (Yüz Tarama, Sanal Makyaj, Ürünler)
- Kategoriler
- Öne çıkan ürünler
- AI asistan banner'ı

### Ürünler
- Kategori filtreleme
- Arama özelliği
- Ürün grid görünümü
- Beğeni özelliği

### Ürün Detayı
- Ürün görselleri
- Fiyat ve özellikler
- Bilgiler, kullanım ve yorumlar sekmeleri
- Sepete ekleme

### Sepet
- Ürün listesi
- Toplam hesaplama
- Sipariş tamamlama

### Profil
- Kullanıcı bilgileri
- Beğenilen ürünler
- Cilt tipi seçimi

### Ayarlar
- Hesap ayarları
- Bildirim tercihleri
- Çıkış yapma

### Yüz Tarama
- Tarama simülasyonu
- İlerleme göstergesi
- 3D model oluşturma (simüle edilmiş)

### Sanal Makyaj
- Kategori seçimi
- Renk paleti
- 3D model görüntüleme (simüle edilmiş)
- Uygulanan makyaj gösterimi

## Notlar

- Bu uygulama web sitesi tasarımının Flutter'a uyarlanmış halidir
- 3D modelleme ve gerçek yüz tarama özellikleri simüle edilmiştir
- Ürün verileri statik olarak tanımlanmıştır
- Gerçek bir uygulama için backend entegrasyonu gereklidir

## Geliştirme

Uygulamayı geliştirmek için:

1. Yeni ekranlar ekleyin: `lib/screens/` klasörüne
2. Widget'lar ekleyin: `lib/widgets/` klasörüne
3. Modeller ekleyin: `lib/models/` klasörüne
4. Veri ekleyin: `lib/data/` klasörüne

## Lisans

Bu proje eğitim amaçlıdır.

