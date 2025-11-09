<template>
  <section class="info container">
    <!-- Bloque 1: Título a la izquierda, información a la derecha -->
    <div class="info-block title-left">
      <h2 class="title">Un Proceso Rápido, Seguro y Transparente</h2>
      <div class="text">
        <p>Presentar una queja o denuncia nunca había sido tan sencillo. Nuestro sistema digital te permite reportar abusos o irregularidades en minutos, desde cualquier lugar y de forma totalmente confidencial. Cada reporte genera un radicado automático y seguimiento en línea, garantizando transparencia y trazabilidad en cada paso.</p>
        <router-link to="/dashboard" class="link">Haz tu denuncia</router-link>
      </div>
    </div>

    <!-- Bloque 2: Título a la derecha, información a la izquierda -->
    <div class="info-block title-right">
      <h2 class="title">Seguimiento en Tiempo Real</h2>
      <div class="text">
        <p>Centralizamos el acceso a múltiples organismos gubernamentales para que gestiones tus denuncias de forma ágil, segura y totalmente digital. Todo en un mismo espacio, con resultados más rápidos y claros.</p>
        <router-link to="/dashboard" class="link">Haz tu denuncia</router-link>
      </div>
    </div>

    <!-- Bloque 3: Título a la izquierda, información a la derecha -->
    <div class="info-block title-left">
      <h2 class="title">Accede fácilmente al historial de tus reportes</h2>
      <div class="text">
        <p>Revisa los avances de cada caso y recibe notificaciones sobre nuevas actualizaciones. Nuestro sistema te brinda total transparencia y control durante todo el proceso para que siempre sepas en qué etapa se encuentra tu denuncia.</p>
        <router-link to="/dashboard" class="link">Haz tu denuncia</router-link>
      </div>
    </div>
  </section>
</template>

<script setup>
</script>

<style scoped>
.info { padding: 48px 30px 64px; margin: 0 auto; }
.info-block {
  display: flex;
  align-items: flex-start;
  justify-content: center;
  gap: 18rem;
  margin: 0 0 96px;
}
/* Colocación por variante */
.info-block.title-left  { flex-direction: row; }
.info-block.title-right { flex-direction: row-reverse; }

.title {
  flex: 1 1 60%;
  margin: 0; /* sin margen inferior aquí */
  max-width: 600px;
}
.info-block.title-left  .title { text-align: left; }
.info-block.title-right .title { text-align: right; }
.text {
  flex: 1 1 50%;
  max-width: 800px;
  position: relative;
  padding-bottom: 12px; 

}
.text::after{
  content: "";
  display: block;
  height: 3px;
  width: 28%;
  background: linear-gradient(90deg, #4dffc1, #1a73e8);
  border-radius: 999px;
  margin-top: 12px;
}
/* Alineación del texto y de la línea por lado */
.info-block.title-left  .text { text-align: right; }
.info-block.title-left  .text::after { margin-left: auto; }
.info-block.title-right .text { text-align: left; }
.info-block.title-right .text::after { margin-right: auto; }
.text p { font-size: 1.6rem; line-height: 1.7; }
.info h3 { font-weight: 650; }
.link {
  display:inline-block;
  margin-top:16px;
  color:#000000;
  font-weight:700;
  text-decoration: underline;
  text-underline-offset: 6px;
  text-decoration-thickness: 2px;
}
.link::after{
  content: "→";
  display: inline-block;
  margin-left: 12px;
  transition: transform .15s ease-in-out;
}
.link:hover::after{ transform: translateX(3px); }
@media (max-width: 900px){
  .info-block { flex-direction: column; gap: 8px; margin-bottom: 48px; }
  .title, .text { flex: 1 1 auto; max-width: 100%; text-align: left !important; }
}


</style>
