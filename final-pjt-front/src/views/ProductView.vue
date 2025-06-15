<template>
      <div>
        <div>
          <h4 class="fw-bold">가입상품 목록</h4>
          <hr>
          <ul v-if="userStore.user.financial_products && userStore.user.financial_products.length > 0">
            <li v-for="product in userProducts" :key="product.id">
              <!-- 상품명-->
              <span class="clickable-text" @click="goDetail(product.product.fin_prdt_cd, product.product.fin_prdt_nm)">
                {{ product.product.fin_prdt_nm }}
              </span>
              <button class='product-type-buttons' @click="updateUser(product.product.fin_prdt_cd)">해제하기</button>
            </li>
            <!-- 여기에 1년 간격으로 금액이 커지는 차트 보여주기 -->
          </ul>
        </div>
        <div>
          <h4 class="fw-bold">가입상품 금리</h4>
          <hr>
          <ProductChart />
        </div>
      </div>
</template>

<script setup>
import ProductChart from '@/components/ProductChart.vue'
import { ref, onMounted, computed } from 'vue'
import { useUserStore } from '@/stores/user'
import { useRouter } from 'vue-router'
import { useFinanceStore } from '@/stores/finance'

const userStore = useUserStore()
const financeStore = useFinanceStore()
const allProducts = ref([])
const userProducts = ref([])

onMounted(async () => {
  await financeStore.getDepositProducts()
  await financeStore.getSavingProducts()
  // 모든 상품 정보
  allProducts.value = [
      ...financeStore.depositProductList,
      ...financeStore.savingProductList
  ]
  // 유저가 가입한 상품명 목록
  const userProductsArray = computed(() => userStore.user.financial_products || [])

  // 가입한 상품 정보 가져오기
  userProducts.value = userProductsArray.value
  .map(item => findProductByCode(item[1]))
  .filter(product => product !== null)
})
  
const user = ref('')

user.value = userStore.user

const router = useRouter()

// 가입한 상품 정보 가져오기
const findProductByCode = function (finPrdtCd) {
  return allProducts.value.find(product => product.product.fin_prdt_cd === finPrdtCd) || null
}

// 상품 구독하기
const updateUser = (finPrdtCd) => {
  // 해제하기
  userStore.unsubscribe(finPrdtCd)
}

// 상품 상세페이지로 이동
const goDetail = function (finPrdtCd, finPrdtNm) {
  if (finPrdtNm.includes('예금')) {
    router.push({name:'deposit_product_detail', params:{fin_prdt_cd: finPrdtCd}})
  } else if (finPrdtNm.includes('적금')) {
    router.push({name:'saving_product_detail', params:{fin_prdt_cd: finPrdtCd}})
  } else {
    router.push({name:'annuity_saving_product_detail', params:{fin_prdt_cd: finPrdtCd}})
  }
  }

const goBack = function () {
  router.back()
}

</script>

<style scoped>
.clickable-text {
  color: #3498db;
  cursor: pointer;
  transition: color 0.3s ease;
}

.clickable-text:hover {
  color: #2980b9;
}

.product-type-buttons {
  margin-bottom: 20px;
}

.product-type-buttons{
  margin-right: 10px;
  background-color: #2ecc71;
  color: #ffffff;
  padding: 8px;
  border: none;
  cursor: pointer;
  transition: background-color 0.3s ease;
  border-radius: 5px;
  margin-left: 5px;
}

.product-type-buttons:hover {
  background-color: #27ae60;
}
</style>