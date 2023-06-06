from django import forms

from posts.models import Post, PostComment


class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            "image",
            "description",
        ]
        widgets = {
            "image": forms.FileInput(
                attrs={"class": "form-control"},
            ),
            "description": forms.Textarea(
                attrs={"class": "form-control"}
            )
        }


class PostUpdateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            "image",
            "description"
        ]
        widgets = {
            "image": forms.FileInput(
                attrs={"class": "form-control"},
            ),
            "description": forms.Textarea(
                attrs={"class": "form-control"}
            )
        }
        
    def save(self, commit=True):
        instance = super().save(commit=False)
        if 'image' in self.changed_data and not instance.image:
            instance.image = self.changed_data['image']
        if commit:
            instance.save()
        return instance


class PostCommentForm(forms.ModelForm):
    class Meta:
        model = PostComment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control'})
        }
