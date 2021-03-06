from django.shortcuts import render, get_object_or_404, redirect
from model.models import Model, Option
from services.graph import get_graph_snod
from services.history import checking_already_has_answer
from services.model import get_model_data
from services.pairs_of_options import (absolute_value_in_str,
                                       data_of_winners, make_question,
                                       write_answer)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View

from services.settings import settingsOrigianlSnodCreate
from .models import HistoryAnswer, PairsOfOptions
from services.snod_original import get_original_snod_question, write_original_snod_answer, \
    get_winners_from_model_original_snod, get_context_history_answer_original_snod
from Verbal_Decision_Analysis.settings import MEDIA_ROOT
import os
import random


class SnodSearchView(LoginRequiredMixin, View):
    login_url = 'login'

    @staticmethod
    def get(request, id):
        model = Model.objects.get(id=id)
        message = make_question(model)
        return render(request, "snod/question.html",
                      {'message': message,
                       'model': model, 'origianl_snod': 0})

    @staticmethod
    def post(request, id):

        answer = request.POST["answer"]
        message = write_answer(request, answer)

        """Проверяем, что нашли лучшую альтернативу в модели"""
        flag_find_winner = message['flag_find_winner']
        if flag_find_winner == 0:
            model = Model.objects.get(id=id)
            return render(request, "snod/question.html",
                          {'message': message,
                           'model': model, 'origianl_snod': 0})
        else:
            return render(request, "snod/result.html",
                          {})


class SnodDetailView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request, id):
        model = Model.objects.get(id=id)
        option_shnur = Option.objects.get(id=model.id_winner_option_shnur)
        option_many = Option.objects.get(id=model.id_winner_option_many)

        """ История ответов """
        history_answers = HistoryAnswer.objects.filter(id_model=model)
        answers = []
        for answer_history in history_answers:
            answers.append({'question': answer_history.question, 'answer': answer_history.answer,
                            'pair': answer_history.pair.id_option_1.name + ' и ' + answer_history.pair.id_option_2.name})

        pairs = PairsOfOptions.objects.filter(id_model=id)
        img = []

        for pair in pairs:
            absolute_value = absolute_value_in_str(model.id, pair.id)
            if 'DATABASE_URL' in os.environ:
                img.append({'pair': pair.id_option_1.name + ' и ' + pair.id_option_2.name,
                            'path': MEDIA_ROOT + str(model.id) + '/' + str(pair.id) + '.png',
                            'absolute_value': absolute_value})

            else:
                img.append({'pair': pair.id_option_1.name + ' и ' + pair.id_option_2.name,
                            'path': 'http://127.0.0.1:8000/media/' + str(model.id) + '/' + str(pair.id) + '.png',
                            'absolute_value': absolute_value})

        model_data, model_header = get_model_data(model.id)
        winners_data, winners_header = data_of_winners(model.id)

        response = {'option_shnur': option_shnur.name, 'option_many': option_many.name, 'history': answers, 'img': img,
                    'time_shnur_elapsed': model.time_shnur, 'time_answer_elapsed': model.time_answer_shnur,
                    'time_many_elapsed': model.time_many, 'model_data': model_data, 'model_header': model_header,
                    'winners_data': winners_data, 'winners_header': winners_header}

        return render(request, "snod/result.html",
                      response)


class SettingsOriginalSnodCreateView(LoginRequiredMixin, View):
    login_url = 'login'

    @staticmethod
    def get(request, id):
        context = {'model': get_object_or_404(Model, id=id), 'mode': ['Классический', 'Автоматический']}
        return render(request, "snod/settings_original_snod.html", context)

    def post(self, request, id, **kwargs):
        settings = settingsOrigianlSnodCreate(request)
        Model.objects.filter(id=id).update(id_settings_original_snod=settings)
        return redirect('snod_original_search', id=id)


class OriginalSnodSearchView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request, id):
        model = Model.objects.get(id=id)

        if model.id_settings_original_snod is None:
            return redirect('snod_original_settings_create', id=id)

        if model.id_settings_original_snod.auto_mode is True:
            return self.post(request, id)

        message = get_original_snod_question(model)
        return render(request, "snod/question.html",
                      {'message': message,
                       'model': model, 'original_snod': 1})

    def post(self, request, id):
        model = Model.objects.get(id=id)

        flag_find_winner = 0
        message = get_original_snod_question(model)

        while flag_find_winner == 0 and model.id_settings_original_snod.auto_mode is True:
            answer: int = random.randint(0, 2)
            message = write_original_snod_answer(request, answer, auto=True,
                                       message=message)
            flag_find_winner = message['flag_find_winner']
            if flag_find_winner != 1:

                message, flag_checking = checking_already_has_answer(request, message, snod_original=True)
                while flag_checking:
                    flag_find_winner = message['flag_find_winner']
                    if flag_find_winner != 1:
                        message, flag_checking = checking_already_has_answer(request, message, snod_original=True)

        if model.id_settings_original_snod.auto_mode is False:
            answer = request.POST["answer"]
            message = write_original_snod_answer(request, answer, auto=False)

        """Проверяем, что нашли лучшую альтернативу в модели"""
        flag_find_winner = message['flag_find_winner']

        if flag_find_winner == 1:
            return redirect('snod_original_result', id=id)

        else:
            message, flag_checking = checking_already_has_answer(request, message, snod_original=True)
            while flag_checking:
                flag_find_winner = message['flag_find_winner']
                if flag_find_winner != 1:
                    message, flag_checking = checking_already_has_answer(request, message, snod_original=True)

            return render(request, "snod/question.html",
                          {'message': message,
                           'model': model, 'original_snod': 1})


class OriginalSnodDetailView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request, id):
        context = {'response': get_winners_from_model_original_snod(id), 'model_data': (get_model_data(id))[0],
                   'model_header': (get_model_data(id))[1], 'history': get_context_history_answer_original_snod(id),
                   'model': Model.objects.get(id=id)}
        if 'DATABASE_URL' in os.environ:
            context['graph'] = get_graph_snod(id)

        else:
            context['graph'] = 'http://127.0.0.1:8000/media' + get_graph_snod(id)
        return render(request, "snod/original_snod_result.html", {'context': context})

