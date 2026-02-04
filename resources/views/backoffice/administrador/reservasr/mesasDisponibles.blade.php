@extends('administrador.layouts.reservasr')

@section('content')
<div class="container d-flex align-items-center" style="min-height: 70vh;">
    <div class="row w-100">
        <div class="col-md-10">
            <div class="p-4 rounded shadow-sm" style="background-color:#f2f2f2;">
                <div class="row">
                    {{-- Lado izquierdo: mesas --}}
                    <div class="col-md-6">
                        <h4 class="mb-5 text-center">Mesas disponibles</h4>
                        <div class="row">
                            {{-- Mesas grandes --}}
                            <div class="col-auto d-flex flex-column gap-5 me-4 justify-content-center">
                                @foreach($mesas->where('capacidad', '>', 4)->take(2) as $mesa)
                                    <div 
                                        class="mesa-card d-flex align-items-center justify-content-center text-white fw-bold"
                                        style="height:90px; width:90px; border-radius:10px; cursor:pointer; 
                                               background-color: {{ $mesa->activo ? '#28a745' : '#dc3545' }};"
                                        onclick="mostrarInfo('{{ $mesa->id_mesa }}','{{ $mesa->numero_mesa }}','{{ $mesa->activo }}','{{ $mesa->capacidad }}')">
                                        {{ $mesa->numero_mesa }}
                                    </div>
                                @endforeach
                            </div>

                            {{-- Mesas pequeñas --}}
                            <div class="col d-flex align-items-center">
                                <div class="row row-cols-2 g-4 justify-content-center">
                                    @foreach($mesas->where('capacidad', '<=', 4) as $mesa)
                                        <div class="col d-flex justify-content-center">
                                            <div 
                                                class="mesa-card d-flex align-items-center justify-content-center text-white fw-bold"
                                                style="height:70px; width:70px; border-radius:10px; cursor:pointer; 
                                                       background-color: {{ $mesa->activo ? '#28a745' : '#dc3545' }};"
                                                onclick="mostrarInfo('{{ $mesa->id_mesa }}','{{ $mesa->numero_mesa }}','{{ $mesa->activo }}','{{ $mesa->capacidad }}')">
                                                {{ $mesa->numero_mesa }}
                                            </div>
                                        </div>
                                    @endforeach
                                </div>
                            </div>
                        </div>
                    </div>

                    {{-- Lado derecho: info mesa y formulario --}}
                    <div class="col-md-6 d-flex flex-column justify-content-center">
                        <h4 class="mb-3 text-center">Información de la mesa</h4>
                        <div id="infoMesa" class="card shadow-sm p-3" style="display:none;">
                            <h5 id="mesaNombre" class="text-center"></h5>
                            <p><strong>Capacidad:</strong> <span id="mesaCapacidad"></span> personas</p>

                            <form action="{{ route('reservasr.storeMesa') }}" method="POST">
                                @csrf
                                <input type="hidden" name="id_mesa" id="mesaId">

                                <div class="mb-3">
                                    <label for="fecha" class="form-label">Fecha:</label>
                                    <input type="date" name="fecha" id="fecha" class="form-control" required>
                                </div>

                                <div class="mb-3">
                                    <label for="hora" class="form-label">Hora:</label>
                                    <input type="time" name="hora" id="hora" class="form-control" required>
                                </div>

                                {{-- Datos opcionales de cliente registrado --}}
                                <h5 class="mt-4">Cliente registrado (opcional)</h5>
                                <div class="mb-3">
                                    <label for="nombre_cliente" class="form-label">Nombre:</label>
                                    <input type="text" name="nombre_cliente" id="nombre_cliente" class="form-control" placeholder="Ej: julian">
                                </div>
                                <div class="mb-3">
                                    <label for="correo_cliente" class="form-label">Correo electrónico:</label>
                                    <input type="email" name="correo_cliente" id="correo_cliente" class="form-control" placeholder="Ej: jsse0706@gmail.com">
                                </div>

                                <div class="text-center">
                                    <button type="submit" class="btn btn-primary">Reservar mesa</button>
                                </div>
                            </form>
                        </div>

                        {{-- Mensajes de éxito/error --}}
                        @if(session('success'))
                            <div class="alert alert-success mt-3">{{ session('success') }}</div>
                        @endif
                        @if(session('error'))
                            <div class="alert alert-danger mt-3">{{ session('error') }}</div>
                        @endif
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

<script>
function mostrarInfo(id, numero, activo, capacidad) {
    document.getElementById('infoMesa').style.display = 'block';
    document.getElementById('mesaNombre').innerText = 'Mesa ' + numero;
    document.getElementById('mesaCapacidad').innerText = capacidad;
    document.getElementById('mesaId').value = id;
}
</script>
@endsection
