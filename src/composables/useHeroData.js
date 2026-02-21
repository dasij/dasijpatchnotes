import { ref, computed, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const talentsCache = new Map()

export function useHeroData() {
  const route = useRoute()
  const router = useRouter()
  
  const hero = ref({})
  // Mantém os talentos de ambos os tipos separadamente
  const vanillaTalentsData = ref({})
  const modifiedTalentsData = ref({})
  const talentType = ref('modified')
  const selectedTalents = ref({
    modified: { 1: null, 4: null, 7: null, 10: null, 13: null, 16: null, 20: null },
    vanilla: { 1: null, 4: null, 7: null, 10: null, 13: null, 16: null, 20: null }
  })
  
  // Support both URL param and direct selection
  const selectedHeroName = ref('')
  
  const heroName = computed(() => selectedHeroName.value || route.params.name?.toLowerCase() || '')
  
  // Retorna os talentos do tipo atual (para compatibilidade com o código existente)
  const talents = computed(() => {
    return talentType.value === 'modified' ? modifiedTalentsData.value : vanillaTalentsData.value
  })
  
  // Mapeamento de nomes de heróis com hífen para nomes de arquivos sem hífen
  const heroNameToFileMap = {
    'li-ming': 'liming',
    'lt-morales': 'ltmorales',
    'sgt-hammer': 'sgthammer',
    'the-butcher': 'thebutcher',
    'the-lost-vikings': 'lostvikings',
    'cho': 'chogall',
    'gall': 'chogall'
  }
  
  const heroPortraitPath = computed(() => {
    if (!heroName.value) return ''
    const fileName = heroNameToFileMap[heroName.value] || heroName.value
    // Usa caminho direto para pasta public (não passa pelo webpack)
    return `/heroes_portraits/${fileName}.png`
  })
  
  // Helper para gerar caminho de imagem de talento (usa pasta public)
  const getTalentImagePath = (hero, imageName) => {
    if (!hero || !imageName) return ''
    // Se já for um caminho completo (começa com / ou http), retorna como está
    if (imageName.startsWith('/') || imageName.startsWith('http')) {
      return imageName
    }
    // Mapeia nomes de heróis com hífen para o formato da pasta
    const mappedHero = heroNameToFileMap[hero] || hero
    return `/talents/${mappedHero}/${imageName}`
  }
  
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
        // Carrega os talentos de AMBOS os tipos
        loadAllTalents(targetHero)
      }
    } catch (error) {
      console.error('Error loading hero data:', error)
    }
  }
  
  // Carrega os talentos de um tipo específico
  const loadTalents = (targetHero = null, type = null) => {
    const hero = targetHero || heroName.value
    const targetType = type || talentType.value
    if (!hero) return
    
    const cacheKey = `${hero}-${targetType}`
    
    if (talentsCache.has(cacheKey)) {
      if (targetType === 'modified') {
        modifiedTalentsData.value = talentsCache.get(cacheKey)
      } else {
        vanillaTalentsData.value = talentsCache.get(cacheKey)
      }
      return
    }
    
    try {
      const fileName = targetType === 'modified'
        ? `${hero}_talents.json`
        : `${hero}_talents_vanilla.json`
      const data = require(`@/data/heroes/talents/${fileName}`)
      
      if (targetType === 'modified') {
        modifiedTalentsData.value = data
      } else {
        vanillaTalentsData.value = data
      }
      talentsCache.set(cacheKey, data)
    } catch (error) {
      console.error(`Error loading ${targetType} talents:`, error)
      if (targetType === 'modified') {
        modifiedTalentsData.value = { abilities: { basic: [], heroic: [], trait: null, general: null } }
      } else {
        vanillaTalentsData.value = { abilities: { basic: [], heroic: [], trait: null, general: null } }
      }
    }
  }
  
  // Carrega os talentos de ambos os tipos
  const loadAllTalents = (targetHero = null) => {
    const hero = targetHero || heroName.value
    if (!hero) return
    
    loadTalents(hero, 'modified')
    loadTalents(hero, 'vanilla')
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
    // Não precisa carregar talentos aqui pois já temos ambos carregados
  }
  
  const setTalentType = (type) => {
    if (type === 'modified' || type === 'vanilla') {
      talentType.value = type
      // Não precisa carregar talentos aqui pois já temos ambos carregados
    }
  }
  
  const toggleTalentSelection = (level, talent) => {
    const type = talentType.value
    const current = selectedTalents.value[type]
    // Comparar por nome em vez de referência de objeto
    const isCurrentlySelected = current[level]?.name === talent.name
    const newValue = isCurrentlySelected ? null : talent
    
    // Criar novo objeto para garantir reatividade
    selectedTalents.value = {
      ...selectedTalents.value,
      [type]: {
        ...current,
        [level]: newValue
      }
    }
  }
  
  const resetSelections = () => {
    selectedTalents.value = {
      modified: { 1: null, 4: null, 7: null, 10: null, 13: null, 16: null, 20: null },
      vanilla: { 1: null, 4: null, 7: null, 10: null, 13: null, 16: null, 20: null }
    }
  }
  
  const isSelected = (level, talent) => 
    currentSelectedTalents.value[level]?.name === talent.name
  
  const isAnySelected = (level) => 
    currentSelectedTalents.value[level] !== null && currentSelectedTalents.value[level] !== undefined
  
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
  
  const setSelectedTalents = (type, selections) => {
    if (type === 'modified' || type === 'vanilla') {
      // Cria uma nova referência para garantir reatividade
      selectedTalents.value = {
        ...selectedTalents.value,
        [type]: { ...selectedTalents.value[type], ...selections }
      }
    }
  }

  return {
    hero,
    talents,
    vanillaTalentsData,
    modifiedTalentsData,
    heroName,
    heroPortraitPath,
    heroSplashPath,
    talentType,
    selectedTalents,
    currentSelectedTalents,
    selectedHeroName,
    loadHeroData,
    loadTalents,
    loadAllTalents,
    selectHero,
    toggleTalentType,
    setTalentType,
    toggleTalentSelection,
    resetSelections,
    setSelectedTalents,
    isSelected,
    isAnySelected,
    findAbilityOrTalent,
    getTalentImagePath
  }
}
