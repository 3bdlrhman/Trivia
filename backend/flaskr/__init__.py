import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_itmes(request, lst):
      page = request.args.get('page', 1, type=int)
      start = (page - 1) * QUESTIONS_PER_PAGE
      end = start + QUESTIONS_PER_PAGE
      paginated_lst = lst[start:end]
      return paginated_lst


def create_app(test_config=None):
    # configure the app
    app = Flask(__name__)
    setup_db(app)


    CORS(app)


    @app.after_request
    def after_request(response):
        response.headers.add('Access_Control_Allow_Headers', 'Content-Type, Authorization, true')
        response.headers.add('Access_Control_Allow_Methods', 'GET, POST, DELETE, PATCH')
        return response


    @app.route('/categories')
    def show_all_categories():
        categories = Category.query.all()
        formated_categories = {category.id: category.type for category in categories}
        return jsonify({
          'success': True,
          'categories': formated_categories
        })


    @app.route('/questions/')
    def show_questins_paginated():
        questions = Question.query.all()
        categories = Category.query.all()
        paginated_questions = paginate_itmes(request, questions)
        formated_questions = [q.format() for q in paginated_questions]
        formated_categories = {category.id: category.type for category in categories}
        if len(questions)==0 or len(categories) ==0:
            abort(404)
        return jsonify({
          'success': True,
          'questions': formated_questions,
          'total_questions': len(formated_questions),
          'categories': formated_categories
        })


    @app.route('/questions/<question_id>', methods=['DELETE'])
    def delete_question_with_id(question_id):
        Q=Question.query.get(question_id)
        if type(Q) is None:
            abort(405)
        try:
            Q.delete()
            return jsonify({
              'success': True,
              'question_id': question_id
            })
        except:
            abort(405)


    @app.route('/questions', methods=['POST'])
    def add_new_question():
        body = request.get_json()
        try:
            question = body.get('question')
            answer = body.get('answer')
            difficulty = body.get('difficulty')
            category = body.get('category')
            Q = Question(question=question, answer=answer,
                        difficulty=difficulty, category=category)
            Q.insert()
            return jsonify({
              'success': True,
              'question': Q.id
            })
        except:
            abort(405)


    @app.route('/search', methods=['POST'])
    def search_for_question():
        body = request.get_json()
        search_term = body.get('searchTerm')
        if not search_term:
              abort(500)
        matched_questions = Question.query.filter(
              Question.question.ilike('%{}%'.format(search_term))).all()
        matched_questions_formated = [question.format() for question in matched_questions]
        return jsonify({
          'success': True,
          'status': 200,
          'questions': matched_questions_formated,
          'total_questions': len(matched_questions)
        })


    @app.route('/categories/<category_id>/questions')
    def list_specific_category_questions(category_id):
        questions_list = Question.query.filter(Question.category == category_id).all()
        if len(questions_list)==0:
              abort(404)
        paginated_list = paginate_itmes(request, questions_list)
        questions_formated = [question.format() for question in paginated_list]
        return jsonify({
          'success': True,
          'status': 200,
          'questions': questions_formated,
          'total_questions': len(questions_formated)
        })


    @app.route('/quizzes', methods=['POST'])
    def play_quiz():
        data = request.get_json()
        previous_questions = data.get('previous_questions')
        quiz_category = data.get('quiz_category')['id']
        if int(quiz_category)==0:
              quiz_category = random.randrange(1,5)
        if not type(quiz_category)==int:
            specific_category_all_questions = Question.query.filter(
              Question.category == quiz_category).all()
        else:
            specific_category_all_questions = Question.query.all()
        if len(specific_category_all_questions)==0:
            abort(404)

        while True:
            random_int = random.randrange(0, len(specific_category_all_questions))
            question = specific_category_all_questions[random_int]
            if question.id not in previous_questions :
                break
            elif len(previous_questions) == len(specific_category_all_questions):
                return jsonify({
                  'success': True
                })

        return jsonify({
          'success': True,
          'question':question.format()
        })


    @app.errorhandler(404)
    def resources_not_found(error):
        return jsonify({
          'success': False,
          'error': 404,
          'message': 'The server can not find the requested resource'
        }), 404
      
    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
          'success': False,
          'error': 405,
          'message': 'The request method is known by the server but not supported.'
        }), 405
      
    @app.errorhandler(422)
    def request_unprocessable(error):
        return jsonify({
          'success': False,
          'error': 422,
          'message': 'The request was unable to be followed due to semantic errors.'
        }), 422
    
    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
          'success': False,
          'error': 500,
          'message': 'The server can not handle this request'
        }), 500
      
    return app
  
