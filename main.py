import os
from docx2pdf import convert
import fitz  # PyMuPDF

def convert_docx_to_pdf(docx_path, pdf_path):
    """Конвертирует Word-документ в PDF-файл"""
    convert(docx_path, pdf_path)

def is_color(rgb):
    """Проверяет, является ли цвет отличным от черного и оттенков серого."""
    if rgb is None:
        return False  # Нет информации о цвете
    r, g, b = rgb
    return not (r == g == b)  # Оттенки серого имеют равные значения RGB

def page_has_color_text(page):
    """Проверяет, есть ли на странице цветной текст."""
    text_instances = page.get_text("dict")["blocks"]
    for block in text_instances:
        for line in block.get("lines", []):
            for span in line.get("spans", []):
                rgb = span.get("color")
                if is_color(rgb):
                    return True
    return False

def page_has_color_images(page, doc):
    """Проверяет, есть ли на странице цветные изображения."""
    image_list = page.get_images(full=True)
    for img in image_list:
        xref = img[0]
        pix = fitz.Pixmap(doc, xref)
        if pix.n >= 3:  # n >= 3 означает наличие цвета (n=4 для CMYK, n=3 для RGB)
            return True
    return False

def page_has_color_content(page, doc):
    """Проверяет, есть ли на странице цветной контент (текст или изображения)."""
    return page_has_color_text(page) or page_has_color_images(page, doc)

def get_color_pages(pdf_path):
    """Возвращает список номеров страниц с цветным контентом."""
    doc = fitz.open(pdf_path)
    color_pages = []
    for page_number in range(len(doc)):
        page = doc[page_number]
        if page_has_color_content(page, doc):
            color_pages.append(page_number + 1)  # Нумерация страниц начинается с 0
    doc.close()
    return color_pages

def find_color_pages(docx_path):
    """Основная функция для нахождения цветных страниц в Word-документе."""
    pdf_path = 'temp_output.pdf'
    # Конвертация в PDF
    convert_docx_to_pdf(docx_path, pdf_path)
    # Поиск цветных страниц
    color_pages = get_color_pages(pdf_path)
    # Удаление временного PDF-файла
    os.remove(pdf_path)
    return color_pages

# Пример использования
if __name__ == "__main__":
    docx_file = 'test.docx'  # Замените на путь к вашему файлу
    pages_with_color = find_color_pages(docx_file)
    if pages_with_color:
        print("Страницы с цветным контентом:", pages_with_color)
    else:
        print("В документе нет страниц с цветным контентом.")
