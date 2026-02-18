import { ref, computed, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const talentsCache = new Map()

export function useHeroData() {
  const route = useRoute()
  const router = useRouter()
  
  const hero = ref({})
  const talents = ref({})
  const talentType = ref('modified')
  const selectedTalents = ref({
    modified: { 1: null, 4: null, 7: null, 10: null, 13: null, 16: null, 20: null },
    vanilla: { 1: null, 4: null, 7: null, 10: null, 13: null, 16: null, 20: null }
  })
  
  // Support both URL param and direct selection
  const selectedHeroName = ref('')
  
  const heroName = computed(() => selectedHeroName.value || route.params.name?.toLowerCase() || '')
  
  const heroPortraitPath = computed(() => {
    if (!heroName.value) return ''
    try {
      return require(`@/assets/heroes_portraits/${heroName.value}.png`)
    } catch {
      return ''
    }
  })
  
  const heroSplashPath = computed(() => {
    if (!heroName.value) return ''
    try {
      return require(`@/assets/heroes_splash/${heroName.value}.webp`)
    } catch {
      try {
        return require(`@/assets/heroes_splash/${heroName.value}.jpg`)
      } catch {
        return ''
      }
    }
  })
  
  const currentSelectedTalents = computed(() => 
    selectedTalents.value[talentType.value]
  )
  
  const loadHeroData = (heroNameOverride = null) => {
    const targetHero = heroNameOverride || heroName.value
    if (!targetHero) return
    
    try {
      const heroData = require(`@/data/heroes/${targetHero}.json`)
      if (heroData) {
        hero.value = heroData
        loadTalents(targetHero)
      }
    } catch (error) {
      console.error('Error loading hero data:', error)
    }
  }
  
  const loadTalents = (targetHero = null) => {
    const hero = targetHero || heroName.value
    if (!hero) return
    
    const cacheKey = `${hero}-${talentType.value}`
    
    if (talentsCache.has(cacheKey)) {
      talents.value = talentsCache.get(cacheKey)
      return
    }
    
    try {
      const fileName = talentType.value === 'modified'
        ? `${hero}_talents.json`
        : `${hero}_talents_vanilla.json`
      const data = require(`@/data/heroes/talents/${fileName}`)
      talents.value = data
      talentsCache.set(cacheKey, data)
    } catch (error) {
      console.error('Error loading talents:', error)
      talents.value = { abilities: { basic: [], heroic: [], trait: null, general: null } }
    }
  }
  
  const selectHero = (heroName) => {
    selectedHeroName.value = heroName.toLowerCase()
    
    // Update URL without navigation (optional - for bookmarking)
    if (router) {
      router.replace({ path: `/hero/${heroName.toLowerCase()}`, query: route.query })
        .catch(() => {}) // Ignore navigation errors
    }
    
    // Reset selections when changing hero
    resetSelections()
    
    // Load new hero data
    loadHeroData(heroName.toLowerCase())
  }
  
  const toggleTalentType = () => {
    talentType.value = talentType.value === 'modified' ? 'vanilla' : 'modified'
    loadTalents()
  }
  
  const toggleTalentSelection = (level, talent) => {
    const current = selectedTalents.value[talentType.value]
    current[level] = current[level] === talent ? null : talent
  }
  
  const resetSelections = () => {
    selectedTalents.value = {
      modified: { 1: null, 4: null, 7: null, 10: null, 13: null, 16: null, 20: null },
      vanilla: { 1: null, 4: null, 7: null, 10: null, 13: null, 16: null, 20: null }
    }
  }
  
  const isSelected = (level, talent) => 
    currentSelectedTalents.value[level] === talent
  
  const isAnySelected = (level) => 
    currentSelectedTalents.value[level] !== null
  
  const findAbilityOrTalent = (type, section, category, index, targetHero) => {
    const hero = targetHero || heroName.value
    if (!hero) return null
    
    const cacheKey = `${hero}-${type}`
    
    let talentsData
    if (talentsCache.has(cacheKey)) {
      talentsData = talentsCache.get(cacheKey)
    } else {
      try {
        const fileName = type === 'modified'
          ? `${hero}_talents.json`
          : `${hero}_talents_vanilla.json`
        talentsData = require(`@/data/heroes/talents/${fileName}`)
        talentsCache.set(cacheKey, talentsData)
      } catch {
        return null
      }
    }
    
    if (section === 'abilities') {
      if (category === 'trait') return talentsData.abilities.trait
      if (category === 'basic') return talentsData.abilities.basic?.[index]
      if (category === 'heroic') return talentsData.abilities.heroic?.[index]
      if (category === 'general') return talentsData.abilities.general
    } else if (section === 'talents') {
      return talentsData[category]?.[index]
    }
    return null
  }
  
  // Initialize from URL if present
  if (route.params.name) {
    selectedHeroName.value = route.params.name.toLowerCase()
    loadHeroData()
  }
  
  // Watch for URL changes
  watch(() => route.params.name, (newName) => {
    if (newName && newName.toLowerCase() !== selectedHeroName.value) {
      selectedHeroName.value = newName.toLowerCase()
      loadHeroData()
    }
  })
  
  return {
    hero,
    talents,
    heroName,
    heroPortraitPath,
    heroSplashPath,
    talentType,
    selectedTalents,
    currentSelectedTalents,
    selectedHeroName,
    loadHeroData,
    loadTalents,
    selectHero,
    toggleTalentType,
    toggleTalentSelection,
    resetSelections,
    isSelected,
    isAnySelected,
    findAbilityOrTalent
  }
}
