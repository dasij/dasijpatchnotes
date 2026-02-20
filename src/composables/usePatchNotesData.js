import { ref, computed, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const talentsCache = new Map()

export function usePatchNotesData() {
  const route = useRoute()
  const router = useRouter()
  
  // Estado principal
  const item = ref({})
  const itemType = ref('hero') // 'hero', 'map', 'general', 'gamemode'
  const itemName = ref('')
  
  // Dados de herói
  const vanillaTalentsData = ref({})
  const modifiedTalentsData = ref({})
  const talentType = ref('modified')
  const selectedTalents = ref({
    modified: { 1: null, 4: null, 7: null, 10: null, 13: null, 16: null, 20: null },
    vanilla: { 1: null, 4: null, 7: null, 10: null, 13: null, 16: null, 20: null }
  })
  
  // Dados de patch notes (maps, general, gamemodes)
  const patchNotes = ref([])
  const selectedChange = ref(null)
  
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
  
  // Computed
  const currentItemName = computed(() => itemName.value)
  const currentItemType = computed(() => itemType.value)
  const isHero = computed(() => itemType.value === 'hero')
  
  // Retorna os talentos do tipo atual (para heróis)
  const talents = computed(() => {
    return talentType.value === 'modified' ? modifiedTalentsData.value : vanillaTalentsData.value
  })
  
  const currentSelectedTalents = computed(() => 
    selectedTalents.value[talentType.value]
  )
  
  const itemPortraitPath = computed(() => {
    if (!itemName.value) return ''
    const fileName = heroNameToFileMap[itemName.value] || itemName.value
    
    if (itemType.value === 'hero') {
      return `/heroes_portraits/${fileName}.png`
    }
    return ''
  })
  
  const itemSplashPath = computed(() => {
    if (!itemName.value) return ''
    try {
      if (itemType.value === 'hero') {
        try {
          return require(`@/assets/heroes_splash/${itemName.value}.webp`)
        } catch {
          return require(`@/assets/heroes_splash/${itemName.value}.jpg`)
        }
      } else if (itemType.value === 'map') {
        return require(`@/assets/maps/menu/${itemName.value}-banner.png`)
      } else if (itemType.value === 'general') {
        return require(`@/assets/general/${itemName.value}.jpg`)
      } else if (itemType.value === 'gamemode') {
        return require(`@/assets/gamemodes/${itemName.value}.webp`)
      }
    } catch {
      return ''
    }
    return ''
  })
  
  // Lista de todas as mudanças (para maps, general, gamemodes)
  const allChanges = computed(() => {
    const changes = []
    patchNotes.value.forEach(patchNote => {
      if (patchNote.general && patchNote.general.length > 0) {
        patchNote.general.forEach((change) => {
          changes.push({
            ...change,
            patchNoteId: patchNote.id,
            patchNoteTitle: patchNote.title,
            patchNoteDate: patchNote.date,
            changeNumber: changes.length + 1
          })
        })
      }
    })
    return changes
  })
  
  // Métodos
  const loadItemData = async (type, name) => {
    if (!name) return
    
    itemType.value = type
    itemName.value = name.toLowerCase()
    
    try {
      if (type === 'hero') {
        const heroData = require(`@/data/heroes/${name.toLowerCase()}.json`)
        item.value = heroData
        loadAllTalents(name.toLowerCase())
        patchNotes.value = []
        selectedChange.value = null
      } else if (type === 'map') {
        const mapData = require(`@/data/maps/${name.toLowerCase()}.json`)
        item.value = mapData
        patchNotes.value = mapData.patchNotes || []
        selectedChange.value = allChanges.value.length > 0 ? allChanges.value[0] : null
      } else if (type === 'general') {
        const generalData = require(`@/data/general/${name.toLowerCase()}.json`)
        item.value = generalData
        patchNotes.value = generalData.patchNotes || []
        selectedChange.value = allChanges.value.length > 0 ? allChanges.value[0] : null
      } else if (type === 'gamemode') {
        const gameModeData = require(`@/data/gamemodes/${name.toLowerCase()}.json`)
        item.value = gameModeData
        patchNotes.value = gameModeData.patchNotes || []
        selectedChange.value = allChanges.value.length > 0 ? allChanges.value[0] : null
      }
    } catch (error) {
      console.error(`Error loading ${type} data:`, error)
    }
  }
  
  const loadTalents = (targetHero = null, type = null) => {
    const hero = targetHero || itemName.value
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
  
  const loadAllTalents = (targetHero = null) => {
    const hero = targetHero || itemName.value
    if (!hero) return
    
    loadTalents(hero, 'modified')
    loadTalents(hero, 'vanilla')
  }
  
  const selectItem = (type, name) => {
    itemType.value = type
    itemName.value = name.toLowerCase()
    
    // Update URL
    if (router) {
      let path = ''
      if (type === 'hero') path = `/hero/${name.toLowerCase()}`
      else if (type === 'map') path = `/map/${name.toLowerCase()}`
      else if (type === 'general') path = `/general/${name.toLowerCase()}`
      else if (type === 'gamemode') path = `/gamemode/${name.toLowerCase()}`
      
      router.replace({ path, query: route.query }).catch(() => {})
    }
    
    resetSelections()
    loadItemData(type, name.toLowerCase())
  }
  
  const selectChange = (change) => {
    selectedChange.value = change
  }
  
  const toggleTalentType = () => {
    talentType.value = talentType.value === 'modified' ? 'vanilla' : 'modified'
  }
  
  const setTalentType = (type) => {
    if (type === 'modified' || type === 'vanilla') {
      talentType.value = type
    }
  }
  
  const toggleTalentSelection = (level, talent) => {
    const type = talentType.value
    const current = selectedTalents.value[type]
    const isCurrentlySelected = current[level]?.name === talent.name
    const newValue = isCurrentlySelected ? null : talent
    
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
    selectedChange.value = null
  }
  
  const setSelectedTalents = (type, selections) => {
    if (type === 'modified' || type === 'vanilla') {
      selectedTalents.value = {
        ...selectedTalents.value,
        [type]: { ...selectedTalents.value[type], ...selections }
      }
    }
  }
  
  const findAbilityOrTalent = (type, section, category, index, targetHero) => {
    const hero = targetHero || itemName.value
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
  
  // Watch for route changes
  watch(() => route.params.name, (newName) => {
    if (newName && newName.toLowerCase() !== itemName.value) {
      const path = route.path
      let type = 'hero'
      if (path.includes('/map/')) type = 'map'
      else if (path.includes('/general/')) type = 'general'
      else if (path.includes('/gamemode/')) type = 'gamemode'
      
      loadItemData(type, newName.toLowerCase())
    }
  })
  
  // Initialize from URL if present
  if (route.params.name) {
    const path = route.path
    let type = 'hero'
    if (path.includes('/map/')) type = 'map'
    else if (path.includes('/general/')) type = 'general'
    else if (path.includes('/gamemode/')) type = 'gamemode'
    
    loadItemData(type, route.params.name.toLowerCase())
  }

  return {
    // Estado
    item,
    itemType,
    itemName,
    patchNotes,
    selectedChange,
    
    // Herói específico
    talents,
    vanillaTalentsData,
    modifiedTalentsData,
    talentType,
    selectedTalents,
    currentSelectedTalents,
    
    // Computed
    currentItemName,
    currentItemType,
    isHero,
    allChanges,
    itemPortraitPath,
    itemSplashPath,
    
    // Métodos
    loadItemData,
    selectItem,
    selectChange,
    loadTalents,
    loadAllTalents,
    toggleTalentType,
    setTalentType,
    toggleTalentSelection,
    resetSelections,
    setSelectedTalents,
    findAbilityOrTalent
  }
}
