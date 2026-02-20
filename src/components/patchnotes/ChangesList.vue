<template>
  <div class="changes-list">
    <h3 class="changes-title">Changes</h3>
    <div v-if="changes.length === 0" class="empty-state">
      <p class="empty-text">No changes available</p>
    </div>
    <div v-else class="changes-container">
      <div
        v-for="change in changes"
        :key="`${change.patchNoteId}-${change.change_id}`"
        class="change-item"
        :class="{ selected: isSelected(change) }"
        @click="selectChange(change)"
      >
        <div class="change-name">{{ change.change }}</div>
      </div>
    </div>
  </div>
</template>

<script setup>
/* eslint-disable no-undef */
const props = defineProps({
  changes: {
    type: Array,
    required: true
  },
  selectedChange: {
    type: Object,
    default: null
  }
})

const emit = defineEmits(['select-change'])

const isSelected = (change) => {
  return props.selectedChange?.change_id === change.change_id
}

const selectChange = (change) => {
  emit('select-change', change)
}
</script>

<style scoped>
.changes-list {
  height: 100%;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.changes-title {
  color: #fff;
  font-size: 18px;
  font-weight: bold;
  margin: 0 0 15px 0;
  padding-bottom: 10px;
  border-bottom: 2px solid #444;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.empty-state {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
}

.empty-text {
  color: #666;
  font-size: 14px;
  font-style: italic;
}

.changes-container {
  flex: 1;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 8px;
  padding-right: 5px;
}

.changes-container::-webkit-scrollbar {
  width: 6px;
}

.changes-container::-webkit-scrollbar-track {
  background: rgba(0, 0, 0, 0.3);
  border-radius: 3px;
}

.changes-container::-webkit-scrollbar-thumb {
  background: #555;
  border-radius: 3px;
}

.changes-container::-webkit-scrollbar-thumb:hover {
  background: #742aff;
}

.change-item {
  background: rgba(30, 30, 30, 0.8);
  border: 1px solid #444;
  border-radius: 8px;
  padding: 12px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.change-item:hover {
  background: rgba(116, 42, 255, 0.2);
  border-color: #742aff;
}

.change-item.selected {
  background: rgba(116, 42, 255, 0.4);
  border-color: #742aff;
  box-shadow: 0 0 10px rgba(116, 42, 255, 0.3);
}

.change-name {
  color: #fff;
  font-size: 14px;
  font-weight: 600;
  line-height: 1.3;
}

.change-item.selected .change-name {
  color: #fff;
}
</style>
