import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import axios from 'axios'

export const useExchangeStore = defineStore('exchange', () => {
  const userStore = useUserStore()
  console.log(userStore.token);
  const exchange_infos = ref([])
  const API_URL = 'http://127.0.0.1:8000'
  const router = useRouter()

  // 로그인 여부
  const isLogin = computed(() => {
    if (userStore.token === null) {
      return false
    } else {
      return true
    }
  })

  // DRF에 board_article 조회 요청을 보내는 action
  const getExchangeRate = function () {
    axios({
      method: 'get',
      url: `${API_URL}/adds/exchange-rate/`,
      headers: {
        Authorization: `Token ${userStore.token}`
      }
    })
      .then((res) =>{
        console.log(res.data)
        exchange_infos.value = res.data
      })
      .catch((err) => {
        console.log(err.response.data)
      })
  }

  return { isLogin, exchange_infos, getExchangeRate, API_URL }
}, { persist: true })
