from models import setup_db, Question, Category
import os
from flask import Flask, request, abort, jsonify, make_response, json
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from helpers import paginate_data, format_query_result
from werkzeug.exceptions import HTTPException, InternalServerError
import random


# class APIError(Exception):
#     """All custom API Exceptions"""
#     pass


# class InternalServerError(APIError):
#     """Custom Authentication Error Class."""
#     code = 500
#     description = "Internal Servier Error"


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
    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response

    '''
  @TODO:
  Create an endpoint to handle GET requests
  for all available categories.
  '''
    @app.route('/categories')
    def get_categories():
        categories = Category.query.order_by(Category.id).all()
        rows = {}
        for row in format_query_result(categories):
            rows[row['id']] = row['type']

        return jsonify({
            'success': True,
            'categories': rows,
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
    @app.route('/questions')
    def get_questions():
        try:
            search_term = request.args.get('search_term')
            questions = []
            if search_term:
                questions = Question.query.order_by(Question.id).filter(
                    Question.question.ilike("%{}%".format(search_term))
                ).all()
            else:
                questions = Question.query.order_by(Question.id).all()
            categories = Category.query.order_by(Category.id).all()
            cats = {}
            for row in format_query_result(categories):
                cats[row['id']] = row['type']

            return jsonify({
                'success': True,
                'questions': paginate_data(request, questions),
                'total_questions': len(questions),
                'categories': cats,
                'current_category': 'some value'
            })
        except Exception as e:
            print('error: ', str(e))
            raise InternalServerError(str(e))

    '''
  @TODO:
  Create an endpoint to DELETE question using a question ID.

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page.
  '''
    @app.route("/questions/<int:question_id>", methods=["DELETE"])
    def delete_question(question_id):
        try:
            question = Question.query.filter(
                Question.id == question_id).one_or_none()

            if question is None:
                print("no question found")
                return make_response(jsonify({"error": f"No question matches the id of {question_id}"}), 404)

            question.delete()
            selection = Question.query.order_by(Question.id).all()
            current_questions = paginate_data(request, selection)

            return jsonify(
                {
                    "success": True,
                    "deleted": question_id,
                    "questions": current_questions,
                    "total_questions": len(Question.query.all()),
                }
            )

        except Exception as e:
            print('error: ', str(e))
            raise InternalServerError(str(e))

    '''
  @TODO:
  Create an endpoint to POST a new question,
  which will require the question and answer text,
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab,
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.
  '''
    @app.route("/questions", methods=["POST"])
    def create_question():
        body = request.get_json()

        question = body.get("question", None)
        answer = body.get("answer", None)
        category = body.get("category", None)
        difficulty = body.get("difficulty", None)
        try:
            question = Question(question=question, answer=answer,
                                category=category, difficulty=difficulty)
            question.insert()

            selection = Question.query.order_by(Question.id).all()
            current_questions = paginate_data(request, selection)

            return jsonify(
                {
                    "success": True,
                    "created": question.id,
                    "questions": current_questions,
                    "total_questions": len(Question.query.all()),
                    "current_category": "science"
                }
            )

        except Exception as e:
            print('error: ', str(e))
            raise InternalServerError(str(e))

    '''
  @TODO:
  Create a GET endpoint to get questions based on a search term.
  It should return any questions for whom the search term
  is a substring of the question.

  TEST: Search by any phrase. The questions list will update to include
  only question that include that string within their question.
  Try using the word "title" to start.
  '''

    '''
  @TODO:
  Create a GET endpoint to get questions based on category.

  TEST: In the "List" tab / main screen, clicking on one of the
  categories in the left column will cause only questions of that
  category to be shown.
  '''
    @app.route("/categories/<int:category_id>/questions")
    def get_questions_by_category_id(category_id):
        try:
            selection = Question.query.filter(
                Question.category == str(category_id)).all()

            return jsonify(
                {
                    "success": True,
                    "questions": paginate_data(request, selection),
                    "total_questions": len(selection),
                }
            )

        except Exception as e:
            print('error: ', str(e))
            raise InternalServerError(str(e))

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

    '''
  @TODO:
  Create error handlers for all expected errors
  including 404 and 422.
  '''
    @app.errorhandler(InternalServerError)
    def handle_exception(e):
        """Return JSON instead of HTML for HTTP errors."""
        # start with the correct headers and status code from the error
        response = e.get_response()
        # replace the body with JSON
        response.data = json.dumps({
            "code": e.code,
            "name": e.name,
            "description": e.description,
        })
        response.content_type = "application/json"
        return response

    return app
