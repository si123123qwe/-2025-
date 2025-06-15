<template>
  <div class="container d-flex flex-column p-2">
    <!-- 상품 추천 -->
    <h4 class="fw-bold">상품추천</h4>
    <p>선택한 카테고리에 따라 <strong>{{ userStore.user.username }}</strong>님과 유사한 이용자의 가입 상품을 추천합니다</p>
    <hr>
    <!-- 포트폴리오, 추천 카테고리, 상품 추천 -->
    <div class="d-flex">
      <!-- 왼쪽 영역 (카드) -->
      <div class="flex-shrink-0 me-4">
        <!-- 추천 카테고리 -->
        <div class="mb-4">
          <div class="fw-bold">카테고리</div>
          <hr>
          <div class="form-check">
            <input class="form-check-input" type="checkbox" v-model="selectedOptions.age" @change="recommendStore.updateRecommendation(selectedOptions)" />
            <label class="form-check-label">나이<strong>({{ ages }}대)</strong></label>
          </div>
          <div class="form-check">
            <input class="form-check-input" type="checkbox" v-model="selectedOptions.gender" @change="recommendStore.updateRecommendation(selectedOptions)" />
            <label class="form-check-label">성별<strong>({{ gender === 'M' ? '남성' : '여성' }})</strong></label>
          </div>
          <div class="form-check">
            <input class="form-check-input" type="checkbox" v-model="selectedOptions.mbti" @change="recommendStore.updateRecommendation(selectedOptions)" />
            <label class="form-check-label">MBTI<strong>({{ userStore.user.mbti }})</strong></label>
          </div>
          <div class="form-check">
            <input class="form-check-input" type="checkbox" v-model="selectedOptions.salary" @change="recommendStore.updateRecommendation(selectedOptions)" />
            <label class="form-check-label">연봉<strong>(±10%)</strong></label>
          </div>

        </div>
      </div>
      <!-- 오른쪽 영역 (상품 추천) -->
      <div class="flex-grow-1 overflow-auto">
        <div>
          <div class="fw-bold"></div>
          <!-- 인기 상품들 카드 -->
          <div>
            <!-- 필터링된 상품 출력 -->
            <div v-if="recommendStore.rankedProductsList.length > 0">
              <div v-for="product in recommendStore.rankedProductsList" :key="product?.product?.fin_prdt_cd" class="card mb-3">
                <div class="product-box" v-if="product && product.product" 
                @click="goDetail(product.product.fin_prdt_cd, product.product.fin_prdt_nm)"
                :style="{ backgroundColor: getRandomColor(0.8), borderColor: getRandomColor(1) }"
                >
                  <strong>
                    {{ product.product.kor_co_nm }}
                  </strong>
                  <div>
                    {{ product.product.fin_prdt_nm }} <br>
                    금리 : {{ product.options[0].intr_rate }}% <br>
                    예치기간 : {{ product.options[0].save_trm }} 개월 <br>
                    예상 만기 후 이자 및 원금 합계 :{{calculateMaturityAmount(product.options[0]).toFixed(2)}} 만원
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, defineProps  } from 'vue'
import { useRecommendStore } from '@/stores/recommend'
import { useUserStore } from '@/stores/user'
import { useFinanceStore } from '@/stores/finance'
import { useRouter } from 'vue-router'

const props = defineProps(['percentMoney'])

const userStore = useUserStore()
const recommendStore = useRecommendStore()
const financeStore = useFinanceStore()
const ages = Math.floor(userStore.user.age / 10) * 10
const gender = userStore.user.gender

const router = useRouter()
financeStore.getAllProducts()

// 선택 옵션
const selectedOptions = ref({
  age: false,
  gender: false,
  mbti: false,
  salary: false,
})

recommendStore.updateRecommendation(selectedOptions.value)

const goBack = function () {
  router.back()
}

const calculateMaturityAmount = (option) => {
  const principal = props.percentMoney / 5
  const interestRate = option.intr_rate / 100
  const time = option.save_trm

  if (option.intr_rate_type_nm === '단리') {
    return principal * (1 + interestRate * time)
  } else if (option.intr_rate_type_nm === '복리') {
    return principal * Math.pow((1 + interestRate), time)
  }
  return 0
}

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
.overflow-auto {
  max-height: 400px; /* 원하는 높이로 조절하세요 */
}

.product-box {
  padding: 15px;
  border-radius: 8px;
  border: none;
  color: rgb(33, 30, 30);
  transition: background-color 0.3s ease-in-out;
  font-size: 15px;
}

.product-box:hover {
  background-color: rgba(5, 244, 104, 0.9) !important;
}
</style>
