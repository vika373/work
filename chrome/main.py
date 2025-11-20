import os
from dotenv import load_dotenv
import google.generativeai as genai

# Загрузка API-ключа из файла .env
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")  # Измените название переменной в .env файле
genai.configure(api_key=api_key)

def read_book(file_path):
    """
    Читает текст книги из указанного файла.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print("Файл не найден. Проверьте путь к файлу.")
        return None

def ask_question(book_text, question):
    """
    Отправляет текст книги и вопрос к модели Gemini для получения ответа.
    """
    try:
        # Создаем модель
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Формируем промпт
        prompt = f"""Ты помощник, который отвечает на вопросы по тексту книги.

Текст книги:
{book_text}

Вопрос: {question}

Пожалуйста, ответь на вопрос, основываясь только на содержании предоставленной книги."""

        response = model.generate_content(prompt)
        return response.text
        
    except Exception as e:
        print(f"Ошибка при запросе к API: {e}")
        return None

def main():
    # Укажите путь к файлу с книгой
    book_path = "book.txt"  # Замените на путь к вашей книге
    book_text = read_book(book_path)

    if book_text:
        print("Книга успешно загружена!")
        print("Модель Gemini готова к работе!")
        
        while True:
            question = input("\nВведите ваш вопрос (или 'выход' для завершения): ")
            if question.lower() == 'выход':
                break
                
            print("Обрабатываю запрос...")
            answer = ask_question(book_text, question)
            
            if answer:
                print(f"\nОтвет: {answer}")
            else:
                print("Не удалось получить ответ. Попробуйте еще раз.")

if __name__ == "__main__":
    main()