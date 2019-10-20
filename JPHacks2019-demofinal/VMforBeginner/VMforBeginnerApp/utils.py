from contextlib import contextmanager
import io
import os
import subprocess
import sys
import traceback
from django.conf import settings

DEFAULT_PYTHON_PATH = [(sys.executable, 'このDjangoを実行してるPython')]
USER_PYTHON_PATH = getattr(settings, 'PYTHON_PATH', [])
PYTHON_PATH = DEFAULT_PYTHON_PATH + USER_PYTHON_PATH

# 拡張子と、Ace.jsのmode名に対応
FILE_TYPE = {
    '.py': 'python',
    '.html': 'html',
    '.css': 'css',
    '.js': 'javascript',
    '.rst': 'rst',
    '.json': 'json',
    '.xml': 'xml',
}
USER_FILE_TYPE = getattr(settings, 'FILE_TYPE', {})
FILE_TYPE.update(USER_FILE_TYPE)

ORIGIN_DEFAULT_ACE_TYPE = 'plain_text'
USER_DEFAULT_ACE_TYPE = getattr(settings, 'DEFAULT_ACE_TYPE', '')
if USER_DEFAULT_ACE_TYPE:
    DEFAULT_ACE_TYPE = USER_DEFAULT_ACE_TYPE
else:
    DEFAULT_ACE_TYPE = ORIGIN_DEFAULT_ACE_TYPE


@contextmanager
def stdoutIO():
    """一時的にstdoutを変更する"""

    old = sys.stdout
    sys.stdout = io.StringIO()
    yield sys.stdout
    sys.stdout = old


def execute_python_exec(code):
    """pythonコードをexecで評価し、出力を返す

    引数:
        code: Pythonコードの文字列

    返り値:
        出力とエラーの文字列
    """

    output = ''
    with stdoutIO() as stdout:
        error = ''
        try:
            exec(code)
        except:
            error = traceback.format_exc()
        finally:
            output = stdout.getvalue() + error
    return output


def execute_cmd(cmd, timeout=120):
    """コマンドを実行する"""

    ret = subprocess.run(
        cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        timeout=timeout, encoding='cp932')
    return ret.stdout


def make_path_list(current_path='.'):
    """直下のディレクトリ、ファイルの一覧を返す

    引数:
        current_path: 基準となるパス。デフォルトは'.'

    返り値:
        path引数が、 '/path/to'　だった例
        
        {
        'files': [('main.py', '/path/to/main.py'), ('memo.txt', '/path/to/memo.txt')],
        'dirs': [('前のフォルダ', '/path'), ('tmp', '/path/to/tmp'), ('static', '/path/to/static')],
        'venv': /path/to/python/path,
        }
        のような辞書を返す
    """

    # ディレクトリや全てのファイルの名前が入る
    files_and_dirs = os.listdir(current_path)

    # dirnameで前のフォルダを表せます
    before_dir = ('前のフォルダ', os.path.dirname(current_path))

    # ファイル一覧とディレクトリ一覧の作成処理
    files = []
    dirs = [before_dir]
    venv = None

    for name in files_and_dirs:
        full_path = os.path.join(current_path, name)
        if os.path.isdir(full_path):
            dirs.append((name, full_path))
        else:
            if name == 'python.exe':
                venv = full_path
            else:
                files.append((name, full_path))

    result_dict = {
        'files': files,
        'dirs': dirs,
        'venv': venv,
    }

    return result_dict


def filename_and_filetype(file_path):
    """ファイル名とファイルタイプを返す

    /var/www/html/main.pyならば、 main.pyとpythonというタプルを返します
    file_typeは、Ace.jsのmode部分に指定できる形式です
    """
    
    if file_path:
        file_name = os.path.basename(file_path)
    else:
        file_name = 'no file'
    _, file_extension = os.path.splitext(file_path)
    file_type = FILE_TYPE.get(file_extension, DEFAULT_ACE_TYPE)
    return file_name, file_type


def url_replace(url_dict, field, value):
    """GETパラメータを一部を置き換える"""

    url_dict[field] = value
    return url_dict.urlencode()


def url_replace_with_nodelete(url_dict, field=None, value=None):
    """GETパラメータを一部を置き換える。deleteパスを削除する"""

    if field and value:
        url_dict[field] = value
    if 'delete_path' in url_dict:
        del url_dict['delete_path']
    return url_dict.urlencode()
