<template>
  <div class="bg-hots-repeat bg-repeat-y bg-contain bg-center bg-no-repeat min-h-screen">
    <div class="container mx-auto py-8">
      <h1 class="text-4xl font-bold text-white mb-4">{{ hero.name }} PATCH NOTES</h1>

      <div v-for="patchNote in patchNotes" :key="patchNote.id" class="mb-12">
        <h2 class="text-2xl font-bold text-white mb-2">{{ patchNote.title }}</h2>
        <p class="text-gray-400 text-sm mb-6">{{ patchNote.date }}</p>

        <div v-if="patchNote.developerCommentary" class="mt-4 bg-[#742aff] bg-opacity-5 border-l-4 border-[#742aff] p-4 text-white italic">
          <p class="font-semibold mb-2">Developer Comment:</p>
          <p v-for="(paragraph, index) in patchNote.developerCommentary.split('\n\n')" :key="index">
            {{ paragraph }}
          </p>
        </div>

        <div v-if="patchNote.general && patchNote.general.length > 0" class="mt-8">
          <h3 class="text-xl font-semibold" style="color: #9900ff;">Base</h3>
          <ul class="list-disc list-inside space-y-4" style="color: #ccc8d3;">
            <li v-for="(item, index) in patchNote.general" :key="index">
              <span class="text-lg font-medium" style="color: #0099ff;">{{ item.change }}</span>
              <ul class="list-disc list-inside ml-4">
                <li v-for="(textItem, textIndex) in item.texts" :key="textIndex">
                  <span style="color: #ccc8d3;">{{ textItem.text }}</span>
                  <ul v-if="textItem.subtexts" class="list-disc list-inside ml-8">
                    <li v-for="(subtext, subtextIndex) in textItem.subtexts" :key="subtextIndex" class="text-sm" style="color: #ccc8d3;">
                      {{ subtext }}
                    </li>
                  </ul>
                </li>
              </ul>
              <div v-if="item.developerCommentary"
                class="mt-4 bg-[#742aff] bg-opacity-5 border-l-4 border-[#742aff] p-4 text-white italic">
                <p class="font-semibold mb-2">Developer Comment:</p>
                <p>{{ item.developerCommentary }}</p>
              </div>
            </li>
          </ul>
        </div>

        <div v-if="patchNote.sections" class="mt-8">
          <h3 class="text-xl font-semibold" style="color: #9900ff;">Talent</h3>
          <ul class="list-disc list-inside space-y-4" style="color: #ccc8d3;">
            <li v-for="(section, sectionIndex) in patchNote.sections" :key="sectionIndex">
              <span class="text-lg font-medium">{{ section.name }}</span>
              <ul class="list-disc list-inside ml-4">
                <li v-for="(change, changeIndex) in section.changes" :key="changeIndex">
                  <span class="text-lg font-medium" style="color: #0099ff;">{{ change.name }}</span>
                  <ul class="list-disc list-inside ml-4">
                    <li v-for="(textItem, textIndex) in change.texts" :key="textIndex">
                      <span style="color: #ccc8d3;">{{ textItem.text }}</span>
                      <ul v-if="textItem.subtexts" class="list-disc list-inside ml-8">
                        <li v-for="(subtext, subtextIndex) in textItem.subtexts" :key="subtextIndex" class="text-sm" style="color: #ccc8d3;">
                          {{ subtext }}
                        </li>
                      </ul>
                    </li>
                  </ul>
                  <div v-if="change.developerCommentary"
                    class="mt-4 bg-[#742aff] bg-opacity-5 border-l-4 border-[#742aff] p-4 text-white italic">
                    <p class="font-semibold mb-2">Developer Comment:</p>
                    <p>{{ change.developerCommentary }}</p>
                  </div>
                </li>
              </ul>
            </li>
          </ul>
        </div>

      </div>
    </div>
  </div>
</template>




<script>
import { heroes } from '../heroData.js'

export default {
  name: 'HeroPatchNotesPage',
  data() {
    return {
      hero: {},
      patchNotes: [],
    }
  },
  created() {
    const heroId = parseInt(this.$route.params.id)
    this.hero = heroes.find(hero => hero.id === heroId)
    this.patchNotes = this.hero.patchNotes
  },
}
</script>
