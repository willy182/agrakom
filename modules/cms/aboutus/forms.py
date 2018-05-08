from django.forms import ModelForm, ModelChoiceField, Select, FileInput, FileField, CharField, TextInput, Textarea, ChoiceField, RadioSelect, IntegerField
from modules.cms.aboutus.models import AboutUs, SliderAboutUs


class CreateAboutusForm(ModelForm):
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

    status = ChoiceField(
        error_messages={'required': 'status can not be empty'},
        widget=RadioSelect(attrs={'class': "Radio"}),
        choices=statuschoice,
        initial=True
    )

    class Meta:
        model = AboutUs
        fields = ('title', 'description', 'status')


class CreateSliderAboutUsForm(ModelForm):
    statuschoice = (
        (True, 'Active'),
        (False, 'Not Active'),
    )

    about_us = ModelChoiceField(initial='Select About Us', required=True, queryset=AboutUs.objects.filter().order_by('id'),
                                widget=Select(attrs={'class': 'form-control ', }))

    position = IntegerField(
        error_messages={'placeholder': "input position"},
        widget=TextInput(attrs={'class': "form-control", 'placeholder': "input position"}),
    )

    image = FileField(widget=FileInput(attrs={'class': 'form-control'}), required=True, error_messages={'required': 'image can not be empty'},)

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
        model = SliderAboutUs
        fields = ('about_us', 'position', 'image', 'caption', 'status')
