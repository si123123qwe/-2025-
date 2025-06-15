<template>
  <div class="welcome">
    <div>
      <h1>예금상세정보</h1>
    </div>
    <div class="product-type-buttons">
      <button @click="goBack">뒤로가기</button>
    </div>
  </div>
  <div style="background-color: gainsboro; padding: 20px;">
  <div class="product-info">
    <!-- 예금 상품 상세 정보 -->
    <h2 style="text-align: center; margin-top: 20px;">{{ financeStore.depositProduct[0].product.fin_prdt_nm }}</h2>
    <div style="text-align: center;">
    <div v-if="userStore.isLogin" class='product-type-buttons'>
      <div v-if="userProductsArray.some(item => item[1] === financeStore.depositProduct[0].product.fin_prdt_cd)">
        <p>이미 구독 중인 상품입니다.</p>
        <button class='product-type-buttons' @click="updateUser(false)">해제하기</button>
      </div>
      <div v-else>
        <!-- 상품 가입페이지로 이동 -->
        <button class='product-type-buttons' @click="goSubscribe(financeStore.depositProduct[0].product.fin_prdt_nd)">가입하기</button>
      </div>
    </div>
  </div> 
  <hr>
      <div class="info-container">
        <div style="padding-left: 50px;">
          <p><strong>공시제출월</strong> : {{ financeStore.depositProduct[0].product.dcls_month }}</p>
          <p @click="goHomepage"><strong>금융회사명</strong> : <span class="clickable-text">{{ financeStore.depositProduct[0].product.kor_co_nm }}</span></p>
          <p><strong>가입제한</strong> : {{ JOIN_DENY_CHOICES[financeStore.depositProduct[0].product.join_deny] }}</p>
          <p><strong>가입방법</strong> : {{ financeStore.depositProduct[0].product.join_way }}</p>
        </div>

        <div style="padding-right: 50px;">
          <p><strong>우대조건</strong> :</p>
          <p>{{ financeStore.depositProduct[0].product.spcl_cnd }}</p>
          <p v-html="formatSpecialConditions(financeStore.depositProduct[0].product.spcl_cnd)"></p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useFinanceStore } from '@/stores/finance'
import { useUserStore } from '@/stores/user'
import { useRoute, useRouter } from 'vue-router'

const financeStore = useFinanceStore()
const userStore = useUserStore()

const route = useRoute()
const router = useRouter()
const finPrdtCd = ref('')

financeStore.getOneProduct()

// 현재 금융상품코드
finPrdtCd.value = route.params.fin_prdt_cd
// 단일 상품 조회
financeStore.getDepositProductDetail(route.params.fin_prdt_cd)
// 단일 상품의 옵션 목록 조회
financeStore.getDepositProductOptions(route.params.fin_prdt_cd)

// 가입제한 정보
const JOIN_DENY_CHOICES = {
  1: '제한 없음',
  2: '서민전용',
  3: '일부제한',
}

// 우대조건 줄바꿈 함수
const formatSpecialConditions = (spclCnd) => {
  const formattedConditions = spclCnd.replace('\n', '<br>')
  return formattedConditions
}

// 상품 구독하기
const updateUser = (isSubscribe) => {
  if (isSubscribe) {
    // 가입하기
    userStore.subscribe(financeStore.depositProduct[0].product.fin_prdt_cd)
  } else {
    // 해제하기
    userStore.unsubscribe(financeStore.depositProduct[0].product.fin_prdt_cd)
  }
  // 유저의 구독 상품 목록 갱신
  userProductsArray.value = userStore.user.financial_products || []
}

// 유저의 구독 상품 목록
const userProductsArray = computed(() => userStore.user.financial_products || [])

// 상품 가입 페이지로 이동
const goSubscribe = (finPrdtCd) => {
  router.push({name:'subscribe', params:{fin_prdt_cd: finPrdtCd}})
}

// 회사 정보 조회
financeStore.getCompanyDetail(financeStore.depositProduct[0].product.fin_co_no)

// 은행 홈페이지로 가기
const goHomepage = function () {
  // 은행 홈페이지 url 확인
  const homepageUrl = financeStore.company?.homp_url

  if (homepageUrl) {
    // 새 탭에서 은행 홈페이지 열기
    window.open(homepageUrl, '_blank')
  } else {
    console.error('은행 홈페이지 url이 없습니다.')
  }
}

// 뒤로 가기
const goBack = () => {
  router.back()
}
</script>

<style scoped>

.welcome {
  background-image: url('@/assets/upup2.png');
  background-size: 150px; /* 배경 이미지를 커버하도록 설정 */
  background-repeat: no-repeat;
  background-position: 10px; /* 이미지를 가운데 정렬 */
  padding: 20px;
  border-bottom: 20px solid green;
  background-color: white;
  text-align: end;
  height: 160px;
}
.product-info {
  background-color: white;
  border: 1px solid;
  border-radius: 10px;
  padding: 10px;
}

.section-title {
  font-size: 18px;
  font-weight: bold;
  margin-bottom: 10px;
}

.info-container {
  display: flex;
  justify-content: space-between;
}

.info-container div {
  width: 48%; /* 조정 가능한 너비 */
}

.product-type-buttons {
  margin-bottom: 20px;
}

.product-type-buttons button {
  margin-top: 10px;
  background-color: #2ecc71;
  color: #ffffff;
  padding: 8px;
  border: none;
  cursor: pointer;
  transition: background-color 0.3s ease;
  border-radius: 5px;
}

.product-type-buttons button:hover {
  background-color: #27ae60;
}

.clickable-text {
  color: #3498db;
  text-decoration: underline;
  cursor: pointer;
  transition: color 0.3s ease;
}

.clickable-text:hover {
  color: #2980b9;
}

.card-container {
  text-align: center;
}

</style>