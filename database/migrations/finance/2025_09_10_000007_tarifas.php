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
        Schema::create('tarifas', function(Blueprint $table){
            $table->id('id_tarifa');
            $table->decimal('tarifa_fija', 10, 2);
            $table->decimal('precio_final', 10, 2)->default(0.0);
            $table->enum('estado', ['vigente','inactiva'])->default('vigente');
            $table->unsignedBigInteger('id_tipo_habitacion');
            $table->foreign('id_tipo_habitacion')
                ->references('id_tipo_habitacion')->on('tipo_habitacion')
                ->onDelete('cascade');
            $table->unsignedBigInteger('id_temporada'); 
            $table->foreign('id_temporada')
                ->references('id_temporada')
                ->on('temporadas')
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
        Schema::dropIfExists('tarifas');
    }
};
