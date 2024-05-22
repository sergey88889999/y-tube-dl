
from pytube import YouTube
from pytube.exceptions import RegexMatchError
from tqdm import tqdm 
import time

def format_time(seconds):
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return "{:02d}:{:02d}:{:02d}".format(int(hours), int(minutes), int(seconds))

def progress_func(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage = (bytes_downloaded / total_size) * 100

    # Оценка времени загрузки
    elapsed_time = time.time() - start_time
    download_speed = bytes_downloaded / elapsed_time
    
    # Оценка оставшегося времени
    remaining_bytes = total_size - bytes_downloaded
    remaining_time = remaining_bytes / download_speed
    
    formatted_elapsed_time = format_time(elapsed_time)
    formatted_remaining_time = format_time(remaining_time)

    # Очистка предыдущего вывода
    print('\r' + ' ' * 100 + '\r', end='')

   # Вывод новой информации
    print(f"\rЗагружено: {percentage:.2f}% | Оставшееся время: {formatted_remaining_time} (время загрузки: {formatted_elapsed_time})", end='', flush=True) 

while True:

    video_url = input("Введите URL-адрес YouTube-видео (ENTER для выхода): ")

    if not video_url:
        break 

    try:

        # Создайте объект YouTube с указанным URL-адресом
        yt = YouTube(video_url, on_progress_callback=progress_func)

        # test - доступные параметры загрузки видео просто для справк
        print("Доступные параметры загрузки:")
        for stream in yt.streams:
            print(f"Разрешение: {stream.resolution}, Формат: {stream.mime_type}, Тип: {stream.type}, Качество: {stream.abr}")


        # Получите лучшее качество видео в формате mp4
        video = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()

        # Выводим имя файла перед началом загрузки
        print(f"Начинается загрузка файла: {video.title}.{video.mime_type.split('/')[-1]}")

        # Запомните время начала загрузки
        start_time = time.time()

        # Загрузите видео
        video.download()

        print("\nВидео успешно загружено!")
    except RegexMatchError:
        print("Ошибка: Некорректный URL-адрес YouTube-видео.")
    except Exception as e:
        print(f"Произошла ошибка при загрузке видео: {type(e).__name__}: {str(e)}")

