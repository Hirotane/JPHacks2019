import os
import shutil

from .forms import EditorForm, ChkForm
from .utils import (
    execute_python_exec, filename_and_filetype,
    make_path_list, execute_cmd, url_replace,
    url_replace_with_nodelete,
)

from django.conf import settings
from django.shortcuts import redirect
from django.shortcuts import render
from django.views import generic

# forchecklist
from django.http.response import HttpResponse
from django.shortcuts import render, render_to_response
from django.contrib.staticfiles.templatetags.staticfiles import static
from . import forms
from django.template.context_processors import csrf


class Home(generic.FormView):
    template_name = 'VMforBeginnerApp/home1.html'
    form_class = EditorForm


    # def get(self, request, *args, **kwargs):
    #     delete_path = self.request.GET.get('delete_path')
    #     if delete_path:
    #         try:
    #             if os.path.isfile(delete_path):
    #                 os.remove(delete_path)
    #             else:
    #                 shutil.rmtree(delete_path)
    #         # 削除後に、F5などをした
    #         except FileNotFoundError:
    #             pass
    #     return self.render_to_response(self.get_context_data())

    def get_current_dirpath(self):
        """エディタの、現在のディレクトリパスを取得する"""

        # パラメータがなければ、manage.py があるディレクトリを返す
        current_path = self.request.GET.get('dir_path', settings.BASE_DIR)

        # ?dir_path= のような場合
        if not current_path:
            current_path = settings.BASE_DIR

        # もしもファイルだった場合は、そのディレクトリのパスに
        if os.path.isfile(current_path):
            current_path = os.path.dirname(current_path)

        return current_path

    def get_context_data(self, **kwargs):
        """contextの取得。アクセスされれば常に呼び出される"""

        # 開いているファイルの取得
        open_file_path = self.request.GET.get('open_file_path', '')

        # ファイル名とファイルの種類を取得
        file_name, file_type = filename_and_filetype(open_file_path)

        # エディタの、現在表示すべきディレクトリパスを取得
        current_path = self.get_current_dirpath()

        # venvのパス
        venv_path = self.request.GET.get('venv_path', '')

        # カレントの、ファイルやディレクトリの一覧が詰まったオブジェクト
        path_list = make_path_list(current_path)



        # contextのアップデート。{{ current_path }}等が使えるようになる
        extra_context = {
            'current_path': current_path,
            'path_list': path_list,
            'open_file_path': open_file_path,
            'file_name': file_name,
            'file_type': file_type,
            'venv_path': venv_path,
        }
        kwargs.update(extra_context)
        return super().get_context_data(**kwargs)


    def get_form_kwargs(self):

        kwargs = super().get_form_kwargs()
        kwargs.update(
            {'request': self.request,}
        )
        return kwargs

    # def run_exec(self, form):
    #     """exec(code)でプログラムを実行する"""

    #     code = form.cleaned_data['code']

    #     # プログラムが空欄の場合は、実行しない
    #     if not code:
    #         output = '空欄です'
    #     else:
    #         output = execute_python_exec(code)

    #     context = self.get_context_data(form=form, output=output)
    #     return self.render_to_response(context)

    # def run(self, form):
    #     """プログラムを実行する"""

    #     open_file_path = self.request.GET.get('open_file_path')

    #     # ファイルを開いてなければ、実行しない
    #     if not open_file_path:
    #         output = 'ファイルを開いてください'
    #     elif not open_file_path.endswith('.py'):
    #         output = '実行はpythonファイルのみです'
    #     else:
    #         code = form.cleaned_data['code'] + '\r\n'
    #         binary_code = code.encode('utf-8')
    #         with open(open_file_path, 'wb') as file:
    #             file.write(binary_code)

    #         python_path = form.cleaned_data['select_python']
    #         cmd = f'{python_path} {open_file_path}'
    #         output = execute_cmd(cmd)

    #     context = self.get_context_data(form=form, output=output)
    #     return self.render_to_response(context)

    # def new_save(self, form):
    #     """プログラムの新規保存"""

    #     file_name = form.cleaned_data['file_name']

    #     # ファイル名を入力してないと保存させない
    #     if file_name:
    #         current_path = self.get_current_dirpath()
    #         file_path = os.path.join(current_path, file_name)
    #         if os.path.exists(file_path):
    #             output = f'既にファイルが存在しています {file_path}'
    #         else:
    #             code = form.cleaned_data['code'] + '\r\n'
    #             binary_code = code.encode('utf-8')
    #             with open(file_path, 'wb') as file:
    #                 file.write(binary_code)
    #             response = redirect('VMforBeginnerApp:home')
    #             url_dict = self.request.GET.copy()
    #             response['Location'] += '?' + url_replace_with_nodelete(url_dict, 'open_file_path', file_path)
    #             return response
    #     else:
    #         output = 'ファイル名を入力してください'
    #     context = self.get_context_data(form=form, output=output)
    #     return self.render_to_response(context)

    # def overwrite_save(self, form):
    #     """プログラムの新規保存・上書き保存を行う"""

    #     open_file_path = self.request.GET.get('open_file_path')

    #     # ファイルを開いていないと上書き保存させない
    #     if open_file_path:
    #         code = form.cleaned_data['code'] + '\r\n'
    #         binary_code = code.encode('utf-8')
    #         with open(open_file_path, 'wb') as file:
    #             file.write(binary_code)
    #         output = f'{open_file_path}を上書き保存しました'

    #     else:
    #         output = '何かファイルを開いてください'
    #     context = self.get_context_data(form=form, output=output)
    #     return self.render_to_response(context)

    def make_dir(self, form):

        #のま:アプリやプロジェクト名入れてもらってディレクトリ作成したい!
        # 新規作成とした時にファイル名入力してもらう?

        dir_name = form.cleaned_data['dir_name']
        # open_file_path = self.request.GET.get('open_file_path')
        # フォルダ名を入力してないと保存させない
        if dir_name:
            current_path = self.get_current_dirpath()
            dir_path = os.path.join(current_path, dir_name)
            if os.path.exists(dir_path):
                output = f'既にフォルダが存在しています {dir_path}'
            else:
                os.mkdir(dir_path)
                output = f'{dir_path}を作りました'
        else:
            output = 'フォルダ名を入力してください'
        context = self.get_context_data(form=form, output=output)
        return self.render_to_response(context)


    def venv(self, form):

        #のま:virtualenv pythonversion 環境名が入力できるようにお願いします to 永田氏

        dir_name = form.cleaned_data['dir_name']
        python_path = form.cleaned_data['select_python']

        # フォルダ名を入力してないと保存させない
        if dir_name:
            current_path = self.get_current_dirpath()
            dir_path = os.path.join(current_path, dir_name)
            if os.path.exists(dir_path):
                output = f'既にフォルダが存在しています {dir_path}'
            else:
                cmd = f'{python_path} -m venv {dir_path}'
                execute_cmd(cmd)
                output = f'{dir_path}をvenvで作りました。'
        else:
            output = 'フォルダ名を入力してください'
        context = self.get_context_data(form=form, output=output)
        return self.render_to_response(context)

    def pip_install(self, form):

        pip_name = form.cleaned_data['pip_name']
        python_path = form.cleaned_data['select_python']

        # pip名を入力してないと保存させない
        if pip_name:
            cmd = f'{python_path} -m pip install -U {pip_name}'
            output = execute_cmd(cmd)
        else:
            output = 'pip名を入力してください'
        context = self.get_context_data(form=form, output=output)
        return self.render_to_response(context)

    def pip_freeze(self, form):

        python_path = form.cleaned_data['select_python']

        cmd = f'{python_path} -m pip freeze'
        output = execute_cmd(cmd)

        context = self.get_context_data(form=form, output=output)
        return self.render_to_response(context)

    def pip_freeze_write(self, form):

        #のま:requirement.txt作れます

        current_path = self.get_current_dirpath()
        python_path = form.cleaned_data['select_python']
        path = os.path.join(current_path, 'requirements.txt')
        cmd = f'{python_path} -m pip freeze > {path}'
        execute_cmd(cmd)
        output = f'{path}に作成しました'

        context = self.get_context_data(form=form, output=output)
        return self.render_to_response(context)


    def form_valid(self, form):
        """Run、又はSaveを押した際に呼び出される"""

        submit_kind = self.request.POST['submit-kind']
        function = getattr(self, submit_kind)
        if function and callable(function):
            return function(form)



