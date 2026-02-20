<template>
  <div class="dev-comments-wrapper" :class="{ open: isOpen }">
    <div class="dev-comments-tab" @click="$emit('toggle')">
      <span>{{ isOpen ? '▼' : '▲' }}</span>
      <span class="tab-text">Dev Comments</span>
    </div>
    <div class="dev-comments-content-wrapper">
      <div class="dev-comments-content" v-if="comment">
        <p><RichText v-if="findAbilityOrTalent" :text="comment" :convert-fn="findAbilityOrTalent" /></p>
      </div>
      <div v-else class="dev-comments-content no-comment">
        <p>No developer comments available.</p>
      </div>
    </div>
  </div>
</template>

<script setup>
/* eslint-disable no-undef */
import { inject } from 'vue'
import RichText from '@/components/RichText.vue'

defineProps({
  isOpen: { type: Boolean, default: false },
  comment: { type: String, default: null }
})

defineEmits(['toggle'])

const findAbilityOrTalent = inject('findAbilityOrTalent', () => null)
</script>

<style scoped>
/* Wrapper posicionado ACIMA da área de descrição */
.dev-comments-wrapper {
  position: absolute;
  bottom: 100%;
  left: 0;
  right: 0;
  z-index: 1000;
}

/* Aba sempre visível */
.dev-comments-tab {
  position: absolute;
  bottom: -1px;
  right: 20px;
  transform: translateY(100%);
  background: #742aff;
  color: #fff;
  padding: 8px 20px;
  border-radius: 0 0 8px 8px;
  cursor: pointer;
  font-size: 11px;
  font-weight: bold;
  text-transform: uppercase;
  letter-spacing: 1px;
  box-shadow: 0 4px 15px rgba(116, 42, 255, 0.5);
  transition: background 0.2s, box-shadow 0.2s;
  display: flex;
  align-items: center;
  gap: 6px;
  white-space: nowrap;
  z-index: 1001;
}

.dev-comments-tab:hover {
  background: #9933ff;
  box-shadow: 0 6px 20px rgba(116, 42, 255, 0.7);
}

.tab-text {
  font-size: 10px;
}

/* Wrapper do conteúdo que expande */
.dev-comments-content-wrapper {
  background: rgba(20, 10, 35, 0.98);
  border-bottom: 3px solid #742aff;
  border-radius: 0;
  max-height: 0;
  overflow: hidden;
  opacity: 0;
  transform: translateY(-10px);
  transition: all 0.3s ease;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.8);
}

.dev-comments-wrapper.open .dev-comments-content-wrapper {
  max-height: 250px;
  opacity: 1;
  transform: translateY(0);
  overflow-y: auto;
}

/* Conteúdo dos comentários */
.dev-comments-content {
  padding: 20px;
  min-height: 60px;
}

.dev-comments-content p {
  color: #eee;
  font-size: 14px;
  line-height: 1.7;
  font-style: italic;
  margin: 0;
}

.dev-comments-content.no-comment p {
  color: #777;
}

/* ===========================================
   RESPONSIVE STYLES
   =========================================== */

/* Tablet */
@media (max-width: 991px) {
  .dev-comments-tab {
    padding: 6px 15px;
    right: 15px;
    font-size: 10px;
  }
  
  .tab-text {
    font-size: 9px;
  }
  
  .dev-comments-wrapper.open .dev-comments-content-wrapper {
    max-height: 200px;
  }
  
  .dev-comments-content {
    padding: 15px;
  }
  
  .dev-comments-content p {
    font-size: 12px;
    line-height: 1.6;
  }
}

/* Mobile */
@media (max-width: 767px) {
  .dev-comments-tab {
    padding: 5px 12px;
    right: 10px;
    font-size: 9px;
    gap: 4px;
  }
  
  .tab-text {
    font-size: 8px;
  }
  
  .dev-comments-wrapper.open .dev-comments-content-wrapper {
    max-height: 180px;
  }
  
  .dev-comments-content {
    padding: 12px;
  }
  
  .dev-comments-content p {
    font-size: 11px;
    line-height: 1.5;
  }
}
</style>
