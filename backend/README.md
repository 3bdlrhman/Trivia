# Full Stack Trivia API Backend

## Getting Started
- Base URL => since this application is not hosted and runs locally 
  it runs at http://localhost:5000/ which is configured as a proxy 
  at the frontend section

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server on macOS, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

To run the server on Windows, execute:

```bash
set FLASK_APP=flaskr
set FLASK_ENV=development
flask run
```


Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 
3. Create an endpoint to handle GET requests for all available categories. 
4. Create an endpoint to DELETE question using a question ID. 
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
6. Create a POST endpoint to get questions based on category. 
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
9. Create error handlers for all expected errors including 400, 404, 422 and 500. 


## Endpoints:
--------------
- GET '/categories'
- GET '/questions'
- POST '/questions'
- DELETE '/questions/id'
- POST '/search'
- POST '/quizzes'

-------------------------------------------------------------------------------------
## GET '/categories'
================
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 

- Sample Request =>  curl http://localhost:5000/categories/

- Sample Response =>    {
                        '1' : "Science",
                        '2' : "Art",
                        '3' : "Geography",
                        '4' : "History",
                        '5' : "Entertainment",
                        '6' : "Sports"
                        }

-------------------------------------------------------------------------------------
## GET '/questions'
===============
- This Endpoint should return json object contains 
(request success state, list of questions (10) , number of questions returned, list of categories).
in form of key:value pair

- Sample Request =>  curl http://localhost:5000/questions/

- Sample Response =>    {
                        'success': True,
                        'questions': List_of_questions,
                        'total_questions': 10,
                        'categories': List_of_categories
                        }

-------------------------------------------------------------------------------------
## POST '/questions'
===============
- This endpoint insert a question into the database

- Arguments => (in order to success) Request Body should contain json object similar to the following:
{
'question' : 'What is our distance from the moon',
'answer' : '4,0000 miles',
'category' : 'science',
'difficulty' : 4
}


- Sample Request =>  curl http://localhost:5000/questions -X POST -H "Content-Type: application/json" -d '{
                                                            'question' : 'What is our distance from the moon',
                                                            'answer' : '4,0000 miles',
                                                            'category' : 'science',
                                                            'difficulty' : 4
                                                            }'

- Sample Response => in the other hand (if succeeded) the returned json object contains
  success state, and posted question id both in form of key:value pair

  {
      'success': True,
      'question': 14
  }
 
-------------------------------------------------------------------------------------
## DELETE '/questions/{question_id}'
=====================
- Deletes the book of the given ID if it exists. 
- Returns the id of the deleted book, success value.

- Sample Request => curl -X DELETE http://localhost:5000/questions/{question_id}

- Sample Response => {
                       'success': True,
                       'question_id': 16
                     }


-------------------------------------------------------------------------------------
## POST '/search'
===============
- This endpoint searches for a word in the database and returns list of questions 
  which contains this word. 

- Arguments => (in order to success) Request Body should contain json object similar to the following:
{
'searchTerm' : 'soccer'
}


- Sample Request =>  curl http://localhost:5000/questions -X POST 
                     -H "Content-Type: application/json" -d '{'searchTerm' : 'history'}'

- Sample Response => in the other hand (if succeeded) the returned json object contains
  success state, list of questions conatins this word, and number of the questions

  {
      'success': True,
      'questions': []
      'num_of_question': 14
  }

-------------------------------------------------------------------------------------
## POST '/quizzes'
===============
- Also you can Play the quiz using /quizzes endpoint after choosing a category 
  you will be asked number of questions and finally see your score. 

- Arguments => (in order to success) Request Body should contain json object similar to the following:
{
'previous_questions' : [list_of_previous_questions],
'quiz_category': {'category_id': 'category_name'}
}

- Sample Response => in the other hand (if succeeded) the returned json object contains
  1- success state. 
  2- Random question according to specified category.

  {
      'success': True,
      'questions': {'question': '', 'answer': '', 'category': '', 'difficulty': ''}
  }

------------------------------------------------------------------------------------------

## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
