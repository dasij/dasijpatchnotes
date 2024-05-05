<template>
  <div>
    <header><!-- Cabeçalho aqui --></header>
    <main class="container mx-auto py-8">
      <h1 class="text-4xl font-bold mb-4">Patch Notes</h1>
      <PatchNoteItem 
        v-for="note in patchNotes"
        :key="note.id"
        :title="note.title"
        :description="note.description"
      />
    </main>
    <footer><!-- Rodapé aqui --></footer>
  </div>
</template>

<script>
import PatchNoteItem from './PatchNoteItem.vue'

export default {
  components: {
    PatchNoteItem,
  },
  data() {
    return {
      patchNotes: [
        { id: 1, title: 'Patch Note 1', description: 'Description 1' },
        { id: 2, title: 'Patch Note 2', description: 'Description 2' },
      ],
    }
  },
}
</script>