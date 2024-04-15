from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UsernameField
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
        field_classes = {"username": UsernameField}
        
    def __init__(self, *args, **kwargs):
        """Handle Fields Style"""
        super().__init__(*args, **kwargs)
        
        self.tailwind_input_style = "mt-1 placeholder:text-gray-800 w-full border border-gray-400 px-5 py-4 rounded-2xl hover:border-blue-700 focus:border-blue-600 focus:placeholder:text-gray-50 hover:border-1 outline-none"

        self.fields['first_name'].required = True
        self.fields['first_name'].label = ''
        self.fields['first_name'].strip = True
        self.fields['first_name'].widget.attrs['placeholder'] = _("First Name")
        self.fields['first_name'].widget.attrs['class'] = self.tailwind_input_style
        
        self.fields['last_name'].required = True
        self.fields['last_name'].label = ''
        self.fields['last_name'].strip = True
        self.fields['last_name'].widget.attrs['placeholder'] = _("Last Name")
        self.fields['last_name'].widget.attrs['class'] = self.tailwind_input_style        
        
        self.fields['email'].required = True
        self.fields['email'].label = ''
        self.fields['email'].strip = True
        self.fields['email'].widget = forms.EmailInput()
        self.fields['email'].widget.attrs['placeholder'] = _("email")
        self.fields['email'].widget.attrs['class'] = self.tailwind_input_style        
        
        self.fields['password1'].label = ''
        self.fields['password1'].widget.attrs['placeholder'] = _("Password")
        self.fields['password1'].widget.attrs['class'] = self.tailwind_input_style
        self.fields['password1'].help_text = ''
        
        self.fields['password2'].label = ''
        self.fields['password2'].widget.attrs['placeholder'] = _("Password Confirmation")
        self.fields['password2'].widget.attrs['class'] = self.tailwind_input_style
        self.fields['password2'].help_text = ''
        
        
    def clean_email(self):
        """ Check if email exists"""
        email = self.cleaned_data.get('email')
        
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(message=_("this email already exists"))
            
        return email


class LoginForm(AuthenticationForm):
    def __init__(self, request, *args, **kwargs):
        """Handle Fields Style"""
        super().__init__(request, *args, **kwargs)
        
        self.fields['username'].label = _('Username / Email:')
        self.fields['username'].strip = True
        
        self.fields['username'].widget.attrs['placeholder'] = _("username / Email")
        self.fields['username'].widget.attrs['class'] = "mt-1 placeholder:text-gray-500 w-full border border-gray-400 px-5 py-4 rounded-2xl hover:border-blue-700 focus:border-blue-600 hover:border-1 outline-none"
        
        
        self.fields['password'].label = _('password:')
        self.fields['password'].widget.attrs['placeholder'] = _("password")
        self.fields['password'].widget.attrs['class'] = "mt-1 focus:border-blue-700 outline-none placeholder:text-gray-500 w-full border border-gray-400 px-5 py-4 rounded-2xl hover:border-blue-600 hover:border-1"