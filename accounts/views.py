from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin

from django.urls import reverse_lazy
from django.views import generic

from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView

from .forms import UserChangeForm, MyUserCreationForm
 
class SignUpView(generic.CreateView):
    form_class = MyUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'accounts/signup.html'


class UserProfileView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'registration/profile.html'
    def get_queryset(self):
        return User.objects.get(id=self.request.user.id)


class UserChangeView(LoginRequiredMixin, generic.FormView):
    template_name = 'registration/change.html'
    form_class = UserChangeForm
    success_url = reverse_lazy('accounts:profile')
    
    def form_valid(self, form):
        #formのupdateメソッドにログインユーザーを渡して更新
        form.update(user=self.request.user)
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # 更新前のユーザー情報をkwargsとして渡す
        kwargs.update({
            'username' : self.request.user.username,
        })
        return kwargs
