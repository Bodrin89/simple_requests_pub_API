
from flask import Flask, request, jsonify
import requests
from config import Config, db
from dotenv import load_dotenv, find_dotenv

from models import Question, QuestionSchema

app = Flask(__name__)

load_dotenv(find_dotenv())

app.config.from_object(Config)
db.init_app(app)

with app.app_context():
    db.create_all()


@app.route('/questions/', methods=['POST'])
def get_questions():
    """Получение вопросов"""

    data = request.get_json()
    questions_num = data.get('questions_num', 0)

    if not isinstance(questions_num, int):
        return jsonify({'error': 'Не правильный тип данных'}), 400

    if questions_num < 0:
        return jsonify({'error': 'Число должно быть положительным'}), 400

    # Запрос к публичному API для получения вопросов
    api_url = f"https://jservice.io/api/random?count={questions_num}"
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        for item in data:
            # Проверка на уникальность вопроса в базе данных
            existing_question = Question.query.filter_by(text_question=item['question']).first()
            while existing_question:
                questions_num = 1
                response = requests.get(api_url)
                if response.status_code == 200:
                    item = response.json()[0]
                    existing_question = Question.query.filter_by(text_question=item['question']).first()
            # Сохранение вопроса в базе данных
            result = Question(
                text_question=item['question'],
                text_answer=item['answer'],
                data_question=item['created_at']
            )
            db.session.add(result)
        db.session.commit()
        try:
            latest_question = Question.query.order_by(Question.id.desc()).limit(2)[1]
            resp_question = QuestionSchema()
            return resp_question.dump(latest_question)
        except:
            return {}
    else:
        return jsonify(error='Не правильный запрос'), 500


if __name__ == '__main__':
    app.run()
