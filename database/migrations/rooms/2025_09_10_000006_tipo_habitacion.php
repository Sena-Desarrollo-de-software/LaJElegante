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
        Schema::create('tipo_habitacion', function (Blueprint $table) {
            $table->id('id_tipo_habitacion');
            $table->enum('nombre_tipo', ['familiar', 'pareja', 'basica', 'especial']);
            $table->string('descripcion', 500)->nullable();
            $table->tinyInteger('capacidad_maxima');
            $table->timestamps();
            $table->softDeletes();
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('tipo_habitacion');
    }
};
