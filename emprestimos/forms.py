from django import forms
from django.forms import inlineformset_factory
from django.utils import timezone
from .models import Emprestimo, ItemEmprestado, HistoricoDevolucao
from colaboradores.models import Colaborador
from equipamentos.models import Equipamento
from django.core.exceptions import ValidationError

## --- Formulário 1: O "Cabeçalho" do Empréstimo (Sem mudanças) ---

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

## --- Formulário 2: Os "Itens" do Empréstimo (Carrinho) (ATUALIZADO) ---

class ItemEmprestadoForm(forms.ModelForm):
    ##
    ## Formulário para um item individual do empréstimo.
    ##
    class Meta:
        model = ItemEmprestado
        ## (ATUALIZADO) Usa o novo nome do campo
        fields = ['equipamento', 'quantidade_emprestada'] 

    def __init__(self, *args, **kwargs):
        super(ItemEmprestadoForm, self).__init__(*args, **kwargs)
        
        self.fields['equipamento'].queryset = Equipamento.objects.filter(
            estoque_disponivel__gt=0
        ).order_by('nome')
        self.fields['equipamento'].label = "Equipamento"
        ## (ATUALIZADO) Atualiza o label do campo
        self.fields['quantidade_emprestada'].label = "Qtde. Emprestada"

    def clean_quantidade_emprestada(self):
        ## (ATUALIZADO) Valida o campo 'quantidade_emprestada'
        quantidade = self.cleaned_data.get('quantidade_emprestada')
        equipamento = self.cleaned_data.get('equipamento')

        if equipamento and quantidade:
            if quantidade <= 0:
                raise ValidationError("A quantidade deve ser pelo menos 1.")
            
            if quantidade > equipamento.estoque_disponivel:
                raise ValidationError(
                    f"Quantidade indisponível. Estoque disponível para '{equipamento.nome}': {equipamento.estoque_disponivel}"
                )
        return quantidade

## --- Formulário 3: O "FormSet" que junta tudo (ATUALIZADO) ---

ItemEmprestadoFormSet = inlineformset_factory(
    Emprestimo,          
    ItemEmprestado,      
    form=ItemEmprestadoForm, 
    ## (ATUALIZADO) Define o campo 'quantidade_emprestada'
    fields=['equipamento', 'quantidade_emprestada'],
    extra=1,             
    can_delete=True,     
    min_num=1,           
    validate_min=True,
)


## --- (NOVO) Formulário 4: Devolução Parcial de um Item ---

class DevolucaoParcialForm(forms.ModelForm):
    ##
    ## Formulário para registrar uma devolução (parcial ou total)
    ## de um ItemEmprestado, criando um registro de Histórico.
    ##
    
    # Este campo é para o usuário digitar quanto quer devolver
    quantidade_devolvida = forms.IntegerField(
        label="Quantidade a Devolver",
        min_value=1,
        widget=forms.NumberInput(attrs={'placeholder': 'Qtde.'}) # Adiciona placeholder
    )

    class Meta:
        model = HistoricoDevolucao
        ## O usuário preenche a quantidade, o status e a observação
        fields = ['quantidade_devolvida', 'status_devolucao', 'observacao']
        widgets = {
            'observacao': forms.TextInput(
                attrs={'placeholder': 'Opcional (ex: "luva rasgada")'}
            ),
        }

    def __init__(self, *args, **kwargs):
        ## (IMPORTANTE) Precisamos receber a 'instance' do ItemEmprestado
        ## para sabermos qual é a quantidade pendente.
        self.item_emprestado_instance = kwargs.pop('item_emprestado_instance', None)
        super().__init__(*args, **kwargs)
        
        self.fields['status_devolucao'].label = "Registrar como"
        
        ## (IMPORTANTE) Define a quantidade máxima permitida no campo
        if self.item_emprestado_instance:
            pendente = self.item_emprestado_instance.get_quantidade_pendente()
            self.fields['quantidade_devolvida'].max_value = pendente
            self.fields['quantidade_devolvida'].initial = pendente ## Sugere o valor máximo

    def clean_quantidade_devolvida(self):
        ## Validação final para garantir que a quantidade não
        ## seja maior do que a pendente.
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
