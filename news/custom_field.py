from django.forms.widgets import RadioSelect
from django.db import models

class CustomBooleanField(models.BooleanField): #radio form
    def formfield(self, **kwargs):
        # choose Có then save True 
        kwargs['widget'] = RadioSelect(choices=((True, 'Có'), (False,'Không')))
        kwargs['initial'] = False
        return super().formfield(**kwargs)