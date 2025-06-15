<template>
  <div class="top-products">
    <!-- MBTI Top 3 -->
    <h2>{{ userStore.user.mbti }} Top 3</h2>
    <hr>
    <div v-for="product in recommendStore.rankedProductsList.slice(0, 3)" :key="product?.product?.fin_prdt_cd" class="card mb-3">
      <div class="card-body" v-if="product && product.product" 
      @click="goDetail(product.product.fin_prdt_cd, product.product.fin_prdt_nm)"
      :style="{ backgroundColor: getRandomColor(0.8), borderColor: getRandomColor(1) }"
      >
        <strong>
          {{ product.product.kor_co_nm }}
        </strong>
        <div style="color: black;">
          {{ product.product.fin_prdt_nm }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRecommendStore } from '@/stores/recommend'
import { useUserStore } from '@/stores/user'
import { useRouter } from 'vue-router'

const router = useRouter()
const userStore = useUserStore()
const recommendStore = useRecommendStore()

recommendStore.rankingProduct({ mbti: userStore.user.mbti })

const goDetail = function (finPrdtCd, finPrdtNm) {
  if (finPrdtNm.includes('예금')) {
    router.push({name:'deposit_product_detail', params:{fin_prdt_cd: finPrdtCd}})
  } else {
    router.push({name:'saving_product_detail', params:{fin_prdt_cd: finPrdtCd}})
  }
}

// 랜덤 색깔 부여
const getRandomColor = (opacity) => {
  const letters = '0123456789ABCDEF';
  let color = '#';
  for (let i = 0; i < 6; i++) {
    color += letters[Math.floor(Math.random() * 16)];
  }
  return color + (opacity !== undefined ? Math.round(opacity * 255).toString(16) : '');
}


</script>

<style scoped>
.top-products {
  display: flex;
  flex-wrap: wrap;
  justify-content: center; /* 카드를 수평 중앙 정렬 */
  border-radius: 10px;
  background-color: white;
  border: 1px solid;
  padding: 20px;
}

.card {
  width: 300px; /* 카드 너비 조절 */
  background-color: #fff;
  border: 1px solid #ddd;
  border-radius: 8px;
  margin-bottom: 15px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.card-body {
  padding: 20px; /* 카드 내용 여백 */
  cursor: pointer; /* 포인터로 마우스 스타일 변경 */
  transition: background-color 0.3s ease; /* 배경색 변경 시 부드러운 효과 */
  border-radius: 10px;
  color: black;
}

.card-body:hover {
  background-color: rgba(5, 244, 104, 0.9) !important;
}

.card-body strong {
  font-size: 1.2em;
}

.card-body div {
  margin-top: 8px;
  color: #555;
}
</style>
