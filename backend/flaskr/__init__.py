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
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  CORS(app)
  
  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
        response.headers.add('Access_Control_Allow_Headers', 'Content-Type, Authorization, true')
        response.headers.add('Access_Control_Allow_Methods', 'GET, POST, DELETE, PATCH')
        return response

  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories')
  def show_all_categories():
        categories = Category.query.all()
        formated_categories = {category.id: category.type for category in categories}
        return jsonify({
          'success': True,
          'categories': formated_categories
        })

  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
   '''
  @app.route('/questions/')
  def show_questins_paginated():
        questions = Question.query.all()
        categories = Category.query.all()
        paginated_questions = paginate_itmes(request, questions)
        formated_questions = [q.format() for q in paginated_questions]
        formated_categories = {category.id: category.type for category in categories}
        return jsonify({
          'success': True,
          'questions': formated_questions,
          'total_questions': len(formated_questions),
          'categories': formated_categories
        })


  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<question_id>', methods=['DELETE'])
  def delete_question_with_id(question_id):
        Q=Question.query.get(question_id)
        if type(Q) is None:
              abort(405) # when the question does not exist
        try:
          Q.delete()
          return jsonify({
            'success': True,
            'question_id': question_id
          })
        except:
          abort(405)

  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''

  @app.route('/questions', methods=['POST'])
  def add_new_question():
        body = request.get_json()
        if not body['question']:
            abort(500) 
            
        question = body.get('question')
        answer = body.get('answer')
        difficulty = body.get('difficulty')
        category = body.get('category')
        
        Q = Question(question, answer, difficulty, int(category))
        
        try:
          Q.insert()
          return jsonify({
            'success': True,
            'question': Q.id
          })
        except:
          abort(405) # method not allowed

  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  @app.route('/search', methods=['POST'])
  def search_for_question():
        body = request.get_json()
        search_term = body.get('searchTerm')
        if not search_term:
              abort(500)
        matched_questions = Question.query.filter(Question.question.ilike('%{}%'.format(search_term))).all()
        matched_questions_formated = [question.format() for question in matched_questions]
        
        return jsonify({
          'success': True,
          'status': 200,
          'questions': matched_questions_formated,
          'total_questions': len(matched_questions)
        })

  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<category_id>/questions')
  def list_specific_category_questions(category_id):
        questions_list = Question.query.filter(Question.category == category_id).all()
        paginated_list = paginate_itmes(request, questions_list)
        questions_formated = [question.format() for question in paginated_list]
        return jsonify({
          'success': True,
          'status': 200,
          'questions': questions_formated,
          'total_questions': len(questions_formated)
        })

  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  @app.route('/quizzes', methods=['POST'])
  def play_quiz():
        data = request.get_json()
        previous_questions = data.get('previous_questions')
        quiz_category = data.get('quiz_category')['id']
        
        if int(quiz_category)==0:
              quiz_category = random.randrange(1,5)
        # check if there is a category specified
        if not type(quiz_category)==int:
              specific_category_all_questions = Question.query.filter(Question.category == quiz_category).all()
        else: # if no category specified 'All'
              specific_category_all_questions = Question.query.filter(Question.category == random.randint(0,5)).all()
                
        if len(specific_category_all_questions)==0:
              abort(404)
              
        while True:
              random_int = random.randrange(0, len(specific_category_all_questions))
              question = specific_category_all_questions[random_int]
              if question.id not in previous_questions :
                    break
              elif len(previous_questions) == len(specific_category_all_questions):
                    abort(404)
        
        return jsonify({
          'question':question.format()
        })
          

  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
    
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
      'message': 'the request method is known by the server but is not supported by the target resource.'
    }), 405
    
  @app.errorhandler(422)
  def request_unprocessable(error):
    return jsonify({
      'success': False,
      'error': 422,
      'message': 'The request was well-formed but was unable to be followed due to semantic errors.'
    }), 422
  
  @app.errorhandler(500)
  def internal_server_error(error):
    return jsonify({
      'success': False,
      'error': 500,
      'message': 'The server can not handle this request'
    }), 500
    
  return app