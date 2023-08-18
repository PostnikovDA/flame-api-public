const state = () => ({
    overlay: true,
})

const getters = {
    overlayStatus: state => {
        return state.overlay
    },
}

const actions = {
    changeOverlayStatus({ commit }, status) {
        commit('setOverlayStatus', { status })
    },
}

const mutations = {
    setOverlayStatus(state, payload) {
        state.overlay = payload.status
    },
}

export default {
    state,
    getters,
    actions,
    mutations
}