<template>
    <div class="bg-general-page-container bg-cover bg-no-repeat min-h-screen">
        <div class="overlay"></div>
        <div class="container mx-auto py-8 relative">
            <h1 class="text-3xl font-bold mb-4 text-white">General</h1>
            <div class="general-grid">
                <div v-for="item in sortedGeneralItems" :key="item.id" class="text-center general-item">
                    <router-link :to="'/general/' + item.name.toLowerCase().replace(/ /g, '_')" class="block relative">
                        <div class="general-image-container mb-4">
                            <img :src="require(`@/assets/${item.image}`)" :alt="item.name"
                                class="w-full h-full object-cover mx-auto mb-2 rounded-lg transition duration-300 ease-in-out transform hover:scale-110" />
                            <span
                                class="text-lg font-bold text-[#CCE5FA] absolute inset-0 flex items-center justify-center">{{
                                    formatItemName(item.name) }}</span>
                        </div>
                        <div
                            class="general-border rounded-lg border-4 border-[#2E60A3] transition duration-300 ease-in-out hover:border-[#4a8fd9]">
                        </div>
                    </router-link>
                </div>
            </div>
        </div>
    </div>
</template>


<style scoped>
.bg-general-page-container {
    background-image: url('@/assets/general_page_background.jpg');
    background-size: cover;
    background-position: center;
    position: relative;
}

.overlay {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.7);
    z-index: 1;
}

.container {
    position: relative;
    z-index: 2;
}

.general-image-container {
    overflow: hidden;
    border-radius: 0.5rem;
    width: 100%;
    height: 200px;
    position: relative;
    /* Adjust the height as needed */
}

.general-image-container img {
    transition: transform 0.3s ease-in-out, filter 0.3s ease-in-out;
    filter: brightness(50%);
}

.general-image-container:hover img {
    transform: scale(1.1);
    filter: brightness(100%);
}

.general-border {
    position: absolute;
    top: 0;
    left: 50%;
    transform: translateX(-50%);
    width: 100%;
    height: 200px;
    /* Adjust the height as needed */
    pointer-events: none;
    transition: width 0.3s ease-in-out, height 0.3s ease-in-out;
}

.general-image-container:hover+.general-border {
    width: 100%;
    height: 205px;
    /* Adjust the height as needed */
    box-shadow: inset 0 0 7px rgba(74, 143, 217, 0.8), inset 0 0 3px rgba(74, 143, 217, 0.5);
}

.general-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 1rem;
}

.general-item {
    width: 100%;
    margin: 0 auto;
}

.general-image-container span {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    color: #CCE5FA;
    font-size: 24px;
    font-weight: bold;
    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.8);
    transition: color 0.3s ease, text-shadow 0.3s ease;
}

@media (min-width: 1024px) {
    .general-grid {
        grid-template-columns: repeat(3, 1fr);
        max-width: calc(300px * 3 + 2rem);
        /* 3 items + 2 gaps */
        margin-right: auto;
    }
}
</style>


<script>
export default {
    name: 'GeneralPage',
    data() {
        return {
            generalItems: [],
            sortedGeneralItems: []
        };
    },
    methods: {
        formatItemName(name) {
            return name.split('-').map(part => part.charAt(0).toUpperCase() + part.slice(1).toLowerCase()).join(' ');
        },
        sortGeneralItems() {
            this.sortedGeneralItems = this.generalItems.sort((a, b) => a.name.localeCompare(b.name));
        }
    },
    async created() {
        const generalFiles = require.context('@/data/general', false, /\.json$/);
        const generalItems = await Promise.all(
            generalFiles.keys().map(async (key) => {
                const itemData = await generalFiles(key);
                return {
                    id: itemData.id,
                    name: itemData.name,
                    image: itemData.image,
                    description: itemData.description,
                };
            })
        );
        this.generalItems = generalItems;
        this.sortGeneralItems();
    },
};
</script>
