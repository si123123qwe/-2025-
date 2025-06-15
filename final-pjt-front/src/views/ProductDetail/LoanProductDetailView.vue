<template>
  <div class="welcome">
    <div>
      <h1>연금상세정보</h1>
    </div>
    <div class="product-type-buttons">
      <button @click="goBack">뒤로가기</button>
    </div>
  </div>
  <div style="background-color: gainsboro; padding: 20px;">
      <div style="background-color: white; border: 1px solid; border-radius: 10px;">
      <h2 style="text-align: center; margin-top: 20px;">{{ financeStore.loanProduct.product.fin_prdt_nm }}</h2>
    <div v-if="userStore.isLogin" class='product-type-buttons' style="text-align: center;">
      <div v-if="userProductsArray.some(item => item[1] === financeStore.loanProduct.product.fin_prdt_cd)">
        <p>이미 구독 중인 상품입니다.</p>
        <button class='product-type-buttons' @click="updateUser(false)">해제하기</button>
      </div>
      <div v-else>
        <!-- 상품 가입페이지로 이동 -->
        <button class='product-type-buttons' @click="goSubscribe(financeStore.loanProduct.product.fin_prdt_nd)">가입하기</button>
      </div>
    </div>
    <hr style="margin-left: 10px; margin-right: 10px;">
    <div class="product-info">
      <!-- 예금 상품 상세 정보 -->
      <div class="info-container">
        <div style="padding-left: 50px;">
          <p><strong>공시제출월</strong> : {{ financeStore.loanProduct.product.dcls_month }}</p>
          <p @click="goHomepage"><strong>금융회사명</strong> : <span class="clickable-text">{{ financeStore.loanProduct.product.kor_co_nm }}</span></p>
          <p><strong>상품명</strong> : {{ financeStore.loanProduct.product.fin_prdt_nm }}</p>
          
          <!-- 주택 담보 대출 -->
          <p v-if="'mrtg_type' in financeStore.loanProduct.options[0]"><strong>가입 방법</strong> : {{ financeStore.loanProduct.product.join_way }}</p>
          <p v-if="'mrtg_type' in financeStore.loanProduct.options[0]"><strong>연체 이자율</strong> : </p>
          <p  v-if="'mrtg_type' in financeStore.loanProduct.options[0]" v-html="formatSpecialConditions(financeStore.loanProduct.product.dly_rate)"></p>
          <p v-if="'mrtg_type' in financeStore.loanProduct.options[0]"><strong>대출 한도</strong> : {{ financeStore.loanProduct.product.loan_lmt }}</p>
          
          <!-- 전세 자금 대출 -->
          <p v-if="!financeStore.loanProduct.options[0]['mrtg_type'] && 'rpay_type' in financeStore.loanProduct.options[0]"><strong>가입 방법</strong> : {{ financeStore.loanProduct.product.join_way }}</p>
          <p v-if="!financeStore.loanProduct.options[0]['mrtg_type'] && 'rpay_type' in financeStore.loanProduct.options[0]"><strong>연체 이자율</strong> : </p>
          <p v-if="!financeStore.loanProduct.options[0]['mrtg_type'] && 'rpay_type' in financeStore.loanProduct.options[0]"  v-html="formatSpecialConditions(financeStore.loanProduct.product.dly_rate)"></p>
          <p v-if="!financeStore.loanProduct.options[0]['mrtg_type'] && 'rpay_type' in financeStore.loanProduct.options[0]"><strong>대출 한도</strong> : {{ financeStore.loanProduct.product.loan_lmt }}</p>
          
          <!-- 신용 대출 -->
          <p v-if="'crdt_prdt_type' in financeStore.loanProduct.options[0]"><strong>가입 방법</strong> : {{ financeStore.loanProduct.product.join_way }}</p>
          <p v-if="'crdt_prdt_type' in financeStore.loanProduct.options[0]"><strong>대출 종류명</strong> : {{ financeStore.loanProduct.product.crdt_prdt_type_nm }}</p>
          <p v-if="'crdt_prdt_type' in financeStore.loanProduct.options[0]"><strong>CB 회사명</strong> : {{ financeStore.loanProduct.product.cb_name }}</p>
          <p v-if="'crdt_prdt_type' in financeStore.loanProduct.options[0]"><strong>금리 구분</strong> : {{ financeStore.loanProduct.options[0].crdt_lend_rate_type_nm }}</p>
        </div>

        <div style="padding-right: 50px;">
          <!-- 주택 담보 대출 -->
          <p v-if="'mrtg_type' in financeStore.loanProduct.options[0]"><strong>대출 부대비용</strong> :</p>
          <p v-if="'mrtg_type' in financeStore.loanProduct.options[0]" v-html="formatSpecialConditions(financeStore.loanProduct.product.loan_inci_expn)"></p>
          
          <p v-if="'mrtg_type' in financeStore.loanProduct.options[0]"><strong>중도 상환 수수료</strong> : </p>
          <p v-if="'mrtg_type' in financeStore.loanProduct.options[0]" v-html="formatSpecialConditions(financeStore.loanProduct.product.erly_rpay_fee)"></p>
          
          <!-- 전세 자금 대출 -->
          <p v-if="!financeStore.loanProduct.options[0]['mrtg_type'] && 'rpay_type' in financeStore.loanProduct.options[0]"><strong>대출 부대비용</strong> : </p>
          <p v-if="!financeStore.loanProduct.options[0]['mrtg_type'] && 'rpay_type' in financeStore.loanProduct.options[0]" v-html="formatSpecialConditions(financeStore.loanProduct.product.loan_inci_expn)"></p>
          
          <p v-if="!financeStore.loanProduct.options[0]['mrtg_type'] && 'rpay_type' in financeStore.loanProduct.options[0]">><strong>중도 상환 수수료</strong> : </p>
          <p v-if="!financeStore.loanProduct.options[0]['mrtg_type'] && 'rpay_type' in financeStore.loanProduct.options[0]"> v-html="formatSpecialConditions(financeStore.loanProduct.product.erly_rpay_fee)"></p>

          <!-- 신용 대출 -->
          <p v-if="'crdt_prdt_type' in financeStore.loanProduct.options[0]"></p>

        </div>
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

// 현재 금융상품코드
finPrdtCd.value = route.params.fin_prdt_cd
// 단일 상품 조회
console.log('대출 상품 조회 시작');
financeStore.getLoanProductDetail(route.params.fin_prdt_cd)

// 상품 구독하기
const updateUser = (isSubscribe) => {
  if (isSubscribe) {
    // 가입하기
    userStore.subscribe(financeStore.loanProduct.product.fin_prdt_cd)
  } else {
    // 해제하기
    userStore.unsubscribe(financeStore.loanProduct.product.fin_prdt_cd)
  }
  // 유저의 구독 상품 목록 갱신
  userProductsArray.value = userStore.user.financial_products || []
}

const crdtGrade = ref([1, 4, 5, 6, 10, 11, 12, 13 ])

// 줄바꿈 함수
const formatSpecialConditions = (data) => {
  const formattedConditions = data.replace('\n', '<br>')
  return formattedConditions
}

// 유저의 구독 상품 목록
const userProductsArray = computed(() => userStore.user.financial_products || [])

// 상품 가입 페이지로 이동
const goSubscribe = (finPrdtCd) => {
  router.push({name:'subscribe', params:{fin_prdt_cd: finPrdtCd}})
}

// 회사 정보 조회
financeStore.getCompanyDetail(financeStore.loanProduct.product.fin_co_no)

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
  margin-top: 20px;
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