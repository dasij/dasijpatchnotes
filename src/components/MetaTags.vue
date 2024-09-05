<template>
    <span></span>
</template>

<script>
import { defineComponent, watch } from 'vue'
import { useRoute } from 'vue-router'

export default defineComponent({
    name: 'MetaTags',
    props: {
        title: String,
        description: String,
        image: String
    },
    setup(props) {
        const route = useRoute()

        const updateMetaTags = () => {
            document.title = props.title
            document.querySelector('meta[property="og:title"]').setAttribute('content', props.title)
            document.querySelector('meta[property="og:description"]').setAttribute('content', props.description)
            document.querySelector('meta[property="og:image"]').setAttribute('content', props.image)
            document.querySelector('meta[property="og:url"]').setAttribute('content', window.location.href)
        }

        watch(() => route.path, updateMetaTags)
        updateMetaTags()
    }
})
</script>