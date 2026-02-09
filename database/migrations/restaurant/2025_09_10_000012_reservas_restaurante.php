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
            Schema::create('reservas_restaurante', function (Blueprint $table) {
                $table->id('id_reserva');
                $table->unsignedBigInteger('id_cliente');
                $table->unsignedBigInteger('id_mesa');
                $table->date('fecha_reserva');
                $table->time('hora_reserva');
                $table->tinyInteger('numero_personas');
                $table->enum('estado_reserva', ['pendiente','confirmada','cancelada'])->default('pendiente');
                $table->boolean('activo')->default(true);
                $table->timestamps();

                $table->foreign('id_cliente')->references('id_cliente')->on('clientes')->onDelete('cascade');
                $table->foreign('id_mesa')->references('id_mesa')->on('mesas')->onDelete('cascade');
            });
        }


            /**
             * Reverse the migrations.
             */
            public function down(): void
            {
                Schema::dropIfExists('reservas_restaurante');
            }
        };
