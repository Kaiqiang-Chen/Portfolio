import {createStore} from 'vuex'
export default createStore({
    namespaced:true,
    state:{
        username:'',
        user_role:0,
        token:''
    },
    mutation:{
        set_jwt_token(state,payload)
        {
            state.jwt=payload
        }
    }
})
