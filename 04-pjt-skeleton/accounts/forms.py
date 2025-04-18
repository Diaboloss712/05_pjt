from django import forms
from .models import User  # 여기에서 커스텀 User 모델을 가져와야 합니다.
from django.contrib.auth.forms import PasswordChangeForm

# 로그인 폼
class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=100, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

# 사용자 정보 수정 폼
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User  # 커스텀 User 모델 사용
        fields = ['username', 'email', 'first_name', 'last_name', 'followers']
        widgets = {
            'followers': forms.CheckboxSelectMultiple(),  # followers는 다대다 관계이므로 다중 선택을 위한 위젯
        }

# 사용자 등록 폼
class UserForm(forms.ModelForm):
    class Meta:
        model = User  # 커스텀 User 모델 사용
        fields = ['username', 'email', 'first_name', 'last_name', 'followers']
        widgets = {
            'followers': forms.CheckboxSelectMultiple(),  # followers는 다대다 관계이므로 다중 선택을 위한 위젯
        }

# 비밀번호 변경 폼 
class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput, required=True)
    new_password1 = forms.CharField(widget=forms.PasswordInput, required=True)
    new_password2 = forms.CharField(widget=forms.PasswordInput, required=True)
