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
        Schema::create('habitaciones', function(Blueprint $table){
            $table->id('id_habitacion');
            $table->unsignedBigInteger('id_tipo_habitacion');
            $table->foreign('id_tipo_habitacion')
                ->references('id_tipo_habitacion')->on('tipo_habitacion')
                ->onDelete('restrict');
            $table->integer('numero_habitacion')->unique();
            $table->enum('estado_habitacion',['en servicio','mantenimiento','ocupada'])
                ->default('en servicio');
            $table->timestamps();
            $table->softDeletes();
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('habitaciones');
    }
};
