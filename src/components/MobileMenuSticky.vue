<template>
  <div class="mobile-menu-sticky">
    <button class="menu-btn" @click="$emit('toggle-sidebar')">
      <span class="menu-icon">☰</span>
      <span class="menu-text">Menu</span>
    </button>
    <div class="sticky-title">
      <span>{{ title }}</span>
    </div>
  </div>
</template>

<script>
export default {
  name: 'MobileMenuSticky',
  props: {
    title: {
      type: String,
      default: 'Select an Item'
    }
  },
  emits: ['toggle-sidebar']
}
</script>

<style scoped>
.mobile-menu-sticky {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  width: 100%;
  height: 50px;
  background: rgba(20, 20, 20, 0.98);
  border-bottom: 2px solid #444;
  display: flex;
  align-items: center;
  padding: 0 15px;
  z-index: 1000;
  gap: 15px;
}

.menu-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  background: transparent;
  border: none;
  color: #fff;
  cursor: pointer;
  padding: 8px 12px;
  border-radius: 6px;
  transition: all 0.2s;
}

.menu-btn:hover {
  background: rgba(116, 42, 255, 0.3);
}

.menu-icon {
  font-size: 20px;
}

.menu-text {
  font-size: 14px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.sticky-title {
  flex: 1;
  color: #888;
  font-size: 14px;
  text-align: center;
  padding-right: 80px; /* Compensar o espaço do botão */
}
</style>
