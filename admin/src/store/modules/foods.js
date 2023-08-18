import axios from 'axios'

const state = () => ({
    food_types: [],
    foods: {}
})

const getters = {
    foodTypes: state => {
        return state.food_types
    },
    foodTypesById: state => id => {
        return state.food_types.find(type => type.group_id === parseInt(id))
    },
    foodByTypeId: state => id => {
        return state.foods[id]
    }
}

const actions = {
    async getFoodTypes({ commit }) {
        let response = await axios
            .get('food/types')
            .catch((error) => {
                console.log(error);
            });
        commit('setFoodTypes', { data: response.data.types })
    },

    async getFoodById({ commit }, group_id) {
        let response = await axios
            .get("food", {
                params: {
                    group_id: group_id,
                    limit: 1000,
                },
            }).catch((error) => {
                console.log(error);
            });
        commit('addFoodById', { group_id: group_id, data: response.data.products })
    },
}

const mutations = {
    setFoodTypes(state, payload) {
        state.food_types = payload.data
    },
    addFoodById(state, payload) {
        state.foods[payload.group_id] = payload.data
    }
}

export default {
    state,
    getters,
    actions,
    mutations
}