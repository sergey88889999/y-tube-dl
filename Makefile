SRC = main.py
EXECUT_N = y-tube-dl

.PHONY: build install clean

all: build install

build:
	# Создание виртуальной среды
	python3 -m venv myenv
	# Активация виртуальной среды и установка зависимостей
	. myenv/bin/activate && pip install -r requirements.txt
	# Сборка исполняемого файла с помощью PyInstaller
	. myenv/bin/activate && pyinstaller --onefile --add-data "locales:locales" --name $(EXECUT_N) $(SRC)

install:
	# Запускать с правами администратора, например: 
	# sudo make install 	
	#
	# Копирование исполняемого файла в системную директорию
	cp dist/$(EXECUT_N) /usr/local/bin/$(EXECUT_N)
	# Добавление прав на исполнение файла
	chmod +x /usr/local/bin/$(EXECUT_N)

clean:
	# Очистка созданных файлов и директорий
	rm -rf myenv/ dist/ build/ $(EXECUT_N).spec

