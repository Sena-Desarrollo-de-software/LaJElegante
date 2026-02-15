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
        Schema::create('detalles_reserva_habitacion', function(Blueprint $table){
            $table->id('id_detalle_reserva_hab');
            $table->unsignedBigInteger('id_habitacion');
            $table->foreign('id_habitacion')
                ->references('id_habitacion')->on('habitaciones')
                ->onDelete('restrict');
            $table->date('fecha_inicio');
            $table->date('fecha_fin');
            $table->tinyInteger('cantidad_personas');
            $table->tinyInteger('noches');
            $table->decimal('precio_noche', 10, 2);
            $table->decimal('descuento_aplicado', 5, 2)->default(0);
            $table->decimal('recargo_aplicado', 5, 2)->default(0);
            $table->decimal('precio_reserva', 10, 2);       
            $table->text('observaciones')->nullable();
            $table->timestamps();
            $table->softDeletes();
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('detalles_reserva_habitacion');
    }
};
