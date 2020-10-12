
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserChangeForm(ModelForm):
    class Meta:
        model = User
        fields = [
            'username',
        ]

    def __init__(self, username=None, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super().__init__(*args, **kwargs)
        # ユーザーの更新前情報をフォームに挿入
        self.fields['username'].widget.attrs['value'] = username
        self.fields['username'].label = "新しい俳号: "
        self.fields['username'].help_text = "漢字、かな、英数字、@/./+/-/_ が使えます。"

    def update(self, user):
        user.username = self.cleaned_data['username']
        user.save()

class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "password1", "password2")
        labels = {
            'username': '俳号',
        }
        help_texts = {
            'username': '漢字、かな、英数字、@/./+/-/_ が使えます。',
        }
