from django.forms import ModelForm, ModelChoiceField, Select, FileInput, FileField, CharField, TextInput, Textarea, ChoiceField, RadioSelect, IntegerField
from modules.cms.awards.models import AwardsGalery, DetailGalery


class CreateAwardsForm(ModelForm):
    statuschoice = (
        (True, 'Active'),
        (False, 'Not Active'),
    )

    title = CharField(
        max_length=225,
        error_messages={'required': 'Title can not be empty', 'placeholder': "input title"},
        widget=TextInput(attrs={'class': "form-control", 'placeholder': "input title"}),
    )
    description = CharField(
        required=False,
        widget=Textarea(attrs={'class': 'form-control', 'placeholder': "input physical location description"}),
    )

    image = FileField(widget=FileInput(attrs={'class': 'form-control'}), required=True, error_messages={'required': 'image can not be empty'})

    position = IntegerField(
        error_messages={'placeholder': "input position"},
        widget=TextInput(attrs={'class': "form-control", 'placeholder': "input position"}),
    )

    status = ChoiceField(
        error_messages={'required': 'status can not be empty'},
        widget=RadioSelect(attrs={'class': "Radio"}),
        choices=statuschoice,
        initial=True
    )

    class Meta:
        model = AwardsGalery
        fields = ('title', 'description', 'image', 'position', 'status')


class CreateAwardDetailForm(ModelForm):
    statuschoice = (
        (True, 'Active'),
        (False, 'Not Active'),
    )

    awards_galery = ModelChoiceField(initial='Select About Us', required=True, queryset=AwardsGalery.objects.filter().order_by('id'),
                                     widget=Select(attrs={'class': 'form-control ', }))

    position = IntegerField(
        error_messages={'placeholder': "input position"},
        widget=TextInput(attrs={'class': "form-control", 'placeholder': "input position"}),
    )

    image = FileField(widget=FileInput(attrs={'class': 'form-control'}), required=True)

    caption = CharField(
        max_length=225,
        error_messages={'placeholder': "input caption"},
        widget=TextInput(attrs={'class': "form-control", 'placeholder': "input caption"}),
    )

    status = ChoiceField(
        error_messages={'required': 'status can not be empty'},
        widget=RadioSelect(attrs={'class': "Radio"}),
        choices=statuschoice,
        initial=True
    )

    class Meta:
        model = DetailGalery
        fields = ('awards_galery', 'position', 'image', 'caption', 'status')
