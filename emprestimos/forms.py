from django import forms
from django.forms import inlineformset_factory
from django.utils import timezone
from .models import Emprestimo, ItemEmprestado, HistoricoDevolucao
from colaboradores.models import Colaborador
from equipamentos.models import Equipamento
from django.core.exceptions import ValidationError

## --- Formulário 1: O "Cabeçalho" do Empréstimo ---

class EmprestimoForm(forms.ModelForm):
    ##
    ## Formulário principal para criar a transação de Empréstimo.
    ##
    colaborador = forms.ModelChoiceField(
        queryset=Colaborador.objects.filter(status='Ativo').order_by('nome_completo'),
        label="Colaborador"
    )

    class Meta:
        model = Emprestimo
        fields = ['colaborador', 'data_prevista_devolucao', 'observacao']
        widgets = {
            'data_prevista_devolucao': forms.DateInput(
                attrs={'type': 'date', 'class': 'form-control'},
                format='%Y-%m-%d'
            ),
            'observacao': forms.Textarea(
                attrs={'rows': 3, 'placeholder': 'Alguma observação sobre o empréstimo? (opcional)'}
            ),
        }

    def clean_data_prevista_devolucao(self):
        data = self.cleaned_data.get('data_prevista_devolucao')
        if data and data < timezone.now().date():
            raise ValidationError("A data de devolução não pode ser no passado.")
        return data

## --- Formulário 2: Os "Itens" do Empréstimo (Carrinho) ---

class ItemEmprestadoForm(forms.ModelForm):
    ##
    ## Formulário para um item individual do empréstimo.
    ##
    class Meta:
        model = ItemEmprestado
        fields = ['equipamento', 'quantidade_emprestada'] 

    def __init__(self, *args, **kwargs):
        super(ItemEmprestadoForm, self).__init__(*args, **kwargs)
        
        self.fields['equipamento'].queryset = Equipamento.objects.filter(
            estoque_disponivel__gt=0
        ).order_by('nome')
        self.fields['equipamento'].label = "Equipamento"
        self.fields['quantidade_emprestada'].label = "Qtde. Emprestada"

    def clean(self):
        cleaned_data = super().clean()
        equipamento = cleaned_data.get('equipamento')
        quantidade = cleaned_data.get('quantidade_emprestada')

        # Verifica se 'quantidade' foi preenchida (mesmo que seja 0)
        # Usamos 'is not None' porque 0 no Python conta como False
        tem_quantidade = quantidade is not None
        tem_equipamento = bool(equipamento)

        # Se preencheu qualquer um dos dois campos, valida a linha inteira
        if tem_equipamento or tem_quantidade:
            
            # Erro 1: Tem quantidade (ex: 1 ou 0), mas não escolheu o equipamento
            if tem_quantidade and not tem_equipamento:
                self.add_error('equipamento', "Selecione um equipamento.")

            # Erro 2: Tem equipamento, mas a quantidade está vazia
            if tem_equipamento and not tem_quantidade:
                self.add_error('quantidade_emprestada', "Informe a quantidade.")

            # Erro 3: Quantidade é 0 ou negativa
            if tem_quantidade and quantidade <= 0:
                self.add_error('quantidade_emprestada', "A quantidade deve ser pelo menos 1.")
            
            # Erro 4: Verifica estoque (apenas se tudo o resto estiver ok e qtd > 0)
            elif tem_equipamento and tem_quantidade and quantidade > 0:
                if quantidade > equipamento.estoque_disponivel:
                    self.add_error(
                        'quantidade_emprestada', 
                        f"Estoque insuficiente. Disponível para '{equipamento.nome}': {equipamento.estoque_disponivel}"
                    )

        return cleaned_data

## --- Formulário 3: O "FormSet" que junta tudo ---

ItemEmprestadoFormSet = inlineformset_factory(
    Emprestimo,          
    ItemEmprestado,      
    form=ItemEmprestadoForm, 
    fields=['equipamento', 'quantidade_emprestada'],
    extra=1,             
    can_delete=True,     
    min_num=1,           
    validate_min=True,
)


## --- Formulário 4: Devolução Parcial de um Item ---

class DevolucaoParcialForm(forms.ModelForm):
    ##
    ## Formulário para registrar uma devolução (parcial ou total)
    ## de um ItemEmprestado, criando um registro de Histórico.
    ##
    
    # Este campo é para o usuário digitar quanto quer devolver
    quantidade_devolvida = forms.IntegerField(
        label="Quantidade a Devolver",
        min_value=1,
        widget=forms.NumberInput(attrs={'placeholder': 'Qtde.'})
    )

    class Meta:
        model = HistoricoDevolucao
        fields = ['quantidade_devolvida', 'status_devolucao', 'observacao']
        widgets = {
            'observacao': forms.TextInput(
                attrs={'placeholder': 'Opcional (ex: "luva rasgada")'}
            ),
        }

    def __init__(self, *args, **kwargs):
        self.item_emprestado_instance = kwargs.pop('item_emprestado_instance', None)
        super().__init__(*args, **kwargs)
        
        self.fields['status_devolucao'].label = "Registrar como"
        
        if self.item_emprestado_instance:
            pendente = self.item_emprestado_instance.get_quantidade_pendente()
            self.fields['quantidade_devolvida'].max_value = pendente
            self.fields['quantidade_devolvida'].initial = pendente

    def clean_quantidade_devolvida(self):
        quantidade = self.cleaned_data.get('quantidade_devolvida')
        
        if not self.item_emprestado_instance:
            raise ValidationError("Erro: Item de empréstimo não encontrado.")
            
        pendente = self.item_emprestado_instance.get_quantidade_pendente()
        
        if quantidade <= 0:
             raise ValidationError("A quantidade deve ser maior que zero.")

        if quantidade > pendente:
            raise ValidationError(
                f"A quantidade a devolver não pode ser maior que a quantidade pendente ({pendente})."
            )
        return quantidade