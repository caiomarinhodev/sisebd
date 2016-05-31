from django.forms import ModelForm

from .models import Igreja, Departamento, Classe, Pessoa


class FormIgreja(ModelForm):
    """
        Form Igreja
    """

    class Meta:
        model = Igreja
        fields = '__all__'


class FormDepartamento(ModelForm):
    """
        Form Departamento
    """

    class Meta:
        model = Departamento
        fields = '__all__'


class FormClasse(ModelForm):
    """
        Form Classe
    """

    class Meta:
        model = Classe
        fields = '__all__'


class FormPessoa(ModelForm):
    """
        Form Aluno
    """

    class Meta:
        model = Pessoa
        exclude = ['status']
