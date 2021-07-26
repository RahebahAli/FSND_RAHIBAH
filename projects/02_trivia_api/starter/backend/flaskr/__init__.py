import os
from flask import Flask, request, abort, jsonify

from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
  # Create and configure the app.
  app = Flask(__name__)
  setup_db(app)

  # Set up CORS. Allow '*' for origins.
  cors = CORS(app, resources={r"*": {"origins": "*"}})

  # Use the after_request decorator to set Access-Control-Allow.
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type, Authorization')
    response.headers.add('Access-Control-Allow-Methods',
                         'GET, POST, PATCH, DELETE, OPTIONS')
    return response

  # Pagination
  def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    current_questions = [question.format()
                         for question in selection[start:end]]
    return current_questions

  # Endpoint to display all available categories.
  @app.route('/categories', methods=['GET'])
  def retrieve_categories():
    # GETTING ALL CATEGORY
    categories = Category.query.all()
    list_cat = [category.format() for category in categories]
    categories_dictionary = {}
    for lst in list_cat:
      categories_dictionary[lst['id']] = lst['type']

    # CHECK: IF NOT FOUND ANY CATEGORY ( abort 404 )
    if len(categories) == 0:
      abort(404)
    # VIEW DATA.
    return jsonify({
      'success': True,
      'categories': categories_dictionary})

  # Endpoint for questions: Display list of questions,
  # number of total questions, current category, categories.
  @app.route('/questions', methods=['GET'])
  def retrieve_questions():
    selection = Question.query.order_by(Question.id).all()
    current_questions = paginate_questions(request, selection)
    categories = Category.query.order_by(Category.type).all()
    categories_dictionry = {category.id: category.type
                            for category in categories}
    # CHECK: IF NOT FOUND ANY CATEGORY ( abort 404 )
    if len(current_questions) == 0:
        abort(404)
    # VIEW DATA
    return jsonify({
        'success': True,
        'questions': current_questions,
        'total_questions': len(selection),
        'categories': categories_dictionry,
        'current_category': 'ALL'})

  # Endpoint for delete questions by using a question ID.
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    try:
      question = Question.query.get(question_id)
      if question is None:
        abort(404)
      question.delete()
      return jsonify({
        'success': True,
        'deleted': question_id})
    except:
        abort(422)

  # Endpoint to create a new questions.
  @app.route('/questions', methods=['POST'])
  def new_question():
    body = request.get_json()

    new_question = body.get('question', None)
    new_answer = body.get('answer', None)
    new_category = body.get('category', None)
    new_difficulty = body.get('difficulty', None)

    try:
      question = Question(question=new_question, answer=new_answer,
                          category=new_category, difficulty=new_difficulty)
      question.insert()

      selection = Question.query.order_by(Question.id).all()
      current_questions = paginate_questions(request, selection)

      return jsonify({
        'success': True,
        'created': question.id,
        'questions': current_questions,
        'total_questions': len(selection)})

    except:
        abort(422)

  # Endpoint to get questions based on a search item.
  @app.route('/questions/search', methods=['POST'])
  def question_search():
    body = request.get_json()
    search_item = body.get('searchTerm', None)
    if search_item:
      searchResult = Question.query.filter(Question.question.ilike("%{}%".format(search_item))).all()
      return jsonify({
        'success': True,
        'questions': [question.format()
                      for question in searchResult],
        'total_questions': len(searchResult),
        'current_category': None
        })
    abort(404)

  # Endpoint to get questions based on a category.
  @app.route('/categories/<int:category_id>/questions', methods=['GET'])
  def get_questions_by_category(category_id):
    current_category = Category.query.get(category_id)
    if current_category is None:
      abort(404)
    categories = Category.query.all()
    categories = [category.format() for category in categories]
    questions = Question.query.filter(Question.category == category_id).all()
    current_questions = paginate_questions(request, questions)
    return jsonify({
        'success': True,
        'questions': current_questions,
        'total_questions': len(questions),
        'current_category': current_category.format(),
        'categories': categories
    })

  # Endpoint to play quiz.
  @app.route('/quizzes', methods=['POST'])
  def play_quiz():
    body = request.get_json()
    prev_qs = body.get('previous_questions')
    quiz_category = body.get('quiz_category')

    try:
        request_cat = quiz_category['id']
    except:
        abort(400)

    if request_cat == 0:
        questions = Question.query.all()
    else:
        questions = Question.query.filter(Question.category == str(request_cat)).all()

    f_questions = [question.format() for question in questions]
    question = random.choice(f_questions)

    while len(prev_qs) < len(f_questions):
        if question['id'] not in prev_qs:
          return jsonify({
          'success': True,
          'question': question
        })
        else:
          question = random.choice(f_questions)

    return jsonify({
        'success': True,
        'question': question
    })

  # Endpoint to error handlers for all expected errors.
  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
        'success': False,
        'error': 400,
        'message': "bad request"
    }), 400

  @app.errorhandler(401)
  def unauthorized(error):
    return jsonify({
        'success': False,
        'error': 401,
        'message': "unauthorized"
    }), 401

  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
        'success': False,
        'error': 404,
        'message': "resource not found"
    }), 404

  @app.errorhandler(405)
  def method_not_allowed(error):
    return jsonify({
        'success': False,
        'error': 405,
        'message': "method not allowed"
    }), 405

  @app.errorhandler(406)
  def not_acceptable(error):
    return jsonify({
        'success': False,
        'error': 406,
        'message': "not acceptable"
    }), 406

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
        'success': False,
        'error': 422,
        'message': "unprocessable"
    }), 422
    
  return app
