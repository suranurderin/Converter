# Converter

Bu proje, ses, video, PDF ve Word dosyaları arasında kolayca dönüşüm yapmanızı sağlayan bir Python uygulamasıdır. MoviePy, pdf2docx ve docx2pdf gibi popüler kütüphaneleri kullanır.

## Özellikler
- **Ses -> Ses**: Farklı ses formatları arasında dönüşüm.
- **Ses -> Video**: Bir ses dosyasını, isteğe bağlı olarak bir resimle veya siyah ekranla video formatına dönüştürme.
- **Video -> Ses**: Videodan sesi ayırıp ses dosyası olarak kaydetme.
- **Video -> Video**: Video formatları arasında dönüşüm.
- **PDF -> Word**: PDF dosyasını stilini koruyarak Word dosyasına çevirme.
- **Word -> PDF**: Word dosyasını PDF formatına dönüştürme.

## Gereksinimler
- Python 3.7+
- moviepy
- numpy
- pdf2docx
- docx2pdf

Gereken kütüphaneleri yüklemek için:

```bash
pip install moviepy numpy pdf2docx docx2pdf
```

## Kullanım

Terminalde aşağıdaki komutla uygulamayı başlatabilirsiniz:

```bash
python app.py
```

Ardından menüden yapmak istediğiniz işlemi seçebilirsiniz.

## Notlar
- Dönüştürme işlemleri sırasında dosya yollarını doğru girdiğinizden emin olun.
- Bazı format dönüşümleri için ek kütüphaneler veya sistemde yüklü yazılımlar (ör. ffmpeg) gerekebilir.

## Lisans
MIT

