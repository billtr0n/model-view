# python imports
import json

# django imports
from django import forms
from django.forms import ModelForm

# user defines imports
from .models import Simulation

class SimulationModelForm(ModelForm):
    class Meta:
        model = Simulation
        exclude = ['comments','upload_date', 'user']

class UploadFileForm( forms.Form ):
    file = forms.FileField()

    # handle file parsing here.
    def clean_file(self):
        data = self.cleaned_data['file']
        files = self.parse_file(data)

        # form = SimulationModelForm(data=data_dict)
        # if form.is_valid():
        #     self.instance = form.save(commit=False)
        # else:
        #     raise forms.ValidationError(u'The file contains invalid data.')
        return data


    def save(self):
        instance = getattr(self, "instance", None)
        if instance:
            instance.save()
        return instance

    # custom for SORD parameters.json file
    def parse_file(self, data):
        # data_dict={}
        # columns = [val.name for val in Simulation._meta.get_fields()]
        # json_data = json.loads(''.join(data.readlines()))
        # for key, val in json_data.iteritems():
        #     if key in columns:
        #         data_dict[key]=val
        try:
            files = [item.strip() or None for item in data]
            self.cleaned_data['files'] = files
        except Exception as e:
            print "unable to read upload file. make sure there is one directory per line."
        return files



        

            
            
                

            
        

    
        

        







