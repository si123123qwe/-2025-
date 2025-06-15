<template>
  <div class="d-flex flex-column profile-container" style="background-color: gainsboro;">

    <header class="welcome">
      <h4><strong>{{ userStore.user.nickname }}</strong>님의 마이페이지<br><span>상품추천을 받아보세요!</span></h4>
      <div class="progress-bar-container">
      <div class="progress" @mouseover="isAssetGaugeVisible = true" @mouseout="isAssetGaugeVisible = false">
        <div class="progress-bar" role="progressbar" 
        :aria-valuenow="calculateProgress" aria-valuemin="0" 
        :aria-valuemax="userStore.user.target_asset" 
        :style="{ width: calculateProgress + '%' }"
        >
          <!-- 텍스트를 나타내는 progress-label 추가 -->
          <p class="progress-label">{{ calculateProgress.toFixed(2) }}%</p>
          <!-- 창을 표시할 부분 -->
          <div v-show="isAssetGaugeVisible" class="asset-gauge-info">
            <strong>자산게이지(목표자산 달성률)</strong>
            <div>매일 가입상품의 금리를 계산해 현재자산이 증가합니다</div>
          </div>
        </div>
      </div>
    </div>
    </header>

    <div style="background-color: gainsboro; padding: 5px;">
    <div class="container">
      <!-- 왼쪽 메뉴 -->
      <div id="left" class="left-menu">
        <div @click="change(1)" class="product-type-buttons">가입상품</div>
        <hr>
        <div @click="change(2)" class="product-type-buttons">상품추천</div>
        <hr>
        <div @click="change(3)" class="product-type-buttons">기본정보</div>
      </div>

      <!-- 오른쪽 컨텐츠 -->
      <div id="right" class="right-content">
        <div v-if="status === '1'" class="content-section">
          <ProductView />
        </div>
        <div v-else-if="status === '2'" class="content-section">
          <PortfolioUpdate />
        </div>
        <div v-else class="content-section">
          <BasicInfoUpdate />
        </div>
      </div>
    </div>
  </div>
  <p>　</p>
  </div>
</template>

<script setup>
import { RouterView } from 'vue-router'
import ProductView from '@/views/ProductView.vue'
import PortfolioUpdate from '@/components/PortfolioUpdate.vue'
import BasicInfoUpdate from '@/components/BasicInfoUpdate.vue'
import { ref, onMounted, computed } from 'vue'
import { useUserStore } from '@/stores/user'
import { useRecommendStore } from '@/stores/recommend'
import { useRouter } from 'vue-router'
import { useFinanceStore } from '@/stores/finance'

const userStore = useUserStore()
const financeStore = useFinanceStore()
const allProducts = ref([])
const userProducts = ref([])
const status = ref('1')
const progress = ref(50); // 임의의 값, 실제 값에 따라 변경

// isAssetGaugeVisible 상태를 관리하는 ref 추가
const isAssetGaugeVisible = ref(false);

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

const goBack = function () {
  router.back()
}

const change = (num) => {
  if (num === 1) {
    status.value = '1'
  } else if (num === 2) {
    status.value = '2'
  } else {
    status.value = '3'
  }
}

// 현재 자산과 목표 자산을 가져오기
const currentMoney = ref(userStore.user.money)
const targetAsset = ref(userStore.user.target_asset)

// 현재 상태 계산
const calculateProgress = computed(() => {
  return (currentMoney.value / targetAsset.value) * 100
})


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

.asset-gauge-info {
  position: fixed;
  top: 25%;
  right: 2%;
  background-color: #fefefe;
  padding: 10px;
  border: 1px solid #ddd;
  z-index: 1;
  color: black;
  border-radius: 5px;
}

.progress-bar-container {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end; /* 내용을 오른쪽으로 정렬 */
}

.progress {
  height: 20px;
  width: 300px;
  position: relative; /* 상대 위치 설정 */
  height: 30px;
}

.progress-bar {
  border-radius: 10px;
  background-color: #05f240; /* 초록색으로 변경 */
}

.progress-label {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%); /* 가운데로 이동시키는 CSS */
  text-align: center;
  font-weight: bold;
  color: black;
}


/* 그리드 레이아웃 스타일 */
.profile-container {
  display: grid;
  grid-template-rows: auto 1fr;
  gap: 20px;
}

.container {
  display: grid;
  grid-template-columns: auto 1fr;
  background-color: white;
  border: 1px solid;
  border-radius: 10px;
  padding: 10px;
}

.content-section {
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
}

.product-type-buttons {
  margin-bottom: 20px;
}

.product-type-buttons {
  margin-top: 10px;
  background-color: #2ecc71;
  color: #ffffff;
  padding: 8px;
  border: none;
  cursor: pointer;
  transition: background-color 0.3s ease;
  border-radius: 5px;
}

.product-type-buttons:hover {
  background-color: #27ae60;
}

.left-menu {
  padding-right: 5px;
}

.right-content {
  border: 2px solid;
  border-radius: 10px;
  border-color: green;
}

</style>