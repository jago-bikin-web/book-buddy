from django import forms
from mybuddy.models import OwnedBook


class UpdateForm(forms.ModelForm):
    # R = lagi dibaca, F = finish, W = wistlish
    STATUS_CHOICES = [('R', 'Read'), ('F', 'Finish'), ('W', 'Wistlish')]
    status = forms.ChoiceField(
        label = "Status",
        required= True,
        choices= STATUS_CHOICES,
        widget= forms.Select(attrs= {
            "class": "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-500 focus:border-primary-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500",
        })
    )
    
    ulasan = forms.CharField(
        required= True,
        widget= forms.Textarea(attrs= {
            "class": "block p-2.5 w-full text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 focus:ring-primary-500 focus:border-primary-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500",
            "rows":5,
            "placeholder": "Ulasan...",
        })
    )
    class Meta:
        model = OwnedBook
        fields = ["status", "ulasan"]