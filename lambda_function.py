# -*- coding: utf-8 -*-

# This is a simple Hello World Alexa Skill, built using
# the implementation of handler classes approach in skill builder.
import logging

import random
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_model import Response
from ask_sdk_model.ui import SimpleCard
from controller.login_controller import validate_login
from controller.question_controller import view_question, count_total_question, view_languagetype
from controller.questiontype_controller import view_questiontype, get_questiontype_id
from controller.result_controller import result_calculation

sb = SkillBuilder()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

session_login_id = 'session_login_id'
session_login_username = 'session_login_username'
session_login_role = 'session_login_role'
answer_flag = False
answer = ""
questiontype_id = None
user_question_counter = 0
total_question_counter = 0
question_counter_dict = {}
question_dict_list = []
que_list = []
que_dict = []
que_type_list = []
language_type_list=[]
language_type = ''
question = ''
language_name=''
questiontype_name=''
questiontype_dict_list = 0
correct_answer_count = 0
incorrect_answer_count = 0
db_total_question = 0


class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        speech_text = "Welcome to Interview Conduction Round,Please Enter Username and Password by saying " \
                      "username is and password is "
        reprompt = ("Please login again by saying, username is and password is ")

        handler_input.response_builder.speak(speech_text).ask(reprompt).set_card(
            SimpleCard("Hello World", speech_text)).set_should_end_session(False)
        return handler_input.response_builder.response


