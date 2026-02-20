<template>
  <div class="splash-controls">
    <div class="horizontal-toggle">
      <span :class="{ active: modelValue === 'vanilla' }">Vanilla</span>
      <label class="switch">
        <input 
          type="checkbox" 
          :checked="modelValue === 'modified'"
          @change="$emit('update:modelValue', modelValue === 'modified' ? 'vanilla' : 'modified')"
        >
        <span class="slider"></span>
      </label>
      <span :class="{ active: modelValue === 'modified' }">Modified</span>
    </div>

    <label class="dev-comments-toggle">
      <input type="checkbox" v-model="devCommentsModel">
      <span class="checkmark-box">✓</span>
      <span class="label-text">Dev Notes</span>
    </label>
  </div>
</template>

<script setup>
/* eslint-disable no-undef */
import { computed } from 'vue'

const props = defineProps({
  modelValue: { type: String, default: 'modified' },
  devCommentsAlways: { type: Boolean, default: false }
})

const emit = defineEmits(['update:modelValue', 'update:devCommentsAlways'])

const devCommentsModel = computed({
  get: () => props.devCommentsAlways,
  set: (val) => emit('update:devCommentsAlways', val)
})
</script>

<style scoped>
.splash-controls {
  display: flex;
  align-items: center;
  gap: 20px;
  pointer-events: auto;
}

.horizontal-toggle {
  display: flex;
  align-items: center;
  gap: 12px;
  background: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(10px);
  padding: 10px 15px;
  border-radius: 30px;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.horizontal-toggle span {
  color: #666;
  text-transform: uppercase;
  font-size: 12px;
  letter-spacing: 1px;
  font-weight: 500;
  transition: all 0.3s;
}

.horizontal-toggle span.active {
  color: #fff;
  font-weight: bold;
}

.switch {
  position: relative;
  display: inline-block;
  width: 48px;
  height: 26px;
}

.switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

.slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #333;
  transition: .3s;
  border-radius: 26px;
}

.slider:before {
  position: absolute;
  content: "";
  height: 20px;
  width: 20px;
  left: 3px;
  bottom: 3px;
  background-color: white;
  transition: .3s;
  border-radius: 50%;
}

input:checked + .slider {
  background-color: #742aff;
}

input:checked + .slider:before {
  transform: translateX(22px);
}

.dev-comments-toggle {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  background: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(10px);
  padding: 10px 15px;
  border-radius: 30px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  transition: all 0.2s;
}

.dev-comments-toggle:hover {
  background: rgba(0, 0, 0, 0.8);
  border-color: rgba(116, 42, 255, 0.5);
}

.dev-comments-toggle input {
  display: none;
}

.checkmark-box {
  width: 18px;
  height: 18px;
  border: 2px solid #444;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  color: transparent;
  transition: all 0.2s;
  background: rgba(255,255,255,0.05);
}

.dev-comments-toggle input:checked + .checkmark-box {
  background: #742aff;
  border-color: #742aff;
  color: #fff;
  box-shadow: 0 0 10px rgba(116, 42, 255, 0.5);
}

.dev-comments-toggle .label-text {
  color: #888;
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 1px;
  font-weight: 500;
  transition: all 0.2s;
}

.dev-comments-toggle:hover .label-text,
.dev-comments-toggle input:checked ~ .label-text {
  color: #fff;
}

/* ===========================================
   RESPONSIVE STYLES
   =========================================== */

/* Tablet */
@media (max-width: 991px) {
  .splash-controls {
    gap: 12px;
  }
  
  .horizontal-toggle {
    gap: 8px;
    padding: 8px 12px;
  }
  
  .horizontal-toggle span {
    font-size: 10px;
    letter-spacing: 0.5px;
  }
  
  .switch {
    width: 40px;
    height: 22px;
  }
  
  .slider:before {
    height: 16px;
    width: 16px;
    left: 3px;
    bottom: 3px;
  }
  
  input:checked + .slider:before {
    transform: translateX(18px);
  }
  
  .dev-comments-toggle {
    gap: 6px;
    padding: 8px 12px;
  }
  
  .checkmark-box {
    width: 16px;
    height: 16px;
    font-size: 10px;
  }
  
  .dev-comments-toggle .label-text {
    font-size: 10px;
    letter-spacing: 0.5px;
  }
}

/* Mobile */
@media (max-width: 767px) {
  .splash-controls {
    gap: 8px;
  }
  
  .horizontal-toggle {
    gap: 6px;
    padding: 6px 10px;
    border-radius: 20px;
  }
  
  .horizontal-toggle span {
    font-size: 9px;
  }
  
  .switch {
    width: 36px;
    height: 20px;
  }
  
  .slider:before {
    height: 14px;
    width: 14px;
    left: 3px;
    bottom: 3px;
  }
  
  input:checked + .slider:before {
    transform: translateX(16px);
  }
  
  .dev-comments-toggle {
    gap: 5px;
    padding: 6px 10px;
    border-radius: 20px;
  }
  
  .checkmark-box {
    width: 14px;
    height: 14px;
    font-size: 9px;
  }
  
  .dev-comments-toggle .label-text {
    font-size: 9px;
  }
}

/* Small Mobile */
@media (max-width: 480px) {
  .splash-controls {
    flex-direction: column;
    gap: 6px;
    align-items: flex-start;
  }
  
  .horizontal-toggle,
  .dev-comments-toggle {
    padding: 5px 8px;
  }
}
</style>
