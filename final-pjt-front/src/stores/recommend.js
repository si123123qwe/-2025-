import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { useAddressStore } from '@/stores/address'
import { useUserStore } from '@/stores/user'
import { useFinanceStore } from '@/stores/finance'
 
export const useRecommendStore = defineStore('recommend', () => {
  const rankedProductsList = ref([])
  const userStore = useUserStore()
  const financeStore = useFinanceStore()

  // 상품 순위 필터링 후 반환
  const rankingProduct = (payload) => {
    console.log(payload);
    axios({
        method: 'post',
        url: `http://127.0.0.1:8000/finances/filter-user/`,
        data: payload,
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
    }).then((res) => {
      const tempProducts = ref([])
      tempProducts.value = res.data.map(entry => entry[0])
      const filteredProductCodes = tempProducts.value.map(productCode => productCode)
      console.log('상품 추천이 완료되었습니다.')
      return filteredProductCodes
    }).then((filteredProductCodes) => {
      rankedProductsList.value = filteredProductCodes.map(productCode => {
        return financeStore.allProductList.find(product => product.product.fin_prdt_cd === productCode) || null
      })
    }).catch(err => console.log(err))
  }

  // 추천 업데이트
  const updateRecommendation = (selectedOptions) => {
    const payload = {}
  
    if (selectedOptions.age) {
      payload.age = userStore.user.age
    }
    if (selectedOptions.gender) {
      payload.gender = userStore.user.gender
    }
    if (selectedOptions.mbti) {
      payload.mbti = userStore.user.mbti
    }
    if (selectedOptions.salary) {
      payload.salary = userStore.user.salary
    }  
    // 추천 상품 요청
    financeStore.getAllProducts()
    rankingProduct(payload)
  }

  const calculateAssetGrowthRate = (finPrdtCd, saveTerm) => {
    // 1. finPrdtCd에 해당하는 상품 찾기
    financeStore.getAllProducts()

    const targetProduct = financeStore.allProductList.find(product => product.product.fin_prdt_cd === finPrdtCd)

    // 2. 예금인지 적금인지 체크
    const intr_rate_type_nm = ref('')
    if (targetProduct.product.fin_prdt_nm.includes('예금')) {
      // 2-1. 예금이면
      intr_rate_type_nm.value = '단리'
    } else {
      intr_rate_type_nm.value = '복리'
    }
    
    // 3. 선택한 예치 기간에 해당하는 옵션 찾기
    const options = targetProduct.options    
    const selectedOption = options.find(option => option.save_trm === saveTerm)

    // 만약 옵션이 없으면
    if (!selectedOption) {
      console.error(`No option found for the selected deposit period: ${saveTerm}`)
      return null
    }
    // 저축 금리, 우대금리
    const interestRate = selectedOption.intr_rate
    const interestRate2 = selectedOption.intr_rate2

    return {intr_rate_type_nm, interestRate, interestRate2}
  }

// 유저 정보 갱신 여부 확인

// 유저 정보 갱신 된 날짜가 오늘이 아니면 날짜 차이만큼 부리 하기

// 부리 할 때는 유저가 가입한 상품들에 담긴 정보(예 : ['231101', 'WB00010', 200] 각각 상품 가입 날짜, 금융상품코드, 월 납입금)를 이용한다. 금융상품코드는 상품을 조회하여 금리와 예치기간과 금리 타입을 가져올 때 사용하고, 가입날짜와 월납입금은 현재 그 상품에 들어간 원금과 발생할 이자를 계산하는데 사용한다.  

const updateAsset = async () => {
  const userProducts = userStore.user.financial_products || []
  const currentDate = new Date()

  if (currentDate === userStore.user.updated_at) {
    console.log('현재 자산 갱신 완료')
    return 
  }
  // 수정된 날짜와 현재 날짜 차이
  const daysDiff = Math.floor((currentDate - userStore.user.updated_at) / (1000 * 60 * 60 * 24))

  let totalAmount = 0 // 추가될 이자
  let productDetail
  let joinDate
  let productCode
  let monthlyPayment

  for (const productInfo of userProducts) {
    // 가입일 날짜 변환
    joinDate = new Date(
      2000 + parseInt(productInfo[0].substring(0, 2)),
      parseInt(productInfo[0].substring(2, 4)) - 1,
      parseInt(productInfo[0].substring(4, 6))
    )
    // 상품 코드
    productCode = productInfo[1]
    // 예치금 혹은 월 납입금
    monthlyPayment = productInfo[2]
    
    // 금리 유형, 금리, 최고 우대 금리 구하기
    for (const term of [6, 12, 24, 36]) {
      productDetail = calculateAssetGrowthRate(productCode, term)
      // 맨 처음에 구한 값으로 결정
      if (productDetail) {
        break
      }
    }

    // 상품 유형 찾기
    const product = financeStore.allProductList.find(item => item.product.fin_prdt_cd === productCode)

    // 상품 이름
    const productName = product.product.fin_prdt_nm

    // 금리 유형, 금리, 최고 우대 금리 할당
    const { intr_rate_type_nm, interestRate, interestRate2 } = productDetail

    // 이자 계산
    if (productName.includes('예금')) {
      // 예금
      if (intr_rate_type_nm === '단리') {
        totalAmount = totalAmount === null ? calculateDailyInterest(monthlyPayment, interestRate, daysDiff) : totalAmount + calculateDailyInterest(monthlyPayment, interestRate, daysDiff)
      } else {
        totalAmount = totalAmount === null ? calculateCompoundInterestDaily(monthlyPayment, interestRate, daysDiff) : totalAmount + calculateCompoundInterestDaily(monthlyPayment, interestRate, daysDiff)
      }
    } else if (productName.includes('적금')) {
      // 적금
      if (intr_rate_type_nm === '단리') {
        totalAmount = totalAmount === null ? calculateSimpleInterest(monthlyPayment, interestRate, userStore.user.updated_at, currentDate) : totalAmount + calculateSimpleInterest(monthlyPayment, interestRate, userStore.user.updated_at, currentDate)
      } else {
        // 복리
        totalAmount = totalAmount === null ? calculateUpdatedPrincipal(monthlyPayment, interestRate, userStore.user.updated_at, currentDate) : totalAmount + calculateUpdatedPrincipal(monthlyPayment, interestRate, userStore.user.updated_at, currentDate)
      }
    } else {
      // 연금 미구현
    }
  }
  // totalAmount가 계산되지 않은 경우 갱신을 하지 않음
  if (!isNaN(totalAmount) && totalAmount !== 0) {
    userStore.userUpdate({
      username: userStore.user.username,
      email: userStore.user.email,
      nickname: userStore.user.nickname,
      age: userStore.user.age,
      address: userStore.user.address,
      salary: userStore.user.salary,
      money: userStore.user.money + totalAmount,
      target_asset: userStore.user.target_asset,
      mbti: userStore.user.mbti.toUpperCase(),
    })
  }
}

// 이자 계산 (적금, 복리)
const calculateUpdatedPrincipal = (monthlyPayment, interestRate, joinDate, currentDate) => {

  // 가입일과 현재 날짜 사이의 일 수 차이 계산
  const daysDiff = Math.floor((currentDate - joinDate) / (1000 * 60 * 60 * 24))
  console.log('가입일과 현재 날짜의 차이', daysDiff);

  // 월 단위 이자율
  const monthlyInterestRate = interestRate / 12 / 100

  let totalInterest = 0

  // 현재 날짜와 가입일 차이가 30일 미만이라면
  if (daysDiff < 30) {
    totalInterest += monthlyPayment * monthlyInterestRate * (daysDiff / 30)
  } else {
    // 30일씩 월 납입금이 추가되는 경우 계산
    const fullMonths = Math.floor(daysDiff / 30)
    totalInterest += monthlyPayment * monthlyInterestRate * fullMonths

    // 나머지 날짜에 대한 이자 계산
    const remainingDays = daysDiff % 30
    totalInterest += monthlyPayment * monthlyInterestRate * (remainingDays / 30)
  }
  console.log('계산 결과:', totalInterest.toFixed(2))

  return totalInterest
}

// 이자 계산 (적금, 단리)
const calculateSimpleInterest = (monthlyPayment, interestRate, joinDate, currentDate) => {

  // 가입일과 현재 날짜 사이의 일 수 차이 계산
  const daysDiff = Math.floor((currentDate - joinDate) / (1000 * 60 * 60 * 24))

  // 월 단위 이자율
  const monthlyInterestRate = interestRate / 12 / 100

  // 현재 날짜와 가입일 차이가 30일 이하라면
  if (daysDiff <= 30) {
    return monthlyPayment * monthlyInterestRate * (daysDiff / 30)
  } else {
    // 30일씩 월 납입금이 추가되는 경우 계산
    const fullMonths = Math.floor(daysDiff / 30)
    return monthlyPayment * monthlyInterestRate * fullMonths
  }
}

// 일 단리
const calculateDailyInterest = (principal, annualInterestRate, daysDiff) => {
  const dailyInterestRate = annualInterestRate / 36500
  const interest = principal * dailyInterestRate * daysDiff
  return interest
}
// 일 복리
const calculateCompoundInterestDaily = (principal, annualInterestRate, daysDiff) => {
  const dailyInterestRate = annualInterestRate / 36500
  const totalAmount = principal * Math.pow((1 + dailyInterestRate), daysDiff)
  const interest = totalAmount - principal
  return interest
}

  return { rankedProductsList, rankingProduct, updateRecommendation, calculateAssetGrowthRate, calculateUpdatedPrincipal, updateAsset, calculateSimpleInterest, calculateDailyInterest, calculateCompoundInterestDaily }
}, { persist: true })
