# PDF Color Analyzer

Приложение для анализа PDF файлов на предмет наличия цветных страниц. В результате работы каждой страницы PDF анализируются, и пользователю предоставляется информация о том, какие страницы можно печатать в цвете, а какие — в черно-белом режиме.

## Особенности

- Графический интерфейс на основе Tkinter
- Конвертация PDF страниц в изображения с помощью pdf2image
- Анализ изображений с использованием Pillow и NumPy

## Требования

Перед запуском приложения необходимо установить следующие зависимости:

- **Python 3.x**
- **NumPy**
- **Pillow**
- **pdf2image**

> **Важно:** Библиотека `pdf2image` требует установленного пакета **poppler**.  
> **Установка Poppler:**  
> - **Windows:** Скачайте [poppler для Windows](http://blog.alivate.com.au/poppler-windows/) и добавьте путь к папке `bin` в переменную окружения PATH.  
> - **Ubuntu:** Установите poppler через менеджер пакетов:
>   ```bash
>   sudo apt update
>   sudo apt install poppler-utils
>   ```

## Установка

1. Склонируйте репозиторий или загрузите файлы проекта.
2. Установите зависимости с помощью pip:
   `bash
   pip install -r requirements.txt
   `

## Запуск приложения

Запустите приложение командой:

```bash
python app.py 
```


## Cборка приложения

Установка PyInstaller
Если PyInstaller не установлен, выполните:

```bash
pip install pyinstaller
```

## Cборка под Windows

```bash
pyinstaller --onefile --windowed app.py
```

## Cборка под Ubuntu

```bash
pyinstaller --onefile app.py
```