# from django.core.files.images import get_image_dimensions
from django.forms import ModelForm, FileInput, FileField, CharField, TextInput, Textarea, ChoiceField, RadioSelect, IntegerField, forms
from modules.cms.ourclients.models import Ourclient


class CreateOurClientsForm(ModelForm):
    statuschoice = (
        (True, 'Active'),
        (False, 'Not Active'),
    )

    # name = CharField(
    #     max_length=225,
    #     error_messages={'required': 'Title can not be empty', 'placeholder': "input title"},
    #     widget=TextInput(attrs={'class': "form-control", 'placeholder': "input title"}),
    # )
    # description = CharField(
    #     required=False,
    #     widget=Textarea(attrs={'class': 'form-control', 'placeholder': "input physical location description"}),
    # )

    image = FileField(widget=FileInput(attrs={'class': 'form-control', 'id': 'img_input'}), required=True, error_messages={'required': 'image can not be empty'},)

    # caption = CharField(
    #     max_length=225,
    #     error_messages={'placeholder': "input caption"},
    #     widget=TextInput(attrs={'class': "form-control", 'placeholder': "input caption"}),
    # )

    # position = IntegerField(
    #     error_messages={'placeholder': "input position"},
    #     widget=TextInput(attrs={'class': "form-control", 'placeholder': "input position"}),
    # )

    status = ChoiceField(
        error_messages={'required': 'status can not be empty'},
        widget=RadioSelect(attrs={'class': "Radio"}),
        choices=statuschoice,
        initial=True
    )

    class Meta:
        model = Ourclient
        fields = ('image', 'status')
    #     field = "image"  # Field name
    #     MinW = 270  # Min. Width
    #     MaxW = 270  # Max. Width
    #     checkH = False  # If it's going to validate the height
    #     MinH = 206  # Min. Height
    #     MaxH = 206  # Max. Height
    #     text_minw = u"The image width is lower than %i" % MinW  # Error text for min. width
    #     text_maxw = u"The image width is larger than %i" % MaxW  # Error text for max. width
    #     text_minh = u"The image height is lower than %i" % MinH  # Error text for min. height
    #     text_maxh = u"The image height is larger than %i" % MaxH  # Error text for max. height
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
    #         if w > self.Meta.MaxW:
    #             raise forms.ValidationError(self.Meta.text_maxw)
    #         if h < self.Meta.MinH and self.Meta.checkH == True:
    #             raise forms.ValidationError(self.Meta.text_minw)
    #         if h > self.Meta.MaxH and self.Meta.checkH == True:
    #             raise forms.ValidationError(self.Meta.text_maxw)
    #
    #     return image
