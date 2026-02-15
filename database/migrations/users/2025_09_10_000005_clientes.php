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
        Schema::create('clientes', function (Blueprint $table){
        $table->id('id_cliente');
        $table->unsignedBigInteger('id_tipo_cliente');
        $table->foreign('id_tipo_cliente')
          ->references('id_tipo_cliente')->on('tipo_cliente')
          ->onDelete('restrict');
        $table->string('email_info');
        $table->string('contrasena');
        $table->string('nombre');
        $table->string('apellido');
        $table->enum('saludo',['MR','MS','MX']);
        $table->string('numero_telefono',20);
        $table->string('prefijo_telefono',5);
        $table->enum('estado',['activo','inactivo']);
        $table->timestamps();
        $table->softDeletes();
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('clientes');
    }
};
