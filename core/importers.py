import pandas as pd
from django.db import transaction
from django.contrib import messages

class BaseImporter:
    """
    Importador genérico que utiliza un ModelForm para validar y guardar cada fila.
    Subclases deben definir:
        - form_class: ModelForm correspondiente
        - field_mapping: dict {columna_csv: nombre_campo_form}
        - unique_field: campo que identifica registros existentes (opcional)
        - defaults: dict {campo: valor_default}
    """
    form_class = None
    field_mapping = {}
    unique_field = None
    defaults = {}

    def __init__(self, request, update_existing=False):
        self.request = request
        self.user = request.user
        self.update_existing = update_existing
        self.results = {
            'created': 0,
            'updated': 0,
            'errors': [],
            'warnings': [],
        }

    def read_file(self, uploaded_file):
        """Lee CSV/Excel y devuelve DataFrame."""
        ext = uploaded_file.name.split('.')[-1].lower()
        if ext == 'csv':
            try:
                return pd.read_csv(uploaded_file, encoding='utf-8')
            except UnicodeDecodeError:
                uploaded_file.seek(0)
                return pd.read_csv(uploaded_file, encoding='latin-1')
        else:
            return pd.read_excel(uploaded_file)

    def validate_columns(self, df):
        required_columns = list(self.field_mapping.keys())
        missing = [col for col in required_columns if col not in df.columns]
        if missing:
            self.results['errors'].append(
                f"Columnas requeridas faltantes: {', '.join(missing)}. "
                f"Encontradas: {', '.join(df.columns)}"
            )
            return False
        return True

    def row_to_form_data(self, row, row_idx):
        data = {}
        for csv_col, form_field in self.field_mapping.items():
            if csv_col in row:
                value = row[csv_col]
                if pd.isna(value):
                    value = None
                data[form_field] = value
        # Aplicar defaults
        for field, default in self.defaults.items():
            if field not in data or data[field] is None:
                data[field] = default
        return data

    def get_instance(self, data):
        if not self.unique_field:
            return None
        unique_value = data.get(self.unique_field)
        if unique_value:
            try:
                return self.form_class.Meta.model.objects.get(**{self.unique_field: unique_value})
            except self.form_class.Meta.model.DoesNotExist:
                pass
        return None

    def get_form(self, data, instance=None):
        if instance and self.update_existing:
            return self.form_class(data, instance=instance)
        return self.form_class(data)

    def apply_audit_fields(self, form, instance):
        if hasattr(form, 'fields') and 'created_by' in form.fields:
            if not instance:
                form.instance.created_by = self.user
            form.instance.updated_by = self.user

    def process_row(self, data, row_idx):
        instance = self.get_instance(data)
        if instance and not self.update_existing:
            self.results['errors'].append(
                f"Fila {row_idx}: {instance._meta.model.__name__} con "
                f"{self.unique_field}={getattr(instance, self.unique_field)} ya existe"
            )
            return

        form = self.get_form(data, instance)
        self.apply_audit_fields(form, instance)

        if form.is_valid():
            form.save()
            if instance and self.update_existing:
                self.results['updated'] += 1
            else:
                self.results['created'] += 1
        else:
            for field, errors in form.errors.items():
                for err in errors:
                    self.results['errors'].append(f"Fila {row_idx} - {field}: {err}")

    def run(self, uploaded_file):
        if not uploaded_file:
            self.results['errors'].append("No se ha seleccionado ningún archivo")
            return

        try:
            df = self.read_file(uploaded_file)
        except Exception as e:
            self.results['errors'].append(f"Error al leer archivo: {str(e)}")
            return

        df.columns = df.columns.str.strip()
        if not self.validate_columns(df):
            return

        for idx, row in df.iterrows():
            try:
                with transaction.atomic():
                    data = self.row_to_form_data(row, idx+2)
                    self.process_row(data, idx+2)
            except Exception as e:
                self.results['errors'].append(f"Fila {idx+2}: {str(e)}")

    def add_messages(self):
        if self.results['created']:
            messages.success(self.request, f"{self.results['created']} registros creados")
        if self.results['updated']:
            messages.info(self.request, f"{self.results['updated']} registros actualizados")
        if self.results['warnings']:
            for warn in self.results['warnings'][:5]:
                messages.warning(self.request, warn)
        if self.results['errors']:
            for err in self.results['errors'][:5]:
                messages.error(self.request, err)
            self.request.session['import_errores'] = self.results['errors']