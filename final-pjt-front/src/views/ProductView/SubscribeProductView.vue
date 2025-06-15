<template>
  <div class="welcome">
    <!-- 금융상품 가입 페이지 -->
    <h1>상품가입</h1>
  <!-- 뒤로 가기 -->
  <div class='product-type-buttons'>
    <button class='product-type-buttons' @click="goBack">뒤로가기</button>
  </div>
</div>
  <div style="background-color: gainsboro; padding: 10px; background-size: cover;">
    <div style="background-color: white; border: 1px solid; border-radius: 10px; padding: 20px;">
    <div class='product-type-buttons'>
        <!-- 예치금 및 월 납입금, 가입하기 -->
        <form @submit.prevent="userStore.subscribe(financeStore.OneProduct.product.fin_prdt_cd, payment)" style="text-align: center;">
          <label class="fs-5 fw-bold" v-if="financeStore.OneProduct.product.fin_prdt_nm.includes('예금')" for="payment">예치금(만원)　</label>
          <label class="fs-5 fw-bold" v-else-if="financeStore.OneProduct.product.fin_prdt_nm.includes('적금')" for="payment">월 납입금(만원)　</label>
          <input v-if="financeStore.OneProduct.product.fin_prdt_nm.includes('예금') || financeStore.OneProduct.product.fin_prdt_nm.includes('적금')" type="payment" name="payment" id="payment" v-model="payment">
          <button style="margin-left: 10px;" class='product-type-buttons'>가입하기</button>
        </form>
        <hr>
          <!-- 금융 상품 상세 정보 -->
          <p>공시제출월 : {{ financeStore.OneProduct.product.dcls_month }}</p>
          <p>금융회사명 : {{ financeStore.OneProduct.product.kor_co_nm }}</p>
          <p>상품명 : {{ financeStore.OneProduct.product.fin_prdt_nm }}</p>
          <div v-if="financeStore.OneProduct.product.fin_prdt_nm.includes('예금') || financeStore.OneProduct.product.fin_prdt_nm.includes('적금')">
            <p>가입제한 : {{ JOIN_DENY_CHOICES[financeStore.OneProduct.product.join_deny] }}</p>
            <p>가입방법 : {{ financeStore.OneProduct.product.join_way }}</p>
            <p>우대조건 :</p>
            <p>{{ financeStore.OneProduct.product.spcl_cnd }}</p>
            <p v-html="formatSpecialConditions(financeStore.OneProduct.product.spcl_cnd)"></p>
          </div>
      </div>
    </div>
    <p>　</p>
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

const payment = ref('')

financeStore.getAllProducts()
financeStore.getOneProduct(route.params.fin_prdt_cd)

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

// 뒤로가기
const goBack = () => {
  router.back()
}

</script>

<style  scoped>
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

</style>