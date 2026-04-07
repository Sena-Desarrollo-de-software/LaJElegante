from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import permission_required
from django.views.decorators.http import require_http_methods, require_safe, require_POST, require_GET
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.http import HttpResponse
from weasyprint import HTML
from core.utils import ahora
from .models import Impuesto, Tarifa, Temporada
from .forms import (
    ImpuestoCreateForm,
    ImpuestoUpdateForm,
    ImpuestoDeleteForm,
    ImpuestoRestoreForm,
    TarifaForm,
    TemporadaForm,
    SoftDeleteConfirmForm,
)

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
@login_required
@permission_required("finance.view_tarifa", raise_exception=True)
@require_GET
def index_tarifa(request):
    tarifas = Tarifa.objects.select_related('temporada', 'servicio_tipo').order_by('-id')
    return render(request, 'backoffice/tarifas/tarifa_index.html', {'tarifas': tarifas})


@login_required
@permission_required("finance.view_tarifa", raise_exception=True)
@require_GET
def detail_tarifa(request, pk):
    tarifa = get_object_or_404(
        Tarifa.all_objects.select_related('temporada', 'servicio_tipo', 'created_by', 'updated_by').prefetch_related('impuestos'),
        pk=pk,
    )
    return render(request, 'backoffice/tarifas/tarifa_detail.html', {'tarifa': tarifa})


@login_required
@permission_required("finance.add_tarifa", raise_exception=True)
@require_http_methods(["GET", "POST"])
@csrf_protect
def create_tarifa(request):
    form = TarifaForm(request.POST or None)
    impuestos_disponibles = Impuesto.objects.filter(is_active=True).order_by('tipo', 'nombre')

    if request.method == "POST":
        impuestos_seleccionados = [int(pk) for pk in request.POST.getlist('impuestos') if pk.isdigit()]
    else:
        impuestos_seleccionados = []

    if request.method == "POST" and form.is_valid():
        tarifa = form.save(commit=False)
        tarifa.created_by = request.user
        tarifa.updated_by = request.user
        impuestos_ids = list(form.cleaned_data.get('impuestos', []).values_list('id', flat=True))
        tarifa.save(impuestos_ids=impuestos_ids)
        form.save_m2m()
        # Recalcular con la relación M2M ya persistida para mantener consistencia.
        tarifa.save()
        return redirect("finance:tarifa_index")

    return render(
        request,
        'backoffice/tarifas/tarifa_create.html',
        {
            'form': form,
            'impuestos_disponibles': impuestos_disponibles,
            'impuestos_seleccionados': impuestos_seleccionados,
        },
    )


@login_required
@permission_required("finance.change_tarifa", raise_exception=True)
@require_http_methods(["GET", "POST"])
@csrf_protect
def update_tarifa(request, pk):
    tarifa = get_object_or_404(Tarifa.objects.select_related('temporada'), pk=pk, is_active=True)
    form = TarifaForm(request.POST or None, instance=tarifa)
    impuestos_disponibles = Impuesto.objects.filter(is_active=True).order_by('tipo', 'nombre')

    if request.method == "POST":
        impuestos_seleccionados = [int(pk) for pk in request.POST.getlist('impuestos') if pk.isdigit()]
    else:
        impuestos_seleccionados = list(tarifa.impuestos.values_list('id', flat=True))

    if request.method == "POST" and form.is_valid():
        tarifa = form.save(commit=False)
        tarifa.updated_by = request.user
        tarifa.save()
        form.save_m2m()
        # En edición, el cálculo correcto depende de los impuestos ya actualizados.
        tarifa.save()
        return redirect("finance:tarifa_index")

    return render(
        request,
        'backoffice/tarifas/tarifa_update.html',
        {
            'form': form,
            'tarifa': tarifa,
            'impuestos_disponibles': impuestos_disponibles,
            'impuestos_seleccionados': impuestos_seleccionados,
        },
    )


@login_required
@permission_required("finance.delete_tarifa", raise_exception=True)
@require_http_methods(["GET", "POST"])
@csrf_protect
def delete_tarifa(request, pk):
    tarifa = get_object_or_404(Tarifa.objects, pk=pk, is_active=True)
    form = SoftDeleteConfirmForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        tarifa.soft_delete(user=request.user)
        return redirect("finance:tarifa_index")

    return render(request, 'backoffice/tarifas/tarifa_delete.html', {'form': form, 'tarifa': tarifa})


@login_required
@permission_required("finance.view_tarifa", raise_exception=True)
@require_GET
def trashcan_tarifa(request):
    tarifas = Tarifa.all_objects.filter(is_active=False).select_related('temporada', 'servicio_tipo').order_by('-id')
    return render(request, 'backoffice/tarifas/tarifa_trashcan.html', {'tarifas': tarifas})

# === TEMPORADA ===
@login_required
@permission_required("finance.view_temporada", raise_exception=True)
@require_GET
def index_temporada(request):
    temporadas = Temporada.objects.order_by('-fecha_inicio', '-id')
    return render(request, 'backoffice/temporadas/temporada_index.html', {'temporadas': temporadas})


@login_required
@permission_required("finance.add_temporada", raise_exception=True)
@require_http_methods(["GET", "POST"])
@csrf_protect
def create_temporada(request):
    form = TemporadaForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        temporada = form.save(commit=False)
        temporada.created_by = request.user
        temporada.updated_by = request.user
        temporada.save()
        return redirect("finance:temporada_index")

    return render(request, 'backoffice/temporadas/temporada_create.html', {'form': form})


@login_required
@permission_required("finance.change_temporada", raise_exception=True)
@require_http_methods(["GET", "POST"])
@csrf_protect
def update_temporada(request, pk):
    temporada = get_object_or_404(Temporada.objects, pk=pk, is_active=True)
    form = TemporadaForm(request.POST or None, instance=temporada)

    if request.method == "POST" and form.is_valid():
        temporada = form.save(commit=False)
        temporada.updated_by = request.user
        temporada.save()
        return redirect("finance:temporada_index")

    return render(request, 'backoffice/temporadas/temporada_update.html', {'form': form, 'temporada': temporada})


@login_required
@permission_required("finance.delete_temporada", raise_exception=True)
@require_http_methods(["GET", "POST"])
@csrf_protect
def delete_temporada(request, pk):
    temporada = get_object_or_404(Temporada.objects, pk=pk, is_active=True)
    form = SoftDeleteConfirmForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        temporada.soft_delete(user=request.user)
        return redirect("finance:temporada_index")

    return render(request, 'backoffice/temporadas/temporada_delete.html', {'form': form, 'temporada': temporada})


@login_required
@permission_required("finance.view_temporada", raise_exception=True)
@require_GET
def trashcan_temporada(request):
    temporadas = Temporada.all_objects.filter(is_active=False).order_by('-fecha_inicio', '-id')
    return render(request, 'backoffice/temporadas/temporada_trashcan.html', {'temporadas': temporadas})