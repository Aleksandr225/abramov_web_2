import random
from flask import Flask, render_template # render_template - функция для рендеринга HTML-шаблонов
from faker import Faker

fake = Faker()

# Создаем приложение для того чтобы управлять маршрутами, обработками запросво и тд.
app = Flask(__name__)
application = app

# Уникальные идентификаторы изображений
images_ids = ['7d4e9175-95ea-4c5f-8be5-92a6b708bb3c',
              '2d2ab7df-cdbc-48a8-a936-35bba702def5',
              '6e12f3de-d5fd-4ebb-855b-8cbc485278b7',
              'afc2cfe7-5cac-4b80-9b9a-d5c65ef0c728',
              'cab5b7f2-774e-4884-a200-0c0180fa777f']

# Генерация комментариев
def generate_comments(replies=True): # Replies - флаг для генерации ответов на комментарии
    comments = []
    for i in range(random.randint(1, 3)): # Количество комментариев
        comment = { 'author': fake.name(), 'text': fake.text() } # Генерация имени и текста автора
        if replies: # Если будет вложенный комментарий
            comment['replies'] = generate_comments(replies=False) 
        comments.append(comment)
    return comments

# Генерация постов
def generate_post(i):
    return {
        'title': fake.sentence(nb_words=7),
        'text': fake.paragraph(nb_sentences=100),
        'author': fake.name(),
        'date': fake.date_time_between(start_date='-2y', end_date='now'),
        'image_id': f'{images_ids[i]}.jpg',
        'comments': generate_comments()
    }

# Создаем список постов и сортируем их по дате от новым к старым
posts_list = sorted([generate_post(i) for i in range(5)], key=lambda p: p['date'], reverse=True)

# Используем маршруты для обработки запросов с помощью декоратора @app.route они связывают URL-адреса с функциями он поддерживает как статические машруты так и динамические.
# Пример работы такой что пользователь переходит по адресу flask вызывает функцию и функция возвращает шаблон с данными этого поста.
@app.route('/') # Главная страница
def index():
    return render_template('index.html')

@app.route('/posts') # Страница со списком постов
def posts():
    return render_template('posts.html', title='Посты', posts=posts_list)

@app.route('/posts/<int:index>') # Страница с конкретным постом
def post(index):
    p = posts_list[index]
    return render_template('post.html', title=p['title'], post=p)

@app.route('/about') # Страница "Об авторе"
def about():
    return render_template('about.html', title='Об авторе')


# Запуск сервера
if __name__ == '__main__':
    app.run(debug=True)