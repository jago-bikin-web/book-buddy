from django import forms
from mybuddy.models import OwnedBook


class UpdateForm(forms.ModelForm):

    page_track = forms.IntegerField(
        required= False,
        widget= forms.TextInput(attrs= {
            "class": "page-track border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 bg-slate-200 border-gray-600 text-grey-900 dark:focus:ring-primary-500 dark:focus:border-primary-500",
            "type": "number",
        })
    )
    # R = lagi dibaca, F = finish, W = wistlish
    STATUS_CHOICES = [('W', 'Wishlist'), ('R', 'Read'), ('F', 'Finish')]
    status = forms.ChoiceField(
        required= True,
        choices= STATUS_CHOICES,
        widget= forms.Select(attrs= {
            "class": "status border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-500 focus:border-primary-500 block w-full p-2.5 bg-slate-200 border-gray-600 dark:placeholder-gray-400 text-grey-900 dark:focus:ring-primary-500 dark:focus:border-primary-500",
        })
    )
    
    ulasan = forms.CharField(
        required= False,
        widget= forms.Textarea(attrs= {
            "class": "ulasan block p-2.5 w-full text-sm text-gray-900 rounded-lg border border-gray-300 focus:ring-primary-500 focus:border-primary-500 bg-slate-200 border-gray-600 dark:placeholder-gray-400 text-grey-900 dark:focus:ring-primary-500 dark:focus:border-primary-500",
            "rows":5,
            "placeholder": "Ulasan...",
        })
    )
    class Meta:
        model = OwnedBook
        fields = ["page_track","status", "ulasan"]