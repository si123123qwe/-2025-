<template>
  <div class="top-products">
    <!-- 나이, 성별 Top 3 -->
    <h2>{{ ageRange }} {{ genderString }} Top 3</h2>
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
import { ref } from 'vue'
import { useRecommendStore } from '@/stores/recommend'
import { useUserStore } from '@/stores/user'
import { useFinanceStore } from '@/stores/finance'
import { useRouter } from 'vue-router'

const userStore = useUserStore()
const recommendStore = useRecommendStore()

const router = useRouter()
const userAge = userStore.user.age;

recommendStore.rankingProduct({ age: userStore.user.age, gender: userStore.user.gender })

// 나이 변환
let ageRange;

if (userAge < 10) {
  ageRange = '10세 미만';
} else if (userAge < 20) {
  ageRange = '10대';
} else if (userAge < 30) {
  ageRange = '20대';
} else if (userAge < 40) {
  ageRange = '30대';
} else if (userAge < 50) {
  ageRange = '40대';
} else if (userAge < 60) {
  ageRange = '50대';
} else {
  ageRange = '60세 이상';
}

// 성별 변환
const userGender = userStore.user.gender;

let genderString;

if (userGender === 'M') {
  genderString = '남성';
} else if (userGender === 'F') {
  genderString = '여성';
} else {
  genderString = '기타'; // 다른 경우에 대한 처리를 원하는 대로 설정할 수 있습니다.
}

// 상품 상세페이지로 이동
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
  width: 300px; /* 원하는 카드 너비 조절 */
  background-color: #fff; /* 카드 배경색 */
  border: 1px solid #ddd; /* 카드 테두리 스타일 */
  border-radius: 8px; /* 카드 테두리 둥글게 */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* 그림자 추가 */
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
  font-size: 1.2em; /* 강조 텍스트 크기 */
}

.card-body div {
  margin-top: 8px; /* 텍스트 간격 조절 */
  color: #555; /* 텍스트 색상 */
}
</style>
