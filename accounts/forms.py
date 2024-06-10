from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from accounts.models import UserProfile

class UserSignupForm(UserCreationForm):
    first_name = forms.CharField(required= True)
    last_name = forms.CharField(required= True)
    class Meta:
        model =User
        fields =['username','password1','password2','first_name','last_name','email']

    def save(self,commit =True):
        our_user = super().save(commit=False)
        if commit:
            our_user.save()
        return our_user
    
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class':(
                    'appearance-none block w-full bg-gray-200 '
                    'text-gray-700 border border-gray-200 rounded '
                    'py-3 px-4 leading-tight focus:outline-none '
                    'focus:bg-white focus:border-gray-500'
                )
            })


class EditeProfileForm(forms.ModelForm):
    image = forms.ImageField(required=False)
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    website = forms.URLField(required=False)
    description =forms.TextInput()
    facebook = forms.URLField(required=False)
    linkedin = forms.URLField(required=False) 
    class Meta:
        model =UserProfile
        fields =['image', 'date_of_birth', 'website', 'facebook', 'linkedin','description']

    
    def save(self, commit=True):
        profile_instance = super().save(commit=False)
        if commit:
            profile_instance.is_active = False
            profile_instance.save()
        return profile_instance

    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': (
                    'appearance-none block w-full bg-gray-200 '
                    'text-gray-700 border border-gray-200 rounded '
                    'py-3 px-4 leading-tight focus:outline-none '
                    'focus:bg-white focus:border-gray-500'
                )
            })
