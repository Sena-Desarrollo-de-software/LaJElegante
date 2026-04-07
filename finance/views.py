from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import permission_required
from django.views.decorators.http import require_http_methods, require_safe, require_POST, require_GET
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.http import HttpResponse
from weasyprint import HTML
from core.utils import ahora
from .models import Impuesto
from .forms import ImpuestoCreateForm, ImpuestoUpdateForm, ImpuestoDeleteForm, ImpuestoRestoreForm

IMPUESTO_INDEX = "finance:impuesto_index"

# === IMPUESTO ===
def filtrar_impuestos(request, queryset=None):
    if queryset is None:
        queryset = Impuesto.objects.all()

    nombre = request.GET.get("nombre")
    tipo = request.GET.get("tipo")
    estado = request.GET.get("estado")

    if nombre:
        queryset = queryset.filter(nombre__icontains=nombre)

    if tipo:
        queryset = queryset.filter(tipo=tipo)

    if estado == "activo":
        queryset = queryset.filter(is_active=True)
    elif estado == "archivado":
        queryset = queryset.filter(is_active=False)

    return queryset

@login_required
def generar_pdf_impuestos(request, impuestos, filtros):
    context = {
        'impuestos': impuestos,
        'filtros': filtros,
        'total_registros': impuestos.count(),
        'usuario': request.user,
        'fecha_exportacion': ahora(),
    }
    html_string = render_to_string('backoffice/impuestos/impuesto_pdf.html', context)
    pdf = HTML(string=html_string).write_pdf()
    return pdf

@login_required
@permission_required("finance.view_impuesto", raise_exception=True)
@require_safe
def index_impuesto(request):
    impuestos = filtrar_impuestos(request)

    if request.GET.get('export') == 'pdf':
        context = {
            'impuestos': impuestos,
            'filtros': request.GET,
            'total_registros': impuestos.count(),
            'usuario': request.user,
            'fecha_exportacion': ahora(),
        }
        html_string = render_to_string('backoffice/impuestos/impuesto_pdf.html', context)
        pdf = HTML(string=html_string).write_pdf()
        
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = f"impuestos_{ahora().strftime('%Y%m%d_%H%M%S')}.pdf"
        response['Content-Disposition'] = f'inline; filename={filename}'
        return response

    return render(request, "backoffice/impuestos/impuesto_index.html", {
        "impuestos": impuestos,
        "filtros": request.GET
    })

@login_required
@permission_required("finance.add_impuesto", raise_exception=True)
@require_http_methods(["GET", "POST"])
@csrf_protect
def create_impuesto(request):
    form = ImpuestoCreateForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        impuesto = form.save(commit=False)
        impuesto.created_by = request.user
        impuesto.updated_by = request.user
        impuesto.save()
        return redirect(IMPUESTO_INDEX)

    return render(request, "backoffice/impuestos/impuesto_create.html", {"form": form})


@login_required
@permission_required("finance.change_impuesto", raise_exception=True)
@require_http_methods(["GET", "POST"])
@csrf_protect
def update_impuesto(request, pk):
    impuesto = get_object_or_404(Impuesto.objects, pk=pk, is_active=True)
    form = ImpuestoUpdateForm(request.POST or None, instance=impuesto)

    if request.method == "POST" and form.is_valid():
        impuesto = form.save(commit=False)
        impuesto.updated_by = request.user
        impuesto.save()
        return redirect(IMPUESTO_INDEX)

    return render(request, "backoffice/impuestos/impuesto_update.html", {
        "form": form,
        "impuesto": impuesto
    })


@login_required
@permission_required("finance.delete_impuesto", raise_exception=True)
@require_http_methods(["GET", "POST"])
@csrf_protect
def delete_impuesto(request, pk):
    impuesto = get_object_or_404(Impuesto.objects, pk=pk, is_active=True)
    form = ImpuestoDeleteForm(request.POST or None, impuesto=impuesto)

    if request.method == "POST" and form.is_valid():
        impuesto.is_active = False
        impuesto.updated_by = request.user
        impuesto.save()
        return redirect(IMPUESTO_INDEX)

    return render(request, "backoffice/impuestos/impuesto_delete.html", {
        "form": form,
        "impuesto": impuesto
    })


@login_required
@permission_required("finance.view_impuesto", raise_exception=True)
@require_safe
def trashcan_impuesto(request):
    impuestos = Impuesto.all_objects.filter(is_active=False)
    return render(request, "backoffice/impuestos/impuesto_trashcan.html", {"impuestos": impuestos})


@login_required
@permission_required("finance.change_impuesto", raise_exception=True)
@require_http_methods(["GET", "POST"])
@csrf_protect
def restore_impuesto(request, pk):
    impuesto = get_object_or_404(Impuesto.all_objects, pk=pk, is_active=False)
    form = ImpuestoRestoreForm(request.POST or None, impuesto=impuesto)

    if request.method == "POST" and form.is_valid():
        impuesto.is_active = True
        impuesto.updated_by = request.user
        impuesto.save()
        return redirect("finance:impuesto_trashcan")

    return render(request, "backoffice/impuestos/impuesto_restore.html", {
        "form": form,
        "impuesto": impuesto
    })

@login_required
@permission_required("rooms.add_reservahabitacion", raise_exception=True)
def import_impuesto(request):
    context = {
        'title': 'Importar Impuestos',
        'subtitle': 'Carga masiva desde archivo CSV/Excel',
        'is_staff': request.user.is_staff,
        'datawizard_url': '/admin/sources/filesource/add/' if request.user.is_staff else None,
    }

    return render(
        request,
        'backoffice/impuestos/impuesto_import.html',
        context
    )
# === TARIFA ===
@require_GET
def index_tarifa(request):
    return render(request,'backoffice/tarifas/tarifa_index.html')

@require_POST
def create_tarifa(request):
    return render(request,'backoffice/tarifas/tarifa_create.html')

@require_http_methods(['POST','GET'])
def update_tarifa(request):
    return render(request,'backoffice/tarifas/tarifa_update.html')

@require_http_methods(['POST','GET'])
def delete_tarifa(request):
    return render(request, 'backoffice/tarifas/tarifa_delete.html')

@require_http_methods(['POST','GET'])
def trashcan_tarifa(request):
    return render(request,'backoffice/tarifas/tarifa_trashcan.html')

# === TEMPORADA ===
@require_GET
def index_temporada(request):
    return render(request,'backoffice/temporadas/temporada_index.html')

@require_POST
def create_temporada(request):
    return render(request,'backoffice/temporada/temporada_create.html')

@require_http_methods(['POST','GET'])
def update_temporada(request):
    return render(request,'backoffice/temporadas/temporada_update.html')

@require_http_methods(['POST','GET'])
def delete_temporada(request):
    return render(request, 'backoffice/temporadas/temporada_delete.html')

@require_http_methods(['POST','GET'])
def trashcan_temporada(request):
    return render(request,'backoffice/temporadas/temporada_trashcan.html')