# class Checklist(generic.FormView):
#     template_name = 'VMforBeginnerApp/demo03.html'
    # form_class = ChkForm
def demo3(request):
    labels = ['チェック','その他','機械学習','動的選択肢１','動的選択肢２']
    # 入力結果を格納する辞書
    results = {}
    radios = {}
    ret = ''
    if request.method == 'POST':
        # 入力されたデータの受取
        # results[labels[0]] = request.POST.getlist("one")
        results[labels[1]] = request.POST.getlist("two")
        results[labels[2]] = request.POST.getlist("three")
        # results[labels[2]] = request.POST.getlist("three")
        # results[labels[3]] = request.POST.getlist("four")
        # results[labels[4]] = request.POST.getlist("five")
        ret = 'OK'
        c = {'results': results,'ret':ret}
        # c = {'results': results}
    else:
        form = forms.ChkForm()
        # choice1 = []
        # choice1.append(('1','動的選択肢１'))
        # choice1.append(('2','動的選択肢２'))
        # choice1.append(('3','動的選択肢３'))
        # choice1.append(('4','動的選択肢４'))
        # form.fields['four'].choices = choice1
        # form.fields['four'].initial = ['2']
        # form.fields['five'].choices = choice1
        # form.fields['five'].initial = ['3']
        # c = {'form': form,'ret':ret}
        c = {'form': form}
        # CFRF対策（必須）
        c.update(csrf(request))
    return render(request,'VMforBeginnerApp/demo03.html',c)
