from django import forms
from urbanizze.map.models import Terreno

EDIFICATION = (
    ('Comercial', 'Comercial'),
    ('Residencial', 'Residencial'),
    ('Industrial', 'Industrial'),
    ('Institucional', 'Institucional'),
)


class TerrenoForm(forms.ModelForm):
    label_edification = '3. Qual o tipo de edificação você deseja construir?'
    label_pav = '4. Quantos pavimentos teria sua edificação?'
    label_address = 'Localize'
    label_desc = 'Identifique'

    edification_type = forms.ChoiceField(label=label_edification,
                                         choices=EDIFICATION, required=True)
    number_pav = forms.IntegerField(label=label_pav,min_value=1,
                                    required=False)
    address = forms.CharField(label=label_address, required=False)
    descricao = forms.CharField(label=label_desc)

    class Meta:
        model = Terreno
        fields = ('edification_type', 'number_pav',
                  'address', 'descricao', 'geom',
                  'account')
        widgets = {'geom': forms.HiddenInput(), 'account': forms.HiddenInput()}
