<template>
  <div class="change-detail">
    <div v-if="change" class="change-content">
      <div class="change-header">
        <h2 class="change-title">{{ change.change }}</h2>
        <div class="change-meta">
          <span class="patch-note-info">{{ change.patchNoteTitle }} • {{ change.patchNoteDate }}</span>
        </div>
      </div>
      
      <div class="change-texts">
        <div
          v-for="(textItem, index) in change.texts"
          :key="index"
          class="text-item"
        >
          <p class="main-text">{{ textItem.text }}</p>
          
          <!-- Imagem associada ao texto -->
          <div v-if="textItem.image" class="text-image-container">
            <img 
              :src="getImageUrl(textItem.image)" 
              :alt="change.change"
              class="change-image"
            />
          </div>
          
          <!-- Subtextos -->
          <ul v-if="textItem.subtexts && textItem.subtexts.length > 0" class="subtexts-list">
            <li v-for="(subtext, subIndex) in textItem.subtexts" :key="subIndex" class="subtext-item">
              {{ subtext }}
            </li>
          </ul>
        </div>
      </div>
      
      <!-- Developer Commentary -->
      <div v-if="change.developerCommentary" class="dev-commentary">
        <div class="dev-commentary-header">
          <span class="dev-icon">💬</span>
          <span class="dev-label">Developer Commentary</span>
        </div>
        <p class="dev-text">{{ change.developerCommentary }}</p>
      </div>
    </div>
    
    <div v-else class="empty-state">
      <p class="empty-text">Select a change to view details</p>
    </div>
  </div>
</template>

<script setup>
/* eslint-disable no-undef */
defineProps({
  change: {
    type: Object,
    default: null
  }
})

const getImageUrl = (imagePath) => {
  try {
    return require(`@/assets/${imagePath}`)
  } catch {
    return ''
  }
}
</script>

<style scoped>
.change-detail {
  height: 100%;
  overflow-y: auto;
  padding-right: 10px;
}

.change-detail::-webkit-scrollbar {
  width: 8px;
}

.change-detail::-webkit-scrollbar-track {
  background: rgba(0, 0, 0, 0.3);
  border-radius: 4px;
}

.change-detail::-webkit-scrollbar-thumb {
  background: #555;
  border-radius: 4px;
}

.change-detail::-webkit-scrollbar-thumb:hover {
  background: #742aff;
}

.change-content {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.change-header {
  border-bottom: 2px solid #444;
  padding-bottom: 15px;
}

.change-title {
  color: #fff;
  font-size: 24px;
  font-weight: bold;
  margin: 0 0 10px 0;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.8);
}

.change-meta {
  display: flex;
  align-items: center;
  gap: 10px;
}

.patch-note-info {
  color: #888;
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.change-texts {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.text-item {
  background: rgba(30, 30, 30, 0.6);
  border-radius: 8px;
  padding: 15px;
  border-left: 3px solid #742aff;
}

.main-text {
  color: #ccc8d3;
  font-size: 15px;
  line-height: 1.6;
  margin: 0;
}

.text-image-container {
  margin-top: 15px;
  display: flex;
  justify-content: center;
}

.change-image {
  max-width: 100%;
  max-height: 300px;
  border-radius: 12px;
  border: 3px solid #742aff;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.5);
}

.subtexts-list {
  margin-top: 12px;
  padding-left: 20px;
  list-style-type: disc;
}

.subtext-item {
  color: #aaa;
  font-size: 14px;
  line-height: 1.5;
  margin-bottom: 6px;
}

.subtext-item::marker {
  color: #742aff;
}

.dev-commentary {
  background: rgba(116, 42, 255, 0.1);
  border: 1px solid rgba(116, 42, 255, 0.3);
  border-radius: 8px;
  padding: 15px;
  margin-top: 10px;
}

.dev-commentary-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 10px;
}

.dev-icon {
  font-size: 16px;
}

.dev-label {
  color: #742aff;
  font-size: 12px;
  font-weight: bold;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.dev-text {
  color: #ccc8d3;
  font-size: 14px;
  line-height: 1.6;
  font-style: italic;
  margin: 0;
}

.empty-state {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
  min-height: 200px;
}

.empty-text {
  color: #666;
  font-size: 16px;
  font-style: italic;
}
</style>
