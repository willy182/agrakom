from django.forms import ModelForm, ModelChoiceField, Select, FileInput, FileField, CharField, TextInput, Textarea, ChoiceField, RadioSelect, IntegerField, forms
from modules.cms.aboutus.models import AboutUs, SliderAboutUs
# from django.core.files.images import get_image_dimensions

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

    image = FileField(widget=FileInput(attrs={'class': 'form-control','id': 'img_input'}), required=True, error_messages={'required': 'image can not be empty'},)

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
    #     field = "image"  # Field name
    #     MinW = 960  # Min. Width
    #     checkH = False  # If it's going to validate the height
    #     MinH = 800  # Min. Height
    #     text_minw = u"The image width is lower than %i" % MinW  # Error text for min. width
    #     text_minh = u"The image height is lower than %i" % MinH  # Error text for min. height
    #
    #     # clean_(name of field)
    #
    # def clean_image(self):
    #     image = self.cleaned_data.get(self.Meta.field)
    #     if not image:
    #         raise forms.ValidationError(u"No image")
    #     else:
    #         w, h = get_image_dimensions(image)
    #         if w < self.Meta.MinW:
    #             raise forms.ValidationError(self.Meta.text_minw)
    #         if h < self.Meta.MinH and self.Meta.checkH == True:
    #             raise forms.ValidationError(self.Meta.text_minw)
    #
    #     return image
