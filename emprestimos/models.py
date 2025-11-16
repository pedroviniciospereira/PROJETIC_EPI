from django.db import models
from django.utils import timezone
from colaboradores.models import Colaborador
from equipamentos.models import Equipamento
from django.core.exceptions import ValidationError
from django.db.models import Sum # (NOVO) Para somar as devoluções

# Create your models here.

class Emprestimo(models.Model):
    ##
    ## Modelo "Mestre" que representa uma transação de empréstimo.
    ## (O "cabeçalho" do recibo)
    ##
    
    STATUS_CHOICES = [
        ('ATIVO', 'Ativo'),        # Empréstimo em andamento
        ('DEVOLVIDO', 'Devolvido'),  # Colaborador já devolveu tudo
        ('ATRASADO', 'Atrasado'),    # Passou da data de devolução
    ]

    colaborador = models.ForeignKey(
        Colaborador, 
        on_delete=models.PROTECT, # Impede excluir colaborador com empréstimo ativo
        related_name="emprestimos"
    )
    data_emprestimo = models.DateTimeField(
        auto_now_add=True, 
        verbose_name="Data do Empréstimo"
    )
    data_prevista_devolucao = models.DateField(
        verbose_name="Data Prevista para Devolução"
    )
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='ATIVO'
    )
    observacao = models.TextField(
        blank=True, 
        null=True, 
        verbose_name="Observação"
    )
    
    def __str__(self):
        return f"Empréstimo #{self.id} - {self.colaborador.nome_completo}"

    def clean(self):
        # Garante que a data de devolução não seja no passado
        if self.data_prevista_devolucao < timezone.now().date():
            raise ValidationError("A data de devolução não pode ser no passado.")


class ItemEmprestado(models.Model):
    ##
    ## (MODIFICADO)
    ## Modelo "Detalhe" que representa cada item dentro de um Empréstimo.
    ## (Ex: "10 x Luvas de Raspa")
    ##
    
    # (MODIFICADO) Status simplificado. O detalhe fica no Histórico.
    STATUS_ITEM_CHOICES = [
        ('PENDENTE', 'Pendente'),   # O colaborador ainda deve itens
        ('CONCLUIDO', 'Concluído'), # Todos os itens foram processados
    ]

    emprestimo = models.ForeignKey(
        Emprestimo, 
        on_delete=models.CASCADE,
        related_name="itens_emprestados"
    )
    equipamento = models.ForeignKey(
        Equipamento, 
        on_delete=models.PROTECT,
        related_name="emprestimos_itens"
    )
    # (MODIFICADO) Renomeado para clareza
    quantidade_emprestada = models.PositiveIntegerField(default=1) 
    
    status_item = models.CharField(
        max_length=20, 
        choices=STATUS_ITEM_CHOICES, 
        default='PENDENTE',
        verbose_name="Status do Item"
    )
    
    # (REMOVIDO) Os campos data_devolucao_item e status_item (EM_USO, DEVOLVIDO)
    # agora pertencem ao novo modelo HistoricoDevolucao.

    def __str__(self):
        return f"{self.quantidade_emprestada}x {self.equipamento.nome} (Empréstimo #{self.emprestimo.id})"
        
    def get_quantidade_devolvida_total(self):
        ##
        ## (NOVO) Soma todas as quantidades nos registros de histórico.
        ##
        # Acessa o 'historico_devolucoes' (related_name do novo modelo)
        # e soma o campo 'quantidade_devolvida'
        soma = self.historico_devolucoes.aggregate(
            total=Sum('quantidade_devolvida')
        )['total']
        return soma or 0 # Retorna 0 se for None
        
    def get_quantidade_pendente(self):
        ##
        ## (NOVO) Calcula o que ainda falta devolver.
        ##
        return self.quantidade_emprestada - self.get_quantidade_devolvida_total()


class HistoricoDevolucao(models.Model):
    ##
    ## (NOVO MODELO)
    ## Registra cada ação de devolução (parcial ou total).
    ## (Ex: "5x Devolvido", "2x Danificado")
    ##
    STATUS_DEVOLUCAO_CHOICES = [
        ('DEVOLVIDO', 'Devolvido'),
        ('DANIFICADO', 'Danificado'),
        ('PERDIDO', 'Perdido'),
    ]

    item_emprestado = models.ForeignKey(
        ItemEmprestado,
        on_delete=models.CASCADE,
        related_name="historico_devolucoes" # Como ItemEmprestado acessa este modelo
    )
    quantidade_devolvida = models.PositiveIntegerField()
    data_devolucao = models.DateTimeField(auto_now_add=True)
    status_devolucao = models.CharField(
        max_length=20,
        choices=STATUS_DEVOLUCAO_CHOICES
    )
    observacao = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.quantidade_devolvida}x {self.get_status_devolucao_display()} em {self.data_devolucao.strftime('%d/%m/%Y')}"
