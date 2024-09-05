export default {
    data() {
        return {
            tooltipTalent: null
        }
    },
    methods: {
        showTooltip(talent) {
            this.tooltipTalent = talent;
        },
        hideTooltip() {
            this.tooltipTalent = null;
        }
    }
}
