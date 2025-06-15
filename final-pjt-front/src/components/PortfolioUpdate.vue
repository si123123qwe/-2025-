<template>
  <div class="profile-box">
    <h4 class="fw-bold">저축성향선택</h4>
    <p>저축성향에 따라 예상 만기 후 이자 및 원금 합계를 파악합니다</p>
    <hr>

    <div class="portfolio-info">
      <div>연봉 : {{ user.salary }}</div>
      <div>
        <label for="salary">월급 : </label>
        <input @click="updatePercent" type="salary" name="salary" id="salary" v-model="salary">
      </div>
      <br>
      <p>
        <strong>저축성향</strong> : 
        <label>
          <input type="radio" v-model="savingsType" value="careful"/> 근검형
        </label>
        <label>
          <input style="margin-left: 10px;" type="radio" v-model="savingsType" value="challenging"/> 실속형
        </label>
        <label>
          <input style="margin-left: 10px;" type="radio" v-model="savingsType" value="diligent"/> 욜로형
        </label>
      </p>
      <div>월저축비중 : {{ percent }} %</div>
      <div>월저축금액 : {{ percentMoney }}</div>
      <button @click="updatePercent">저축성향선택</button>
    </div>
    <hr>
    <div>
      <RecommendProduct :percentMoney="percentMoney" />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useUserStore } from '@/stores/user'
import { useFinanceStore } from '@/stores/finance'
import { useRouter } from 'vue-router'
import axios from 'axios'
import RecommendProduct from './RecommendProduct.vue'
import { computed } from '@vue/reactivity'

const financeStore = useFinanceStore()
const userStore = useUserStore()
const user = ref('')
user.value = userStore.user
const salary = ref(Math.round(user.value.salary / 12))
// const percent = ref(0)
const percentMoney = ref(0)
const save = ref(Math.round(salary/5))
const router = useRouter()
const savingsType = ref(user.saving_type)
const favoriteCompany = ref(user.value.favorite_company)

const percent = computed(() => {
  if (savingsType.value === 'careful') {
    return 50
  } else if (savingsType.value === 'challenging') {
    return 30
  } else if (savingsType.value === 'diligent') {
    return 10
  } else {
    return 0
  }
})

onMounted(() => {
  // 사용자의 저축 성향에 따라 초기값 설정
  if (savingsType.value === 'careful') {
    percent.value = 50
  } else if (savingsType.value === 'challenging') {
    percent.value = 30
  } else if (savingsType.value === 'diligent') {
    percent.value = 10
  }
  percentMoney.value = Math.round(salary.value * percent.value / 100);
});

// 뒤로 가기
const goBack = function () {
  router.back()
}
console.log(percentMoney.value);
// 월 저축 비중
const updatePercent = () => {
  percentMoney.value = Math.round(salary.value * percent.value / 100)
  alert('수정 되었습니다.')
}
</script>

<style scoped>
.profile-box {
  background-color: white;
  border-radius: 5px;
  margin-bottom: 10px;
}

.portfolio-info {
  margin-top: 20px;
}

button {
  margin-top: 10px;
  background-color: #2ecc71; /* 초록색 테마색 */
  color: #ffffff; /* 흰색 텍스트 색상 */
  padding: 8px;
  border: none;
  cursor: pointer;
  transition: background-color 0.3s ease;
  border-radius: 5px;
}

button:hover {
  background-color: #27ae60; /* 마우스를 올렸을 때의 배경 색상 */
}
</style>
