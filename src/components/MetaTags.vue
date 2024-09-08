<template>
    <div v-if="false"></div>
</template>

<script>
import { defineComponent } from 'vue'
import { useMeta } from 'vue-meta'

export default defineComponent({
    name: 'MetaTags',
    props: {
        title: String,
        description: String,
        image: String
    },
    setup(props) {
        useMeta(() => ({
            title: props.title,
            meta: [
                { name: 'description', content: props.description },
                { property: 'og:title', content: props.title },
                { property: 'og:description', content: props.description },
                { property: 'og:image', content: props.image },
                { property: 'og:url', content: window.location.href }
            ]
        }))
    }
})
</script>