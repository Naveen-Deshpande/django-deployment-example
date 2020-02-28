from django import forms
from .models import Post,Comment

# create the requried forms here
class PostForm(forms.ModelForm):

    # create a meta class thst directly connects the forms
    # to the model
    class Meta():

        # set the model
        model = Post
        # set the field that you want to edit
        fields = ('author','title','text')

        # add the widgets for the required field to style it using CSS
        # this goes inside of the meta class and is a dictionary with atrributes
        # (attrs) as a sub dictionary
        widgets = {
            'title':forms.TextInput(attrs={'class':'textinputclass'}),
            # customize the text area with the medium lib, it is connected to 3 diff
            # css classes as mentioned in the sub dictionary attrs
            'text': forms.Textarea(attrs={'class':'editable medium-editor-textarea postcontent'})
        }

class CommentForm(forms.ModelForm):

    class Meta():
        model = Comment
        fields = ('author','text')
        widgets = {
            'author':forms.TextInput(attrs={'class':'textinputclass'}),
            # customize the text area with the medium lib, it is connected to 3 diff
            # css classes as mentioned in the sub dictionary attrs
            'text': forms.Textarea(attrs={'class':'editable medium-editor-textarea'})
        }
