<template>
  <section class="hero" :style="bgStyle">
    <div class="hero-inner container">
      <div class="hero-left">
        <h1 class="title">Levanta la voz, nosotros te respaldamos</h1>
        <p class="subtitle">
          Denuncia abusos o malas prácticas de funcionarios públicos de forma segura, confidencial y sencilla. Un sistema transparente creado para proteger tus derechos y fortalecer la rendición de cuentas.
        </p>
        <router-link :to="registerButtonLink" class="btn-primary">{{ registerButtonText }}</router-link>
      </div>
      <!-- a la derecha queda la imagen/espacio vacío similar a la referencia -->
    </div>
  </section>
</template>

<script setup>
import { computed } from 'vue'

import heroImg from '@/assets/images/foto_landing.jpg';
import auth from '@/stores/auth'

const bgStyle = {
  backgroundImage: `linear-gradient(rgba(0,0,0,0.55), rgba(0,0,0,0.55)), url(${heroImg})`,
  backgroundSize: 'cover',
  backgroundPosition: 'center'
}

// Computed para determinar el destino del botón
const registerButtonLink = computed(() => {
  return auth.state.user ? '/dashboard' : '/login?register=1'
})

// Computed para el texto del botón
const registerButtonText = computed(() => {
  return auth.state.user ? 'Ir al Dashboard' : 'Regístrate'
})

</script>

<style scoped>
.hero {
  min-height: 90vh;
  color: white;
  padding-bottom: 30px;
  position: relative;
}
.hero-inner {
  display:flex;
  justify-content: flex-start; /* alinear al borde izquierdo */
  align-items:center;
  height: calc(90vh - 40px);
  width: 100%;
}
.hero-left {
  width: 100%;
  max-width: none; /* sin límite para que el título pueda llegar a 50vw */
  padding-left: 0;
  padding-right: 0;
}
.title {

  line-height: 1.12;
  margin: 0 0 10px;
  font-weight:800;
  letter-spacing: 0;
  color:#fff;
  max-width: 50vw; /* el título solo se extiende hasta la mitad de la pantalla */
}
.subtitle {
  margin-bottom:16px;
  opacity:0.98;
  line-height:1.52;
  max-width: 35vw; /* subtítulo controlado para mantener composición */
  font-size: 18px;
  color:#fff; 
}
.btn-primary{
  display:inline-block;
  padding: 1rem 5rem;
  background:#e9ecef; /* gris claro similar al mockup */
  color:#ffffff;
  border-radius: 10px;
  text-decoration:none;
  font-weight:700;
  font-size: 1.05rem;
  background: rgba(255,255,255,0.5);

}
/* sin padding lateral; en móvil se controla desde global.css */
@media (max-width: 768px){
  .title { font-size:2rem; letter-spacing: 0.01em; max-width: 100%; }
  .hero-inner { height: auto; padding: 60px 0; }
}
</style>
