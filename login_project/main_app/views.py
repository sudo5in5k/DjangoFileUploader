# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect, HttpResponse, Http404
from django.views.decorators.http import require_POST
from django.urls import reverse_lazy
from .forms import RegisterForm, PasswordConfirmForm, ForgetPasswordForm, UploadFileForm
from django.contrib import messages
from django.contrib.auth import views as authv
from django import template
from .models import FileUpModel
from .utils import group, file_upload
import os, sys, re
from datetime import datetime
from urllib.parse import quote
from unidecode import unidecode


def index(request):
    context = {
        'user': request.user,
    }
    return render(request, 'main_app/index.html', context)


register = template.Library()


def profile(request):
    context = {
        'user': request.user,
        'group_flag': group.has_group_bool(request),
        'group_list': group.get_user_group_list(request)
    }
    return render(request, 'main_app/profile.html', context)


def register(request):
    form = RegisterForm(request.POST or None)
    context = {
        'form': form,
    }
    return render(request, 'main_app/register.html', context)


@require_POST
def register_save(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "ユーザが正しく登録されました")
            return redirect('main_app:register')
    else:
        form = RegisterForm()

    context = {
        'form': form,
    }
    return render(request, 'main_app/register.html', context)


def password_reset(request):
    context = {
        'post_reset_redirect': reverse_lazy('main_app:password_reset_done'),
        'template_name': 'main_app/password_reset.html',
        'password_reset_form': ForgetPasswordForm,
    }
    return authv.password_reset(request, **context)


def password_reset_done(request):
    context = {
        'template_name': 'main_app/password_reset_done.html'
    }
    return authv.password_reset_done(request, **context)


def password_reset_confirm(request, uidb64, token):
    context = {
        'uidb64': uidb64,
        'token': token,
        'post_reset_redirect': reverse_lazy('main_app:password_reset_complete'),
        'template_name': 'main_app/password_reset_confirm.html',
        'set_password_form': PasswordConfirmForm,
    }
    return authv.password_reset_confirm(request, **context)


def password_reset_complete(request):
    context = {
        'template_name': 'main_app/password_reset_complete.html',
    }
    return authv.password_reset_complete(request, **context)


def certain_project(request, project_name):
    illegal_direct_flag = False
    print(group.get_user_group_list(request))
    print(project_name)
    for gs in group.get_user_group_list(request):
        if str(gs) == project_name:
            illegal_direct_flag = True
            break

    if illegal_direct_flag:
        query_sets = select_records_in_group(project_name)
        context = {
            'user': request.user,
            'group_flag': group.has_group_bool(request),
            'group_list': group.get_user_group_list(request),
            'send_to_html_project': project_name,
            'query_sets': query_sets,
        }
        return render(request, 'main_app/profile_introduce.html', context)
    else:
        return redirect('main_app:profile')



# uploader

UPLOAD_DIR = os.path.dirname(os.path.abspath(__file__)) + '/static/'


def form(request, project_name):
    # アップロードに失敗した場合でもデータを表示するために必要
    query_sets = select_records_in_group(project_name)

    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            file_size = file.size
            upload_directory = os.path.join(UPLOAD_DIR, 'files/' + str(project_name))
            path = upload_directory + '/' + file.name
            os.makedirs(upload_directory, exist_ok=True)
            print(upload_directory)

            file_upload.handle_uploaded_file(file, path)

            # DB
            insert_data = FileUpModel(file_name=file.name, upload_time=datetime.now(), upload_size=file_size,
                                      upload_path=path, upload_group=project_name)
            insert_data.save()
            key_value_upload = 1

            # アップロードに成功させた後にデータを即時反映させるために必要
            query_sets = select_records_in_group(project_name)

            context = {
                'user': request.user,
                'file_name': file.name,
                'file_size': file_size,
                'group_flag': group.has_group_bool(request),
                'group_list': group.get_user_group_list(request),
                'send_to_html_project': project_name,
                'key_value_upload': key_value_upload,
                'query_sets': query_sets,
            }
            return render(request, 'main_app/profile_introduce.html', context)

        else:
            key_value_upload = -1
            print("flag" + str(key_value_upload))
            context = {
                'user': request.user,
                'group_flag': group.has_group_bool(request),
                'group_list': group.get_user_group_list(request),
                'send_to_html_project': project_name,
                'key_value_upload': key_value_upload,
                'query_sets': query_sets,
            }
            return render(request, 'main_app/profile_introduce.html', context)


def upload_complete(request):
    return render(request, 'main_app/upload_complete.html')


def handle_select_button(request, project_name):
    print(request.POST)
    if request.method == 'POST':
        if 'download_button' in request.POST:
            return download_file(request, project_name)
        elif 'delete_button' in request.POST:
            delete_file(request, project_name)
        query_sets = select_records_in_group(project_name)
        context = {
            'user': request.user,
            'group_flag': group.has_group_bool(request),
            'group_list': group.get_user_group_list(request),
            'send_to_html_project': project_name,
            'query_sets': query_sets,
        }
        return render(request, 'main_app/profile_introduce.html', context)


def download_file(request, project_name):
    file_name = request.POST['download_button']
    path = select_path_in_group_and_title(project_name, file_name)
    if os.path.exists(path):
        with open(path, 'rb') as f:
            print(f)
            response = HttpResponse(f.read(), content_type='application/octet-stream')
            response['Content-Disposition'] = \
                "attachment;" \
                "filename={ascii_filename};" \
                "filename*=UTF-8''{utf_filename}".format(
                    ascii_filename=unidecode(file_name).replace(' ', '_'),
                    utf_filename=quote(file_name)
                )
            return response
        raise Http404


def delete_file(request, project_name):
    # fileの削除
    file_name = request.POST['delete_button']
    path = select_path_in_group_and_title(project_name, file_name)
    # DBからデータを削除 (同じ名前/パスのものは一括削除)
    delete_path_in_group_and_title(project_name, file_name, path)
    os.remove(path)




# DB statements as follows:
# equal to "select file_name, upload_path, upload_size, upload_time from tbl where upload_group=group_str
# order by upload_time"
def select_records_in_group(group_str):
    query = FileUpModel.objects.values_list('file_name', 'upload_path', 'upload_size', 'upload_time').filter(
        upload_group=group_str).distinct().order_by('upload_time').reverse()
    query_sets = [q for q in query]
    return query_sets


def select_path_in_group_and_title(group_str, title_str):
    query = FileUpModel.objects.values_list('upload_path').filter(upload_group=group_str) \
        .filter(file_name=title_str).distinct().order_by('upload_time').reverse().first()
    return query[0]


def delete_path_in_group_and_title(group_str, title_str, path_str):
    FileUpModel.objects.all().filter(upload_group=group_str) \
        .filter(file_name=title_str).filter(upload_path=path_str).delete()
