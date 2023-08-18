const state = () => ({
    token: '',
    user: {}
})

const getters = {}

const actions = {
    login({ commit }, token) {
        commit('setToken', token)
    },
    logout({ commit }) {
        commit('clearToken')
    }
}

const mutations = {
    setToken(state, token) {
        state.token = token
    },
    clearToken(state) {
        state.token = null
    },
    setUser(state, user) {
        state.user = user
    },
}

export default {
    state,
    getters,
    actions,
    mutations
}