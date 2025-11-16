from django.db import models
from django.utils import timezone

class Equipamento(models.Model):
    ##
    ## Modelo para cadastrar os Equipamentos de Proteção Individual (EPIs).
    ##
    
    CATEGORIAS_CHOICES = [
        ('CABECA', 'Proteção da Cabeça'),
        ('OLHOS', 'Proteção Ocular/Facial'),
        ('AUDITIVA', 'Proteção Auditiva'),
        ('RESPIRATORIA', 'Proteção Respiratória'),
        ('TRONCO', 'Proteção do Tronco'),
        ('MEMBROS_SUP', 'Proteção Membros Superiores (Mãos)'),
        ('MEMBROS_INF', 'Proteção Membros Inferiores (Pés)'),
        ('CORPO_INTEIRO', 'Proteção Corpo Inteiro'),
        ('OUTRO', 'Outro'),
    ]

    # --- Campos Principais ---
    # (CORRIGIDO) Adicionado unique=True
    nome = models.CharField(
        max_length=100, 
        help_text="Nome do equipamento (ex: Capacete, Luva de Raspa)",
        unique=True
    )
    categoria = models.CharField(max_length=20, choices=CATEGORIAS_CHOICES, default='OUTRO')
    
    ca = models.CharField(
        max_length=20, 
        verbose_name="Certificado de Aprovação (C.A.)", 
        blank=True, 
        null=True, 
        help_text="Número do C.A. do equipamento (se aplicável)"
    )
    
    # --- Campos de Estoque ---
    estoque_total = models.PositiveIntegerField(
        default=1, # (CORRIGIDO) Default agora é 1
        help_text="Quantidade total deste item comprada pela empresa."
    )
    estoque_disponivel = models.PositiveIntegerField(
        default=0, 
        help_text="Quantidade disponível no estoque para empréstimo."
    )
    
    # --- Campos de Controle ---
    data_cadastro = models.DateTimeField(auto_now_add=True, verbose_name="Data de Cadastro")
    data_ultima_atualizacao = models.DateTimeField(auto_now=True, verbose_name="Última Atualização")
    
    def __str__(self):
        return f"{self.nome} (C.A.: {self.ca or 'N/A'})"

    def save(self, *args, **kwargs):
        # Garante que, ao criar um novo equipamento (sem ID),
        # o estoque disponível seja igual ao estoque total.
        if not self.id:
            self.estoque_disponivel = self.estoque_total
        super(Equipamento, self).save(*args, **kwargs)