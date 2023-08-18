import axios from 'axios'

const state = () => ({
    dishes: []
})

const getters = {
}

const actions = {
    async getDishes({ commit }) {
        let response = await axios
            .get("dish/all").catch((error) => {
                console.log(error);
            });
        commit('setDishes', { data: response.data.dishes })
    },
    async saveDishIntoDB({ dispatch }, dish) {
        await axios
            .post("dish", { dish: dish }).catch((error) => {
                console.log(error);
            });

        await dispatch("getDishes")
    }
}

const mutations = {
    setDishes(state, payload) {
        console.log(payload.data);
        state.dishes = payload.data
    },
}

export default {
    state,
    getters,
    actions,
    mutations
}