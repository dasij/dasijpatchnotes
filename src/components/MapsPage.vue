<template>
    <div class="maps-page-container">
        <div class="content-wrapper">
            <div class="container mx-auto py-8">
                <h1 class="text-3xl font-bold mb-4 text-white">Maps</h1>
                <div class="grid">
                    <div v-for="map in sortedMaps" :key="map.id" class="map-item" @mouseover="hover = map.id"
                        @mouseleave="hover = null">
                        <router-link :to="'/map/' + map.name.toLowerCase()" class="block relative">
                            <div class="image-container" :class="{ 'unchanged': !map.changed }">
                                <img :src="require(`@/assets/${map.image}`)" :alt="map.name" class="map-image" />
                                <span class="map-name" v-if="hover === map.id && !map.changed">Under Construction</span>
                                <span class="map-name" v-else>{{ map.name }}</span>
                            </div>
                        </router-link>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'MapsPage',
    data() {
        return {
            maps: [],
            hover: null // Track hover state
        };
    },
    computed: {
        sortedMaps() {
            // Create a copy of the maps array and sort by name
            const sortedByName = [...this.maps].sort((a, b) => a.name.localeCompare(b.name));
            // Then group by 'changed' status
            const changed = sortedByName.filter(map => map.changed);
            const unchanged = sortedByName.filter(map => !map.changed);
            // Concatenate the two arrays: changed first, then unchanged
            return [...changed, ...unchanged];
        }
    },
    async created() {
        const mapFiles = require.context('@/data/maps', false, /\.json$/);
        const maps = await Promise.all(
            mapFiles.keys().map(async (key) => {
                const mapData = await mapFiles(key);
                return {
                    id: mapData.id,
                    name: mapData.name,
                    image: mapData.image,
                    changed: mapData.changed // Ensure this property is correctly read from the JSON
                };
            })
        );
        this.maps = maps;
    }
};
</script>

<style scoped>
/* Existing styles remain unchanged */
.content-wrapper {
    background-color: rgba(0, 0, 0, 0.7);
    min-height: calc(100vh);
}

.maps-page-container {
    background-image: url('@/assets/maps_page_background.jpg');
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    min-height: 100vh;
}

.grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    /* Two items per row */
    gap: 10px;
}

.map-item {
    text-align: center;
    position: relative;
    box-shadow: 0 4px 8px #2E1939;
    /* Purple box shadow */
    transition: box-shadow 0.3s ease;
    /* Smooth transition for box shadow */
}

.image-container {
    position: relative;
    overflow: hidden;
}

.image-container::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: black;
    opacity: 0.5;
    /* Default dark overlay for changed items */
    transition: opacity 0.3s ease;
}

.image-container.unchanged::before {
    opacity: 0.9;
    /* Darker overlay for unchanged items */
}

.image-container:hover::before {
    opacity: 0;
    /* Remove overlay on hover */
}

.map-image {
    height: 195px;
    width: 100%;
    object-fit: cover;
}

.map-name {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    color: #CCE5FA;
    /* Default color */
    font-size: 24px;
    font-weight: bold;
    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.8);
    /* Default text shadow */
    transition: color 0.3s ease, text-shadow 0.3s ease;
    /* Smooth transitions for color and text shadow */
}

.map-item:hover .map-name {
    color: white;
    /* White color on hover */
    text-shadow: 4px 4px 8px rgba(0, 0, 0, 1);
    /* Enhanced text shadow on hover */
}
</style>