class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = "You can say hello to me!"

        handler_input.response_builder.speak(speech_text).ask(speech_text).set_card(
            SimpleCard("Hello World", speech_text))
        return handler_input.response_builder.response


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (
            is_intent_name("AMAZON.CancelIntent")(handler_input) or is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = "Goodbye!"

        handler_input.response_builder.speak(speech_text).set_card(SimpleCard("Hello World", speech_text))
        return handler_input.response_builder.response


class FallbackIntentHandler(AbstractRequestHandler):
    """AMAZON.FallbackIntent is available in these locales.
    This handler will not be triggered except in supported locales,
    so it is safe to deploy on any locale.
    """

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = ("The Hello World skill can't help you with that.  "
                       "You can say hello!!")
        reprompt = "You can say hello!!"
        handler_input.response_builder.speak(speech_text).ask(reprompt)
        return handler_input.response_builder.response


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        return handler_input.response_builder.response


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Catch all exception handler, log exception and
    respond with custom message.
    """

    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speech = "Sorry, there was some problem. Please try again!!"
        handler_input.response_builder.speak(speech).ask(speech)

        return handler_input.response_builder.response


class LoginIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("LoginIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        request_slot = handler_input.request_envelope.request.intent.slots

        request_login_username = request_slot['request_login_username']
        request_login_password = request_slot['request_login_password']

        if request_login_username.value is not None:
            if request_login_password.value is not None:
                login_dict_list = validate_login(request_login_username.value, request_login_password.value)
                if len(login_dict_list) != 0:
                    handler_input.attributes_manager.session_attributes[session_login_id] = login_dict_list[0][
                        'login_id']
                    handler_input.attributes_manager.session_attributes[session_login_username] = login_dict_list[0][
                        'login_username']
                    handler_input.attributes_manager.session_attributes[session_login_role] = login_dict_list[0][
                        'login_role']
                    speech_text = "You are successfully logged in. please say begin the session."
                    reprompt = ("Please say again, begin the session.")
                else:
                    speech_text = "Username or Password is Incorrect!"
                    reprompt = ("Please login again by saying, username is and password is ")
            else:
                speech_text = "Password is not available."
                reprompt = ("Please login again by saying, username is and password is ")
        else:
            speech_text = "Username is not available."
            reprompt = ("Please login again by saying, username is and password is ")

        handler_input.response_builder.speak(speech_text).ask(reprompt).set_card(
            SimpleCard("Hello World", speech_text)).set_should_end_session(False)
        return handler_input.response_builder.response


class QuestiontypeIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("QuestiontypeIntent")(handler_input)

    def handle(self, handler_input):
        global questiontype_dict_list
        global language_type
        global language_type_list
        global que_type_list
        global language_name
        global questiontype_name
        # type: (HandlerInput) -> Response
        request_slot = handler_input.request_envelope.request.intent.slots

        request_language_type = request_slot['request_language_type']
        language_type = request_language_type.value
        if language_type is not None:
            if language_type in language_type_list:
                if session_login_username in handler_input.attributes_manager.session_attributes:
                    session_login_username_value = handler_input.attributes_manager.session_attributes[
                        session_login_username]
                    if session_login_username_value is not None:
                        questiontype_dict_list = view_questiontype()
                        questiontype_name = ""
                        if len(questiontype_dict_list) != 0:
                            for index in questiontype_dict_list:
                                questiontype_name += index['questiontype_name'] + ","
                                que_type_list.append(index['questiontype_name'])
                            speech_text = "The question type format is listed here:" + questiontype_name + "Please choose type by saying question type is " + questiontype_name + " to begin the interview round"
                            reprompt = ("You can tell me your question type by saying, question type is ")
                        else:
                            speech_text = "Interview session will be conducted soon!"
                    else:
                        speech_text = "username not found !"
                else:
                    speech_text = "I don't know your username please logged in again !"
            else:
                speech_text="Invalid Language Type,The language format is listed here:" + language_name + "Please choose type by saying language is " + language_name + " to begin the interview round"
        else:
            speech_text = "Invalid Language Type"
            reprompt = (
                "I'm not sure what your interview language is, You can tell me your interview language by saying, language is  ")
        handler_input.response_builder.speak(speech_text).ask(reprompt).set_card(
            SimpleCard("Hello World", speech_text)).set_should_end_session(False)
        return handler_input.response_builder.response


class LanguagetypeIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("LanguagetypeIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        global language_type_list
        global language_name
        if session_login_username in handler_input.attributes_manager.session_attributes:
            session_login_username_value = handler_input.attributes_manager.session_attributes[session_login_username]
            if session_login_username_value is not None:
                language_list = view_languagetype()
                language_name = ""
                if len(language_list) != 0:
                    for index in language_list:
                        language_name += index + ","
                        language_type_list.append(index)
                    print("Language_name", language_name)
                    speech_text = "The language format is listed here:" + language_name + "Please choose type by saying language is " + language_name + " to begin the interview round"
                    reprompt = ("You can tell me your language by saying, language is ")
                else:
                    speech_text = "Interview session will be conducted soon!"
            else:
                speech_text = "username not found !"
        else:
            speech_text = "I don't know your username please logged in again !"
        handler_input.response_builder.speak(speech_text).ask(reprompt).set_card(
            SimpleCard("Hello World", speech_text)).set_should_end_session(False)
        return handler_input.response_builder.response


class QuestionIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("QuestionIntent")(handler_input)

    def handle(self, handler_input):
        global answer
        global question
        global que_list
        global que_dict
        global questiontype_dict_list
        global questiontype_id
        global user_question_counter
        global question_counter_dict
        global question_dict_list
        global total_question_counter
        global db_total_question
        global correct_answer_count
        global incorrect_answer_count
        global session_login_id
        global language_type
        global que_type_list
        global questiontype_name
        global question_list

        # type: (HandlerInput) -> Response
        db_total_question = count_total_question()
        if session_login_username in handler_input.attributes_manager.session_attributes:
            session_login_username_value = handler_input.attributes_manager.session_attributes[session_login_username]
            if session_login_username_value is not None:
                request_slot = handler_input.request_envelope.request.intent.slots
                request_questiontype_name = request_slot['request_questiontype_name']
                print("request_questiontype_name:", request_questiontype_name)

                if request_questiontype_name.value in que_type_list:
                    que_type_list.remove(request_questiontype_name.value)
                    question_list = ''
                    for i in que_type_list:
                        question_list += i + ","
                if request_questiontype_name.value is not None:
                    question_questiontype_id = get_questiontype_id(request_questiontype_name.value)
                    print("question_questiontype_id=", question_questiontype_id)
                    if user_question_counter == 0:
                        questiontype_id = question_questiontype_id
                        print("language_type:", language_type)
                        question_dict_list = view_question(question_questiontype_id, language_type)
                        if len(question_dict_list) != 0:
                            # question_counter_dict.update({"question_questiontype_id": len(question_dict_list)})
                            for i in range(100):
                                ran_que = random.choice(question_dict_list)
                                if ran_que not in que_dict:
                                    if len(que_dict) < 3:
                                        que_dict.append(ran_que)
                                    else:
                                        break
                            print("que_dict:", que_dict)
                            question = que_dict[user_question_counter]['question_name']
                            answer = que_dict[user_question_counter]['question_answer']
                            user_question_counter += 1
                            total_question_counter += 1
                            speech_text = "question is " + question
                            reprompt = ("you can say repeat question or next question.")
                        else:
                            speech_text = "No Questions Available !"
                else:
                    if total_question_counter == (len(questiontype_dict_list)) * 3:
                        login_id = handler_input.attributes_manager.session_attributes[session_login_id]
                        result = result_calculation(correct_answer_count, incorrect_answer_count,
                                                    total_question_counter,
                                                    login_id, language_type)
                        speech_text = "You have completed your exam. You can check your result on your dashboard. please say goodbye."
                        reprompt = ("please say goodbye.")
                        answer = ""
                        questiontype_id = None
                        user_question_counter = 0
                        total_question_counter = 0
                        question_counter_dict = {}
                        question_dict_list = []
                        que_list = []
                        que_dict = []
                        language_type = ''
                        correct_answer_count = 0
                        incorrect_answer_count = 0
                        db_total_question = 0

                    elif user_question_counter < len(que_dict):
                        question = que_dict[user_question_counter]['question_name']
                        answer = que_dict[user_question_counter]['question_answer']
                        user_question_counter += 1
                        total_question_counter += 1

                        speech_text = "question is " + question
                        reprompt = ("you can say repeat question or next question.")
                    else:
                        que_dict = []
                        user_question_counter = 0
                        speech_text = "You have completed all questions. Please select new question type " + question_list + " by saying question type is"
                        reprompt = (
                            "please select next question type" + question_list + " by saying, question type is ")

            else:
                speech_text = "username not found !"
        else:
            speech_text = "I don't know your username please logged in again !"
        handler_input.response_builder.speak(speech_text).ask(reprompt).set_card(
            SimpleCard("Hello World", speech_text)).set_should_end_session(False)
        return handler_input.response_builder.response


class RepeatQuestionIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("RepeatIntent")(handler_input)

    def handle(self, handler_input):
        global question
        if question is not None:
            speech_text = "question is " + question
        else:
            speech_text = "there is no question."

        # type: (HandlerInput) -> Response


        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Hello World", speech_text)).set_should_end_session(False)
        return handler_input.response_builder.response


class AnswerIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AnswerIntent")(handler_input)

    def handle(self, handler_input):
        global answer
        global question
        global que_list
        global que_dict
        global questiontype_dict_list
        global questiontype_id
        global user_question_counter
        global question_counter_dict
        global question_dict_list
        global total_question_counter
        global db_total_question
        global correct_answer_count
        global incorrect_answer_count
        global session_login_id
        global language_type
        global question_list

        # type: (HandlerInput) -> Response
        request_slot = handler_input.request_envelope.request.intent.slots
        request_question_answer = request_slot['request_question_answer']
        if request_question_answer.value is not None:
            answer_list = answer.split(",")
            print("answer_list:", answer_list)
            if request_question_answer.value in answer_list:
                print("request_question_answer.value", request_question_answer.value)
                correct_answer_count += 1

            else:
                print("Wrong Answer")
                incorrect_answer_count += 1

            if total_question_counter == (len(questiontype_dict_list)) * 3:
                login_id = handler_input.attributes_manager.session_attributes[session_login_id]
                result = result_calculation(correct_answer_count, incorrect_answer_count,
                                            total_question_counter,
                                            login_id, language_type)
                speech_text = "You have completed your exam. You can check your result on your dashboard. please say goodbye."
                reprompt = ("please say goodbye.")
                answer = ""
                questiontype_id = None
                user_question_counter = 0
                total_question_counter = 0
                question_counter_dict = {}
                question_dict_list = []
                que_list = []
                que_dict = []
                language_type = ''
                correct_answer_count = 0
                incorrect_answer_count = 0
                db_total_question = 0

            elif user_question_counter < len(que_dict):
                question = que_dict[user_question_counter]['question_name']
                answer = que_dict[user_question_counter]['question_answer']
                user_question_counter += 1
                total_question_counter += 1

                speech_text = "next question is " + question
                reprompt = ("you can say repeat question or next question.")
            else:
                que_dict = []
                user_question_counter = 0
                speech_text = "You have completed all questions. Please select new question type " + question_list + " by saying question type is"
                reprompt = (
                    "please select next question type" + question_list + " by saying, question type is ")

        else:
            speech_text = "invalid input"
            reprompt = ("please answer the question by saying, answer is ")

        handler_input.response_builder.speak(speech_text).ask(reprompt).set_card(
            SimpleCard("QuestionIntent", speech_text)).set_should_end_session(False)
        return handler_input.response_builder.response


sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_exception_handler(CatchAllExceptionHandler())
sb.add_request_handler(LoginIntentHandler())
sb.add_request_handler(LanguagetypeIntentHandler())
sb.add_request_handler(QuestiontypeIntentHandler())
sb.add_request_handler(QuestionIntentHandler())
sb.add_request_handler(RepeatQuestionIntentHandler())
sb.add_request_handler(AnswerIntentHandler())

handler = sb.lambda_handler()
