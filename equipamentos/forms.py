from django import forms
from .models import Equipamento

class EquipamentoForm(forms.ModelForm):
    ##
    ## Formulário para criar e atualizar Equipamentos (EPIs).
    ##

    class Meta:
        model = Equipamento
        fields = [
            'nome', 
            'categoria', 
            'ca', 
            'estoque_total', 
            'estoque_disponivel'
        ]
        
        widgets = {
            'nome': forms.TextInput(attrs={
                'id': 'nome_equipamento',
                'placeholder': 'Ex: Capacete de Segurança V-Gard'
            }),
            'categoria': forms.Select(attrs={
                'id': 'categoria',
            }),
            'ca': forms.TextInput(attrs={
                'id': 'ca',
                'placeholder': 'Ex: 498 (somente números)'
            }),
            'estoque_total': forms.NumberInput(attrs={
                'id': 'estoque_total',
                'min': '1', # (CORRIGIDO) Mínimo é 1
                'placeholder': '1'
            }),
            'estoque_disponivel': forms.NumberInput(attrs={
                'id': 'estoque_disponivel',
                'min': '0',
                'placeholder': '0'
            }),
        }
        
        error_messages = {
            # (NOVO) Mensagem de erro para nome repetido
            'nome': {
                'unique': "Já existe um equipamento cadastrado com este nome.",
            },
            'ca': {
                'unique': "Já existe um equipamento cadastrado com este número de C.A.",
            }
        }

    def __init__(self, *args, **kwargs):
        super(EquipamentoForm, self).__init__(*args, **kwargs)
        
        if self.instance and self.instance.pk:
            self.fields['estoque_disponivel'].disabled = True

    def clean_ca(self):
        ca = self.cleaned_data.get('ca')
        if ca and not ca.isdigit():
            raise forms.ValidationError("O C.A. deve conter apenas números.")
        return ca
        
    def clean_estoque_total(self):
        # (NOVO) Validação extra para garantir > 0
        total = self.cleaned_data.get('estoque_total', 0)
        if total <= 0:
            raise forms.ValidationError("O estoque total deve ser pelo menos 1.")
        return total

    def clean_estoque_disponivel(self):
        if self.fields['estoque_disponivel'].disabled:
            return self.instance.estoque_disponivel

        total = self.cleaned_data.get('estoque_total', 0)
        disponivel = self.cleaned_data.get('estoque_disponivel', 0)
        
        if disponivel > total:
            raise forms.ValidationError(
                "O estoque disponível não pode ser maior que o estoque total."
            )
        return disponivel

    def clean(self):
        cleaned_data = super().clean()
        
        if not self.instance.pk:
            total = cleaned_data.get('estoque_total')
            cleaned_data['estoque_disponivel'] = total
            
        return cleaned_data