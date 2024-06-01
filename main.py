
from pytube import YouTube
from pytube.exceptions import RegexMatchError
from tqdm import tqdm 
import time
import gettext
from gettext import gettext as _
import locale
import os

# функция задает формат времени в 00:00:00
def format_time(seconds):       
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return "{:02d}:{:02d}:{:02d}".format(int(hours), int(minutes), int(seconds))

# функция отслеживает прогресс загрузки видео и выводит соответствующую информацию
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

# Определяем текущую локаль
locale.setlocale(locale.LC_ALL, '')
current_locale = locale.getlocale()

if current_locale[0] and current_locale[0].startswith('ru'): 
    lang_dir = 'ru_RU' 
else: 
    lang_dir = 'en_US'

# Путь к каталогу с файлами перевода 
locale_dir = os.path.join(os.path.dirname(__file__), 'locales') 

# Устанавливаем каталог для поиска файлов перевода 
gettext.bindtextdomain('messages', locale_dir) 
# Устанавливаем текущий домен 
gettext.textdomain('messages')

print(_("Linux terminal utility v.0.0.1 - that downloads videos from YouTube using a provided link."))

while True:

    video_url = input(_("Enter YouTube video URL (Press ENTER to exit): "))

    if not video_url:
        break 

    try:

        # Создайте объект YouTube с указанным URL-адресом
        yt = YouTube(video_url, on_progress_callback=progress_func)

        # test кусок кода - доступные параметры загрузки видео просто для справки
        print(_("Available download options:"))
        for stream in yt.streams:
            quality = stream.abr if stream.abr else "None"  # Обработка отсутствующего качества
            print(_("Resolution: %(resolution)s, Format: %(mime_type)s, Type: %(type)s, Quality: %(abr)s") % {
                'resolution': stream.resolution,
                'mime_type': stream.mime_type,
                'type': stream.type,
                'abr': stream.abr
            })
           
        # Получите лучшее качество видео в формате mp4
        video = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()

        # Выводим имя файла перед началом загрузки
                
        print(_("Starting download of file: %(title)s.%(file_extension)s") % {
            'title': video.title,
            'file_extension': video.mime_type.split('/')[-1]
        })

        start_time = time.time()

        # Загрузите видео
        video.download()
        
        print()
        print(_("Video successfully downloaded!"))
    except RegexMatchError:
        print(_("Error: Invalid YouTube video URL."))
    except Exception as e:
        print(_("An error occurred while downloading the video: %(exception_type)s: %(exception_message)s") % {
            'exception_type': type(e).__name__,
            'exception_message': str(e)
        })
    

