from moviepy.editor import VideoFileClip, AudioFileClip, ImageClip
from pathlib import Path
import numpy as np

# Yeni eklenen kütüphaneler
from pdf2docx import Converter
from docx2pdf import convert as docx2pdf_convert

# ------------------------
# Yardımcı Fonksiyonlar
# ------------------------
def ensure_path(input_file):
    path = Path(input_file)
    if not path.exists():
        raise FileNotFoundError(f"❌ Dosya bulunamadı: {path}")
    return path

def get_output_path(input_path, output_name, new_ext):
    name = output_name or input_path.stem
    return input_path.parent / f"{name}.{new_ext}"

# ------------------------
# Ses -> Ses
# ------------------------
def convert_audio(input_file, output_ext, output_name=None, overwrite=True):
    input_path = ensure_path(input_file)
    output_path = get_output_path(input_path, output_name, output_ext)

    if output_path.exists() and not overwrite:
        print(f"⏩ Atlandı (zaten var): {output_path}")
        return str(output_path)

    with AudioFileClip(str(input_path)) as audio:
        audio.write_audiofile(str(output_path))

    print(f"✅ Ses dönüştürüldü: {output_path}")
    return str(output_path)

# ------------------------
# Ses -> Video
# ------------------------
VIDEO_FORMATS = {"mp4", "avi", "mov"}

def convert_audio_to_video(input_file, output_ext="mp4", output_name=None, image_file=None, overwrite=True):
    if output_ext.lower() not in VIDEO_FORMATS:
        raise ValueError(f"❌ {output_ext} geçerli değil. Desteklenenler: {VIDEO_FORMATS}")

    input_path = ensure_path(input_file)
    output_path = get_output_path(input_path, output_name, output_ext)

    if output_path.exists() and not overwrite:
        print(f"⏩ Atlandı (zaten var): {output_path}")
        return str(output_path)

    with AudioFileClip(str(input_file)) as audio:
        if image_file:
            video = ImageClip(str(image_file)).set_duration(audio.duration).set_audio(audio)
        else:
            black_frame = np.zeros((720, 1280, 3), dtype=np.uint8)
            video = ImageClip(black_frame).set_duration(audio.duration).set_audio(audio)

        codec = {"mp4": "libx264", "mov": "libx264", "avi": "png"}[output_ext]
        video.write_videofile(str(output_path), fps=24, codec=codec)

    print(f"✅ Ses videoya dönüştürüldü: {output_path}")
    return str(output_path)

# ------------------------
# Video -> Ses
# ------------------------
def convert_video_to_audio(input_file, output_ext="mp3", output_name=None, overwrite=True):
    input_path = ensure_path(input_file)
    output_path = get_output_path(input_path, output_name, output_ext)

    if output_path.exists() and not overwrite:
        print(f"⏩ Atlandı (zaten var): {output_path}")
        return str(output_path)

    with VideoFileClip(str(input_file)) as clip:
        if clip.audio is None:
            raise RuntimeError("❌ Videoda ses bulunamadı.")
        clip.audio.write_audiofile(str(output_path))

    print(f"✅ Video sesten ayrıldı: {output_path}")
    return str(output_path)

# ------------------------
# Video -> Video (format değişimi)
# ------------------------
def convert_video(input_file, output_ext="mp4", output_name=None, overwrite=True):
    if output_ext.lower() not in VIDEO_FORMATS:
        raise ValueError(f"❌ {output_ext} geçerli değil. Desteklenenler: {VIDEO_FORMATS}")

    input_path = ensure_path(input_file)
    output_path = get_output_path(input_path, output_name, output_ext)

    if output_path.exists() and not overwrite:
        print(f"⏩ Atlandı (zaten var): {output_path}")
        return str(output_path)

    with VideoFileClip(str(input_file)) as video:
        codec = {"mp4": "libx264", "mov": "libx264", "avi": "png"}[output_ext]
        video.write_videofile(str(output_path), fps=video.fps or 24, codec=codec)

    print(f"✅ Video dönüştürüldü: {output_path}")
    return str(output_path)

# ------------------------
# PDF -> Word (stil koruyarak)
# ------------------------
def convert_pdf_to_word(input_file, output_name=None, overwrite=True):
    input_path = ensure_path(input_file)
    output_path = get_output_path(input_path, output_name, "docx")

    if output_path.exists() and not overwrite:
        print(f"⏩ Atlandı (zaten var): {output_path}")
        return str(output_path)

    # pdf2docx kullanımı
    cv = Converter(str(input_path))
    cv.convert(str(output_path), start=0, end=None)
    cv.close()

    print(f"✅ PDF Word'e dönüştürüldü (stil korundu): {output_path}")
    return str(output_path)

# ------------------------
# Word -> PDF
# ------------------------
def convert_word_to_pdf(input_file, output_name=None, overwrite=True):
    input_path = ensure_path(input_file)
    output_path = get_output_path(input_path, output_name, "pdf")

    if output_path.exists() and not overwrite:
        print(f"⏩ Atlandı (zaten var): {output_path}")
        return str(output_path)

    docx2pdf_convert(str(input_path), str(output_path))
    print(f"✅ Word PDF'e dönüştürüldü: {output_path}")
    return str(output_path)

# ------------------------
# Menü
# ------------------------
def main():
    print("\n🎬 Dönüştürücü")
    print("1) Ses -> Video")
    print("2) Video -> Ses")
    print("3) Ses -> Ses")
    print("4) Video -> Video")
    print("5) PDF -> Word")
    print("6) Word -> PDF")

    choice = input("Seçim (1-6): ").strip()

    try:
        if choice == "1":
            audio_file = input("Ses dosyası: ").strip()
            fmt = input("Hedef video formatı (mp4/avi/mov): ").strip().lower()
            img = input("Arka plan resmi (boş = siyah ekran): ").strip() or None
            out_name = input("Yeni dosya ismi (boş = orijinal isim): ").strip() or None
            convert_audio_to_video(audio_file, fmt, output_name=out_name, image_file=img)

        elif choice == "2":
            video_file = input("Video dosyası: ").strip()
            fmt = input("Hedef ses formatı (mp3/wav/ogg): ").strip().lower()
            out_name = input("Yeni dosya ismi (boş = orijinal isim): ").strip() or None
            convert_video_to_audio(video_file, fmt, output_name=out_name)

        elif choice == "3":
            audio_file = input("Ses dosyası: ").strip()
            fmt = input("Hedef ses formatı (mp3/wav/ogg): ").strip().lower()
            out_name = input("Yeni dosya ismi (boş = orijinal isim): ").strip() or None
            convert_audio(audio_file, fmt, output_name=out_name)

        elif choice == "4":
            video_file = input("Video dosyası: ").strip()
            fmt = input("Hedef video formatı (mp4/avi/mov): ").strip().lower()
            out_name = input("Yeni dosya ismi (boş = orijinal isim): ").strip() or None
            convert_video(video_file, fmt, output_name=out_name)

        elif choice == "5":
            pdf_file = input("PDF dosyası: ").strip()
            out_name = input("Yeni Word dosya ismi (boş = orijinal isim): ").strip() or None
            convert_pdf_to_word(pdf_file, output_name=out_name)

        elif choice == "6":
            word_file = input("Word dosyası (.docx): ").strip()
            out_name = input("Yeni PDF dosya ismi (boş = orijinal isim): ").strip() or None
            convert_word_to_pdf(word_file, output_name=out_name)

        else:
            print("⚠️ Geçersiz seçim!")

    except Exception as e:
        print("❌ Hata:", e)

if __name__ == "__main__":
    main()
