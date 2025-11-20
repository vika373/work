import os
import sqlite3
from dotenv import load_dotenv
import google.generativeai as genai

# Загрузка API-ключа из .env
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# --- Работа с базой данных ---
def initialize_db():
    conn = sqlite3.connect("books.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            category TEXT NOT NULL,
            content TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def add_book(title, category, file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        conn = sqlite3.connect("books.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO books (title, category, content) VALUES (?, ?, ?)",
                       (title, category, content))
        conn.commit()
        conn.close()
        print(f"Книга '{title}' добавлена в категорию '{category}'.")
    except Exception as e:
        print(f"Ошибка при добавлении книги: {e}")

def list_categories():
    conn = sqlite3.connect("books.db")
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT category FROM books")
    categories = [row[0] for row in cursor.fetchall()]
    conn.close()
    return categories

def list_books_by_category(category):
    conn = sqlite3.connect("books.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, title FROM books WHERE category = ?", (category,))
    books = cursor.fetchall()
    conn.close()
    return books

def get_book_text(book_id):
    conn = sqlite3.connect("books.db")
    cursor = conn.cursor()
    cursor.execute("SELECT content FROM books WHERE id = ?", (book_id,))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else None

# --- Взаимодействие с Gemini ---
def ask_question(book_text, question):
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
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

# --- Главный интерфейс ---
def main():
    initialize_db()

    while True:
        print("\nМеню:")
        print("1. Добавить книгу")
        print("2. Задать вопрос по книге")
        print("3. Выйти")

        choice = input("Выберите опцию: ")

        if choice == '1':
            title = input("Название книги: ")
            category = input("Категория: ")
            file_path = input("Путь к файлу книги: ")
            add_book(title, category, file_path)

        elif choice == '2':
            categories = list_categories()
            if not categories:
                print("Нет доступных категорий.")
                continue

            print("\nДоступные категории:")
            for i, cat in enumerate(categories, start=1):
                print(f"{i}. {cat}")

            cat_choice = input("Выберите категорию по номеру: ")
            try:
                selected_category = categories[int(cat_choice) - 1]
            except:
                print("Неверный выбор категории.")
                continue

            books = list_books_by_category(selected_category)
            if not books:
                print("Нет книг в этой категории.")
                continue

            print("\nДоступные книги:")
            for id, title in books:
                print(f"{id}. {title}")

            book_id = input("Введите ID книги: ")
            book_text = get_book_text(book_id)

            if not book_text:
                print("Книга не найдена.")
                continue

            print(f"\nВы выбрали книгу. Теперь вы можете задавать вопросы.\n")

            while True:
                question = input("Вопрос (или 'назад'): ")
                if question.lower() == 'назад':
                    break

                print("Обрабатываю запрос...")
                answer = ask_question(book_text, question)

                if answer:
                    print(f"\nОтвет: {answer}")
                else:
                    print("Не удалось получить ответ.")

        elif choice == '3':
            print("Выход из программы.")
            break
        else:
            print("Неверный выбор.")

if __name__ == "__main__":
    main()