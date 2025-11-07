<template>
  <section class="stats container">
    <div class="stat">
      <div class="big">98%</div>
      <div class="small-title">Usuarios Satisfechos</div>
      <p class="desc">La mayoría de los ciudadanos valora la transparencia, facilidad de uso y confidencialidad del sistema.</p>
    </div>

    <div class="stat">
      <div class="big">5+</div>
      <div class="small-title">Años de Servicio a la Ciudadanía</div>
      <p class="desc">Más de un lustro fortaleciendo la participación ciudadana y la rendición de cuentas en el sector público.</p>
    </div>

    <div class="stat">
      <div class="big">5000+</div>
      <div class="small-title">Denuncias y Quejas Gestionadas</div>
      <p class="desc">Miles de reportes han sido tramitados con eficacia, garantizando respuestas claras y procesos justos.</p>
    </div>
  </section>
</template>

<script setup>
</script>

<style scoped>
.stats {
  display:flex;
  flex-wrap: wrap; /* permite varias filas */
  gap: 200px; /* separadas un poco más */
  margin-top: 50px;
  margin-bottom: 30px;
  align-items:flex-start;
  justify-content: center; /* centra el grupo de tarjetas */
  padding: 32px 30px 26px; /* más aire vertical */
}
.stat {
  flex: 0 1 380px; /* ligeramente más anchas para abrir espacios */
  min-width: 430px;
  background: linear-gradient(180deg, #f3f5f8 0%, #eef1f5 100%);
  border-radius: 16px;
  box-shadow: 0 8px 20px rgba(16,24,40,.08), 0 2px 6px rgba(16,24,40,.06);
  padding: 18px 20px 22px;
  position: relative;
  overflow: hidden;
}
.stat::after{
  content: "";
  display: block;
  height: 3px;
  width: 28%;
  background: linear-gradient(90deg, #4dffc1, #1a73e8);
  border-radius: 999px;
  margin-top: 12px;
}
.big {
  font-size: clamp(2.6rem, 4.6vw, 3.4rem);
  font-weight:800;
}
.small-title {
  font-weight:800;
  margin-top:8px;
  font-size: clamp(1.1rem, 1.6vw, 1.25rem);
}
.desc {
  margin-top:10px;
  color: #444;
  font-size: clamp(1.02rem, 1.3vw, 1.12rem);
}
@media (max-width: 900px){
  .stats { flex-direction: column; gap: 24px; padding-top: 20px; padding-bottom: 16px; align-items: stretch; justify-content: flex-start; }
  .stat { flex: 1 1 100%; min-width: 0; }
}
</style>
