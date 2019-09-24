from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


class UserCustomCreationForm(UserCreationForm):
    username = forms.RegexField(
        label='ID',
        max_length=20,
        min_length=5,
        regex=r"^[a-zA-Z0-9]+$",
        error_messages={
            'invalid': "5~20자의 영문, 숫자만 사용 가능합니다."
        })

    password1 = forms.CharField(max_length=16,
                                min_length=8,
                                label='비밀번호',
                                error_messages={
                                    'invalid': '8~16자의 비밀번호를 만들어주세요.'
                                },
                                widget=forms.PasswordInput
                                )
    password2 = forms.CharField(error_messages={
                                    'invalid': '비밀번호가 일치하지 않습니다.'
                                },
                                label='비밀번호 재확인',
                                widget=forms.PasswordInput
                                )

    class Meta:
        model = get_user_model()
        fields = ['username', 'password1', 'password2', ]
