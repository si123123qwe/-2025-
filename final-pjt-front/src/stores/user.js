import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { useAddressStore } from '@/stores/address'
 
export const useUserStore = defineStore('user', () => {
  const API_URL = 'http://127.0.0.1:8000'
  const token = ref(null)
  const router = useRouter()
  const name = ref(null)
  const user = ref({})
  const addressStore = useAddressStore()

  // 회원가입 기능
  const signUp = function (payload) {
    const username = payload.username
    const password1 = payload.password1
    const password2 = payload.password2
    const nickname = payload.nickname
    const gender = payload.gender
    const age = payload.age
    const address = payload.address
    const salary = payload.salary
    const money = payload.money
    const mbti = payload.mbti.toUpperCase()
    const target_asset = payload.target_asset

    axios({
      method: 'post',
      url: `${API_URL}/accounts/signup/`,
      data: {
        username, password1, password2, nickname, gender, age, address, salary, money, mbti, target_asset
      }
    })
      .then(res => {
        console.log(res.data);
        const password = password1
        // 회원가입 하면 로그인 상태 유지하기
        console.log(username, password)
        logIn({ username, password })
      })
      .catch(err => console.log(err))
  }

  // 로그인 기능
  const logIn = function (payload) {
    console.log(payload)
    const username = payload.username
    const password = payload.password
    axios({
      method: 'post',
      url: `${API_URL}/accounts/login/`,
      data: {
        username, password
      }
    })
      .then(res => {
        token.value = res.data.key
        console.log('유저토큰',token.value)
        name.value = username
        // 유저 정보를 받아오기
        axios({
          method: 'get',
          url: `${API_URL}/accounts/user/`,
          headers: {
            Authorization: `Token ${token.value}`
          }
        })
        .then(res => {
          user.value = res.data
          console.log(res.data);
          // 로그인 후 메인페이지로 이동
          router.push({name: 'main'})
        })
        // accessToken 받아오기
        addressStore.getToken() 
      })
      .catch(err => console.log(err.response.data))
  }

  // 로그아웃 함수
  const logOut = function () {
    axios({
      method: 'post',
      url: `${API_URL}/accounts/logout/`,
      headers: {
        Authorization: `Token ${token.value}`
      }
    })
      .then(() => {
        // 로그아웃 성공 시 로컬 상태 초기화
        token.value = null
        localStorage.removeItem('user')
        router.push({ name: 'main'})
      })
      .catch(err => console.log(err.response.data))
  }

  // 로그인 여부
  const isLogin = computed(() => {
    if (token.value === null) {
      return false
    } else {
      return true
    }
  })

  // 회원 정보 수정
  const userUpdate = function (payload) {
    const newData = {
      username: payload.username,
      email: payload.email,
      nickname: payload.nickname,
      age: payload.age,
      address: payload.address,
      salary: payload.salary,
      money: payload.money,
      target_asset: payload.target_asset,
      mbti: payload.mbti.toUpperCase(),
    }
    axios({
      method: 'put',
      url: `${API_URL}/accounts/update-user/`,
      headers: {
        Authorization: `Token ${token.value}`,
      },
      data: newData,
    })
      .then((res) => {
        user.value = res.data
        console.log(res.data)
        console.log('회원정보 수정 완료!!');
      })
      .catch((err) => console.log(err));
  }

  // 상품 구독 해제
  const unsubscribe = function (finPrdtCd) {
    // 기존 상품 구독 배열
    const existingProducts = user.value.financial_products || []

    // 이미 구독한 상품인 경우 해당 상품 제거
    const updatedProducts = existingProducts.filter(productCode => productCode[1] !== finPrdtCd)
    console.log('구독을 해제합니다.')

    axios({
      method: 'put',
      url: `${API_URL}/accounts/update-user/`,
      headers: {
        Authorization: `Token ${token.value}`,
      },
      data: { financial_products: updatedProducts },
    })
      .then((res) => {
        user.value = res.data
        console.log(res.data)
      })
      .catch((err) => console.log(err))
  }

  // 현재 날짜 반환 함수
  const getCurrentDate = () => {
    const currentDate = new Date();
    const year = String(currentDate.getFullYear()).slice(-2)
    const month = String(currentDate.getMonth() + 1).padStart(2, '0')
    const day = String(currentDate.getDate()).padStart(2, '0')
    console.log(year+month+day);
    return year + month + day
  }

  // 구독
  const subscribe = function (finPrdtCd, payment) {
    const existingProducts = user.value.financial_products || []
    console.log(finPrdtCd, payment);
    // 없는 상품인 경우 새로 구독하기
    const newFinPrdtCd = existingProducts.concat([[getCurrentDate(), finPrdtCd, payment]])

    axios({
      method: 'put',
      url: `${API_URL}/accounts/update-user/`,
      headers: {
        Authorization: `Token ${token.value}`,
      },
      data: { financial_products: newFinPrdtCd },
    })
      .then((res) => {
        user.value = res.data;
        console.log(res.data);
        console.log('상품 구독 완료');
        router.back()
      })
      .catch((err) => console.log(err));
  }

  // 저축 성향 저장 및 수정
  const updateUserPortfolio  = function (savingsType, favoriteCompany) {
    axios({
      method: 'put',
      url: `${API_URL}/accounts/update-user/`,
      headers: {
        Authorization: `Token ${token.value}`,
      },
      data: {
        saving_type: savingsType,
        favorite_company: favoriteCompany,
      },
    })
    .then((res) => {
      user.value = res.data
      console.log(res.data)
      console.log('포트폴리오 수정 완료!!');
    })
    .then(() => {
      router.push({name:'portfolio'})
    })
    .catch((err) => console.log(err));
  }

  return { signUp, logIn, logOut, userUpdate, subscribe, unsubscribe, updateUserPortfolio, getCurrentDate, isLogin, token, name, user }
}, { persist: true })
