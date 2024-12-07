
# Hava Aracı Üretim Uygulaması

Bu proje, hava aracı üretim sürecini yönetmek için bir web tabanlı uygulama sunar. Kullanıcılar, montaj takımları ve üretim ekipleri ile parça ve hava aracı üretimi yapabilir, üretim sürecini takip edebilir.

## İçindekiler

1. [Başlangıç](#başlangıç)
2. [Kurulum](#kurulum)
   - [Python Ortamı](#python-ortamı)
   - [NPM ve Tailwind](#npm-ve-tailwind)
   - [Docker](#docker)
3. [Veriler](#veriler)
4. [Kullanım](#kullanım)
5. [Fonksiyonalite](#fonksiyonalite)
6. [Teknoloji](#teknoloji)
   - [Ekstralar (Bonus)](#ekstralar-bonus)
7. [Requirements.txt](#requirementstxt)
8. [Ekran Görüntüleri](#ekran-görüntüleri)

## Başlangıç

Proje, hava aracı üretimi ve parça montajı yönetimini kolaylaştırmak için tasarlanmıştır. Bu doküman, projeyi yerel bir makinede çalıştırmak için gerekli adımları açıklamaktadır.

## Kurulum

### Python Ortamı

1. Gerekli bağımlılıkları kurmak için bir sanal ortam oluşturun ve aktif hale getirin:

   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows için: venv\\Scripts\\activate
   ```
2. Gerekli Python paketlerini yükleyin:

    ```bash
    pip install -r requirements.txt
    ```

### NPM ve Tailwind

1. Node.js ve NPM'in yüklü olduğundan emin olun. Ardından Tailwind CSS için bağımlılıkları yükleyin:

    ```bash
    npm install
    ```
2. Tailwind'i derlemek için aşağıdaki komutu çalıştırın:

    ```bash
    npx tailwindcss -i ./src/input.css -o ./dist/output.css --watch
    ```
### Docker

1. Docker ve Docker Compose yüklü olduğundan emin olun.

2. Docker kapsayıcısını oluşturmak ve başlatmak için:

    ```bash
    docker-compose up --build
    ```

## Veriler

* Parçalar
  * Kanat
  * Gövde
  * Kuyruk
  * Aviyonik  
* Uçaklar
  * TB2
  * TB3
  * AKINCI
  * KIZILELMA
* Takımlar
  * Kanat Takımı
  * Gövde Takımı
  * Kuyruk Takımı
  * Aviyonik Takımı
  * Montaj Takımı

## Kullanım

* Montaj takımları ve diğer parça üretici ekiplerin üretim sürecini yönetmek için kullanılan uygulama.
* Yeni parçalar üretmek için parça üretiminde çalışma yetkinliği bulunan kişi ile iletişime geç.
* Daha detaylı bilgileri görüntülemek için montajcılar ile iletişime geç.
  * Yeterli sayıda parçan varsa hava aracının üretimini de montajcılar yapar.

## Fonksiyonalite

* ✅ Personel giriş ekranı.
* ✅ Personel takımı:
  * Bir takımda birden fazla personel olabilir `CASCADE`  
  * Takımların kendi parçalarını üretme, listeleme ve geri dönüşüme gönderme işlemleri `CRUD`
  * Takımlar kendi sorumluluğundan başka parça üretemez. `Permissions`
  * Montaj takımının bütün uyumlu parçaları birleştirerek 1 uçak üretmesi gerekmektedir.
    * 1 Gövde
    * 1 Kuyruk
    * 1 Aviyonik
    * 2 Kanat
* ✅ Her parça uçağa özeldir. `1-1` , `One-to-One Relationship`
* ✅ Montaj takımı üretilen uçakları listeleyebilir.
* ✅ Envanterde eksik parça olduğunda `Notifications` ile eksik miktarı bildirilir.
* ✅ 1 uçakta kullanılan parça, başka uçakta kullanılamaz, kullanılma durumu "kullanıldı" ise tekrar kullanılamaz. `1-1` , `One-to-One Relationship`
* ✅ Uçaklar için bütün parçaları oluşturup monte ettikten sonra kullanılan parçaların sayısını ve hangi uçakta kullanıldığının bilgisi tutulur.
* ✅ Montaj Personeli ekranında üretilebilir ,halihazırda parçaları tam olan, uçakların listesi tutulur.

## Teknoloji
* Python
* Django
* Django Rest Framework
* PostgreSQL
* Docker
* Docker Compose
* Tailwind CSS

### Ekstralar (Bonus)
* Projenin docker ile ayağa kalkması
* İyi hazırlanmış dökümantasyon ve yorum satırları
* Birim testi
* Listeleme sayfaları için datatable kullanılması
* Server-side datatable kullanılması
* Ön yüzde asenkron (Ajax, fetch vs.) yapı kullanılması
* İlişkisel tabloların ayrı ayrı tutulması
* Django için ekstra kütüphaneler kullanılması
* Ön yüzde (Front-End) Bootstrap, Tailwind, Jquery vs. kullanılması
* API docs (swagger)
* API security (jwt, token)



## Requirements.txt

```Requirements.txt
asgiref==3.8.1
Django==5.1.4
psycopg2==2.9.10
sqlparse==0.5.2
tzdata==2024.2
djangorestframework==3.14.0
drf-spectacular==0.26.2
djangorestframework-simplejwt==5.2.2
django-filter==24.3
```

## Ekran Görüntüleri

<h1 align="center">
  <p align="center">AI-Generated Logo</p>
    <img
      height="128"
      width="128"
      src="/static/images/aircraft-logo.png"
      alt="AI-Generated Logo">
</h1>

* Giriş Ekranı
<h1 align="center">
    <img
      height="500"
      width="500"
      src="/static/images/Login-screen.png"
</h1>

* Giriş Bildirimi
<h1 align="center">
    <img
      height="500"
      width="500"
      src="/static/images/Giris-bildirimi.png"
</h1>

* `Parça` Üretimi
    Hedef `Hava Aracı` seçilir ve `Parça`  üretilir.
<h1 align="center">
    <img
      height="500"
      width="500"
      src="/static/images/parca-uretimi.png"
</h1>

* `Parça` Silme Paneli
<h1 align="center">
    <img
      height="500"
      width="500"
      src="/static/images/parca-silme-paneli.png"
</h1>

* `Parça` Geri Dönüşümü
    `6:52`'de oluşturulan `Akıncı` için üretilmiş `KUYRUK` silindi.
<h1 align="center">
    <img
      height="500"
      width="500"
      src="/static/images/parca-geridonusumu.png"
</h1>

* `Takım` içerisindeki `Parça` işlemleri izin kontrolleri
    Sadece kendi takımının ürettiği `Parça`yı silebilir ve kullanılmış `Parça`ları silemez.
<h1 align="center">
    <img
      height="500"
      width="500"
      src="/static/images/takim-izin-kontrolu.png"
</h1>

* Montaj Personeli Ekranı
    Kullanılmış ve Kullanılmamış `Parça`ların ayrı listeleri
<h1 align="center">
    <img
      height="500"
      width="500"
      src="/static/images/montaj-personeli-ekrani.png"
</h1>

  * `Parça`ları tam ve üretime hazır olan Hava Aracı listesi
<h1 align="center">
    <img
      height="500"
      width="500"
      src="/static/images/montaj-personeli-ekrani2.png"
</h1>

* Eksik `Parça` Bildirimi
<h1 align="center">
    <img
      height="500"
      width="500"
      src="/static/images/eksik-parca-bildirimi.png"
</h1>

* Üretim sonrası `Hava Aracı` listeleri güncellemesi
<h1 align="center">
    <img
      height="500"
      width="500"
      src="/static/images/uretim-sonrasi-montaj.png"
</h1>

* Üretim sonrası `Parça` listeleri
<h1 align="center">
    <img
      height="500"
      width="500"
      src="/static/images/kullanilmis-parca-guncellemesi.png"
</h1>

