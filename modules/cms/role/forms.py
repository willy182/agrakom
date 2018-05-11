from django.db.models import Q
from django.forms import ModelForm, ModelChoiceField, CharField, TextInput, Select
from django.contrib.auth.models import Group, Permission
from django.core.validators import RegexValidator


class GroupForm(ModelForm):
    alphanumeric = RegexValidator(r'^[0-9a-zA-Z ]*$', 'Only alphanumeric characters are allowed.')
    permissions = ModelChoiceField(initial=None, required=False,
                    queryset=Permission.objects.filter(~Q(content_type_id__in=[1,4,5])).order_by('content_type_id'),
                    empty_label=None,
                    widget=Select(attrs={
                        'id': 'id_get_groups',
                        'class': 'form-control select2',
                        'style': ' width: 100%;', 'multiple':'multiple'}))

    name = CharField(
        max_length=80,
        error_messages={'required': 'Nama Group tidak boleh kosong'},
        widget=TextInput(attrs={'class': "form-control",
                                'placeholder': "Role name", 'id': 'role_name'}),
        validators=[alphanumeric]
    )

    class Meta:
        model = Group
        fields = ('name', 'permissions')
        widgets = {
            'filter': TextInput(attrs={'class': "form-control", }),
        }
