import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import os
from pdf2image import convert_from_path
from PIL import Image
import numpy as np

# Порог, определяющий чувствительность к цвету (можно настроить)
COLOR_THRESHOLD = 0  # если находим хоть один пиксель, где каналы различаются, считаем страницу цветной

def is_page_color(image):
    """
    Проверяет, является ли изображение цветным.
    Для ускорения изменим размер изображения до 100x100 пикселей.
    """
    small_img = image.resize((100, 100))
    img_array = np.array(small_img)
    # Если изображение уже в режиме L (оттенки серого), то это Ч/Б.
    if small_img.mode == "L":
        return False
    # Если изображение в режиме RGB, проверим, есть ли разница между каналами.
    if small_img.mode == "RGB":
        # Вычисляем разницу между каналами R и G, а также между R и B.
        r, g, b = img_array[:,:,0], img_array[:,:,1], img_array[:,:,2]
        # Находим количество пикселей, где каналы не равны
        diff_rg = np.count_nonzero(r - g)
        diff_rb = np.count_nonzero(r - b)
        if diff_rg > COLOR_THRESHOLD or diff_rb > COLOR_THRESHOLD:
            return True
    return False

class PDFColorAnalyzer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Анализатор PDF страниц")
        self.geometry("600x500")
        
        self.pdf_path = None
        
        # Кнопка для выбора PDF файла
        self.select_button = tk.Button(self, text="Выбрать PDF файл", command=self.select_pdf)
        self.select_button.pack(pady=10)
        
        # Кнопка для анализа выбранного файла
        self.analyze_button = tk.Button(self, text="Анализировать PDF", command=self.analyze_pdf, state=tk.DISABLED)
        self.analyze_button.pack(pady=10)
        
        # Текстовое поле для вывода результатов
        self.result_text = scrolledtext.ScrolledText(self, wrap=tk.WORD, width=70, height=20)
        self.result_text.pack(padx=10, pady=10)
    
    def select_pdf(self):
        file_path = filedialog.askopenfilename(
            title="Выберите PDF файл",
            filetypes=[("PDF Files", "*.pdf")]
        )
        if file_path:
            self.pdf_path = file_path
            self.result_text.insert(tk.END, f"Выбран файл: {os.path.basename(file_path)}\n")
            self.analyze_button.config(state=tk.NORMAL)
    
    def analyze_pdf(self):
        if not self.pdf_path:
            messagebox.showwarning("Предупреждение", "Сначала выберите PDF файл.")
            return
        
        self.result_text.insert(tk.END, "Начинаем анализ PDF...\n")
        try:
            # Конвертируем PDF в изображения (каждая страница = изображение)
            pages = convert_from_path(self.pdf_path)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось конвертировать PDF: {e}")
            return
        
        color_pages = []
        bw_pages = []
        
        for i, page in enumerate(pages, start=1):
            self.result_text.insert(tk.END, f"Анализ страницы {i}...\n")
            if is_page_color(page):
                color_pages.append(i)
            else:
                bw_pages.append(i)
            self.update()  # Обновление интерфейса
        
        self.result_text.insert(tk.END, "\nРезультаты анализа:\n")
        self.result_text.insert(tk.END, f"Страницы для цветной печати: {color_pages}\n")
        self.result_text.insert(tk.END, f"Страницы для Ч/Б печати: {bw_pages}\n")
        self.result_text.insert(tk.END, "Анализ завершён.\n")
        
if __name__ == "__main__":
    app = PDFColorAnalyzer()
    app.mainloop()
