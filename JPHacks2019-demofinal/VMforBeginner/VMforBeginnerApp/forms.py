from django import forms
from .utils import PYTHON_PATH

class EditorForm(forms.Form):
    code = forms.CharField(
        widget=forms.Textarea,
        required=False,
    )
    file_name = forms.CharField(
        required=False,
    )

    dir_name = forms.CharField(
        required=False,
    )

    select_python = forms.ChoiceField(
        choices= PYTHON_PATH,
    )

    pip_name = forms.CharField(
        required=False,
    )
    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        open_file_path = request.GET.get('open_file_path')
        if open_file_path:
            try:
                self.fields['code'].initial = open(open_file_path, 'rb').read().decode('utf-8')
            # 現在開いているファイルを削除した
            except FileNotFoundError:
                self.fields['code'].initial = ''
        else:
            self.fields['code'].initial = ''

        venv_path = request.GET.get('venv_path')
        if venv_path:
            choices = [(venv_path, 'venv')] + PYTHON_PATH
            self.fields['select_python'] = forms.ChoiceField(choices=choices)


class ChkForm(forms.Form):
     labels = ['Machine Learning','Visualize', 'other',]
     CHOICE = [
        ('keras','Keras'),
        ('tensorflow','Tensorflow'),
        ('chainer','Chainer')]

     CHOICE1 = [
        ('matplotlib','Matplotlib'),
        ('seaborn','Seaborn'),
        ]
          
     CHOICE2 = [
          ('numpy','numpy'),
          ('pandas','pandas'),
          ('opencv-python','opencv'),
          ]
 
    
     one = forms.MultipleChoiceField(
          label=labels[0],
          required=False,
          disabled=False,
          initial=[],
          choices=CHOICE,
          widget=forms.CheckboxSelectMultiple(attrs={
               'id': 'one','class': 'form-check-input'}))


     two = forms.MultipleChoiceField(
          label=labels[1],
          required=False,
          disabled=False,
          initial=[],
          choices=CHOICE1,
          widget=forms.CheckboxSelectMultiple(attrs={
              'id': 'two','class': 'form-check-input'}))

     three = forms.MultipleChoiceField(
          label=labels[2],
          required=False,
          disabled=False,
          initial=[],
          choices=CHOICE2,
          widget=forms.CheckboxSelectMultiple(attrs={
              'id': 'three','class': 'form-check-input'}))

