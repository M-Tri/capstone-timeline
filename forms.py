from django import forms
from .models import Label

POPULARITY = [
    ('High', 'High'),
    ('Medium', 'Medium'),
    ('Low', 'Low'),
]

class PostNews(forms.Form):
    title = forms.CharField(max_length=100)
    author_name = forms.CharField(max_length=100)
    original_post = forms.URLField(
        label="Main Image", 
    )
    url_field_2 = forms.URLField(
        label="Image 2 (Optional)",
        required=False,
    )
    url_field_3 = forms.URLField(
        label="Image 3 (Optional)", 
        required=False,
    )
    content = forms.CharField(
        widget=forms.Textarea(), 
    )
    popularity = forms.ChoiceField(choices=POPULARITY, widget=forms.RadioSelect)
    url_source = forms.URLField(
        label="Source URL", 
    )


class PostOpinion(forms.Form):
    title = forms.CharField(max_length=100)
    author_name = forms.CharField(max_length=100)
    content = forms.CharField(
        widget=forms.Textarea(), 
    )
    labels_select = forms.ModelMultipleChoiceField(
        queryset=None,
        widget=forms.CheckboxSelectMultiple,
        )
    bias = forms.IntegerField()
    opinion = forms.ModelChoiceField(
    queryset=Opinion.objects.none(),
    widget=forms.TextInput(attrs={'list': 'opinion-datalist'}),
    required=True,
    )
    
    # Extract labels dynamically when form is created rather than when class is defined.
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["labels_select"].queryset = Label.objects.all()
        self.fields["opinion"].queryset = Opinion.objects.all()
