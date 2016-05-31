from django.forms import ModelForm

from .models import Igreja, Departamento, Classe, Pessoa


class BaseForm(ModelForm):
    """
        Form Base para adicionar classe de estilo.
    """

    def __init__(self, *args, **kwargs):
        super(BaseForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class FormIgreja(BaseForm):
    """
        Form Igreja.
    """

    class Meta:
        model = Igreja
        fields = '__all__'


class FormDepartamento(BaseForm):
    """
        Form Departamento.
    """

    class Meta:
        model = Departamento
        fields = '__all__'


class FormClasse(BaseForm):
    """
        Form Classe.
    """

    class Meta:
        model = Classe
        fields = '__all__'


class FormPessoa(BaseForm):
    """
        Form Pessoa.
    """

    class Meta:
        model = Pessoa
        exclude = ['status']
