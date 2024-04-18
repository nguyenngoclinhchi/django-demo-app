from django.forms.widgets import RadioSelect
from django.db import models

class CustomBooleanField(models.BooleanField): #radio form
    def formfield(self, **kwargs):
        # choose Có then save True 
        kwargs['widget'] = RadioSelect(choices=((True, 'Có'), (False,'Không')))
        kwargs['initial'] = False
        return super().formfield(**kwargs)
    
class CustomBooleanFieldContact(models.BooleanField): 
    def formfield(self, **kwargs):
        # choose Có then save True 
        kwargs['widget'] = RadioSelect(choices=((True, 'Đã liên hệ'), (False,'Chưa liên hệ')))
        kwargs['initial'] = False
        return super().formfield(**kwargs)
