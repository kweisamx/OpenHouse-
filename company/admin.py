from django.contrib import admin
from company.models import Company
from django.contrib.auth.admin import UserAdmin
from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.conf.urls import url,include
from . import export


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = Company
        fields = '__all__'

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField(label= ("Password"),
            help_text= ( "<h3><a href=\"../password/\">變更廠商密碼</a></h3>"))

    class Meta:
        model = Company
        fields = ['name']

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('cid','name', 'category','hr_name','hr_phone','hr_email','last_update')
    list_filter = ()
    fieldsets = (
            ("基本資料", {
                'classes': ('wide',),
                'fields': ('cid','password','name','shortname','category','phone',
               'postal_code','address','website','brief','recruit_info','logo','recruit_url','business_project','relation_business','subsidiary','receipt_title')
                }
                ),
            ("人資資料", {
                'classes': ('wide',),
                'fields': ('hr_name','hr_phone','hr_fax','hr_mobile','hr_email')
                }
                ),
            ("第二位人資資料", {
                'classes': ('wide',),
                'fields': ('hr2_name','hr2_phone','hr2_fax','hr2_mobile','hr2_email','hr_ps')
                }
                ),
            )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
            ("基本資料", {
                'classes': ('wide',),
                'fields': ('cid','password1', 'password2','name','shortname',
               'category','phone','postal_code','address','website','brief','recruit_info','logo','recruit_url','receipt_title')
                }
                ),
            ("人資資料", {
                'classes': ('wide',),
                'fields': ('hr_name','hr_phone','hr_fax','hr_mobile','hr_email')
                }
                ),
            ("第二位人資資料", {
                'classes': ('wide',),
                'fields': ('hr2_name','hr2_phone','hr2_fax','hr2_mobile','hr2_email','hr_ps')
                }
                ),
            )
    search_fields = ('cid','name','shortname')
    ordering = ('cid',)
    filter_horizontal = ()

    def get_urls(self):
        urls = super(UserAdmin, self).get_urls()
        my_urls = [
                url(r'^export/$', export.Export_Company),
                ]
        return my_urls + urls


# Now register the new UserAdmin...
admin.site.register(Company, UserAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
#admin.site.unregister(Group)
