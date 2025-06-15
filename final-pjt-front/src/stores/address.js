import { ref } from 'vue'
import { defineStore } from 'pinia'
import { useUserStore } from '@/stores/user'
import axios from 'axios'
import router from '../router'

export const useAddressStore = defineStore('address', () => {
  const token = ref(null)
  const consumerKey = import.meta.env.VITE_ADDRESS_API_KEY
  const consumerSecret = import.meta.env.VITE_SECRET_API_KEY
  const infos = ref(null)

  const getToken = function () {
    axios({
      method: 'get',
      url: `https://sgisapi.kostat.go.kr/OpenAPI3/auth/authentication.json?consumer_key=${consumerKey}&consumer_secret=${consumerSecret}`
    })
    .then((res) => {
      console.log(res.data);
      token.value = res.data.result.accessToken
      axios({
        method: 'get',
        url: `https://sgisapi.kostat.go.kr/OpenAPI3/addr/stage.json?accessToken=${token.value}`
      })
      .then((res) => {
        infos.value = res.data
      })
      .catch((err) => {
        console.log(err);
      })
    })
    .catch((err) => {
      console.log(err);
    })

  }

  return { getToken, token, infos }
}, { persist: true })
