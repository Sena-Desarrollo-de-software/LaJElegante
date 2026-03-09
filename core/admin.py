from django.contrib import admin

AUDITORIA_FIELDSET = ('Auditoría', {
    'fields': ('created_at', 'updated_at', 'deleted_at'),
    'classes': ('collapse',),
})

AUDITORIA_READONLY = ('created_at', 'updated_at', 'deleted_at')
