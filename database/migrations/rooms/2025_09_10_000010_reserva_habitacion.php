<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    /**
     * Run the migrations.
     */
    public function up(): void
    {
        Schema::create('reserva_habitacion', function(Blueprint $table){
            $table->id('id_reserva_habitacion');
            $table->unsignedBigInteger('id_cliente');
            $table->foreign('id_cliente')
                ->references('id_cliente')->on('clientes')
                ->onDelete('restrict');

            $table->unsignedBigInteger('id_detalle_reserva_hab');
            $table->foreign('id_detalle_reserva_hab')
                ->references('id_detalle_reserva_hab')->on('detalles_reserva_habitacion')
                ->onDelete('restrict');
            $table->timestamps();
            $table->softDeletes();
       });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('reserva_habitacion');
    }
};
