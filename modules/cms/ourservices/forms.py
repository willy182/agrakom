from django.core.files.images import get_image_dimensions
from django.forms import ModelForm, ModelChoiceField, Select, FileInput, FileField, CharField, TextInput, Textarea, ChoiceField, RadioSelect, IntegerField, forms
from modules.cms.ourservices.models import OurServices, OurServiceDetail


class CreateServiceForm(ModelForm):
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
        model = OurServices
        fields = ('title', 'description', 'status')


class CreateServiceDetailForm(ModelForm):
    statuschoice = (
        (True, 'Active'),
        (False, 'Not Active'),
    )

    our_services = ModelChoiceField(initial='Select Our Services', required=True, queryset=OurServices.objects.filter().order_by('id'),
                                    widget=Select(attrs={'class': 'form-control ', }))

    image = FileField(widget=FileInput(attrs={'class': 'form-control', 'id': 'img_input'}), required=True)

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
        model = OurServiceDetail
        fields = ('our_services', 'image', 'caption', 'status')
        field = "image"  # Field name
        MinW = 280  # Min. Width
        MaxW = 280  # Max. Width
        checkH = False  # If it's going to validate the height
        MinH = 280  # Min. Height
        MaxH = 280  # Max. Height
        text_minw = u"The image width is lower than %i" % MinW  # Error text for min. width
        text_maxw = u"The image width is larger than %i" % MaxW  # Error text for max. width
        text_minh = u"The image height is lower than %i" % MinH  # Error text for min. height
        text_maxh = u"The image height is larger than %i" % MaxH  # Error text for max. height

        # clean_(name of field)

    def clean_image(self):
        image = self.cleaned_data.get(self.Meta.field)
        if not image:
            raise forms.ValidationError(u"No image")
        else:
            w, h = get_image_dimensions(image)
            if w < self.Meta.MinW:
                raise forms.ValidationError(self.Meta.text_minw)
            if w > self.Meta.MaxW:
                raise forms.ValidationError(self.Meta.text_maxw)
            if h < self.Meta.MinH and self.Meta.checkH == True:
                raise forms.ValidationError(self.Meta.text_minw)
            if h > self.Meta.MaxH and self.Meta.checkH == True:
                raise forms.ValidationError(self.Meta.text_maxw)

        return image
