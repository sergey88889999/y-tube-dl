
from pytube import YouTube
from pytube.exceptions import RegexMatchError
from tqdm import tqdm 
import time
import gettext
from gettext import gettext as _
import locale
import os
import argparse

# функция задает формат времени в 00:00:00
# The function sets the time format to 00:00:00
def format_time(seconds):       
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return "{:02d}:{:02d}:{:02d}".format(int(hours), int(minutes), int(seconds))

# функция отслеживает прогресс загрузки видео и выводит соответствующую информацию
# The function tracks the progress of video uploading and outputs relevant information
def progress_func(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage = (bytes_downloaded / total_size) * 100

    # Оценка времени загрузки
    # Estimated upload time
    
    elapsed_time = time.time() - start_time
    download_speed = bytes_downloaded / elapsed_time
    
    # Оценка оставшегося времени
    # Estimated remaining time
    
    remaining_bytes = total_size - bytes_downloaded
    remaining_time = remaining_bytes / download_speed
    
    formatted_elapsed_time = format_time(elapsed_time)
    formatted_remaining_time = format_time(remaining_time)

    # Очистка предыдущего вывода
    # Clearing previous output
    print('\r\033[K', end='', flush=True)

    # Вывод статистики загрузки файла
    # Outputting file upload statistics
    print(_("Uploaded: %(percentage).2f%% | Remaining Time: %(formatted_remaining_time)s (upload time: %(formatted_elapsed_time)s)") % {
        'percentage': percentage,
        'formatted_remaining_time': formatted_remaining_time,
        'formatted_elapsed_time': formatted_elapsed_time
        }, end='', flush=True)

# функция опеределения и смену локали по основании системных настроек, по умолчанию английский язык   
# Function to determine and change the locale based on system settings, defaulting to English
def set_locale():
    try:
        locale.setlocale(locale.LC_ALL, '')
    except locale.Error:
        print("Error while setting locale")
      
    current_locale = locale.getlocale()
    if current_locale[0] and current_locale[0].startswith('ru'): 
        language = 'ru_RU'
    else: 
        language = 'en_US'
    
    locale_dir = os.path.join(os.path.dirname(__file__), 'locales')
    gettext.bindtextdomain('messages', locale_dir)
    gettext.textdomain('messages')
    gettext.translation('messages', localedir=locale_dir, languages=[language], fallback=True).install()

# Функция загрузки видео по умолчанию без доп. параметров, с отображанием возможных вариантов качества
# A function for video loading by default without additional parameters, displaying possible quality options
def download_video(video_url):
    
    # Объявляем start_time как глобальную переменную
    # We declare start_time as a global variable.
    global start_time  
    start_time = time.time()
    try:
        # Создайте объект YouTube с указанным URL-адресом
        yt = YouTube(video_url, on_progress_callback=progress_func)
        # Получите лучшее качество видео в формате mp4
        video = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()

        # Выводим имя файла перед началом загрузки
        print(_("Starting download of file: %(title)s.%(file_extension)s") % {
            'title': video.title,
            'file_extension': video.mime_type.split('/')[-1]
        })

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

def interactive():
    while True:
        video_url = input(_("Enter YouTube video URL (Press ENTER to exit): "))   
        if video_url:
            download_video(video_url)
        else:
            break    
        
def main():
    
    set_locale()
    
    print(_("Linux terminal utility v.0.0.1 - that downloads videos from YouTube using a provided link."))
        
    # Создание парсера аргументов командной строки
    # Creating a command-line argument parser.
    # parser = argparse.ArgumentParser(description='Description of command-line parameters.')
    class CustomHelpFormatter(argparse.HelpFormatter):
        def add_usage(self, usage, actions, groups, prefix=None):
            if prefix is None:
                prefix = _('usage: ')
            return super().add_usage(usage, actions, groups, prefix)

        def start_section(self, heading):
            heading = _(heading)
            super().start_section(heading)

        def add_argument(self, action):
            action.help = _(action.help)
            super().add_argument(action)

    parser = argparse.ArgumentParser(prog='y-tube-dl',formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('--URL', type=str, default=None, help=_('URL - link to the YouTube video'))
    args = parser.parse_args()
    if args.URL:
        download_video(args.URL)
    else:
        print(_("usage: y-tube-dl [-h] [--URL URL]; by default, it starts in interactive mode with limited functionality."))
        interactive()
        
    
if __name__ == "__main__":
    main()
    
