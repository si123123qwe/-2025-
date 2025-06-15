<template>
  <!-- 프로필 페이지 기본 정보 -->
  <div>
    <div v-if="status === '1'" class="row">
      <div class="col-12">
        <div>
          <h4 class="fw-bold">기본정보</h4>
        </div>
        <hr>
        <div style="font-size: 20px;">
          <p><strong>아이디 : </strong>{{ userStore.user.username }}</p>
          <p><strong>별명</strong> : {{ userStore.user.nickname }}</p>
          <p v-if="userStore.user.gender === 'M'">
            <strong>성별</strong> : 남자
          </p>
          <p v-else>
            <strong>성별</strong> : 여자
          </p>
          <p><strong>나이</strong> : {{ userStore.user.age }}</p>
          <p><strong>주소</strong> : {{ userStore.user.address }}</p>
          <p><strong>연봉</strong> : {{ userStore.user.salary }} 만원</p>
          <p><strong>MBTI</strong> : {{ userStore.user.mbti }}</p>
          <p><strong>현재자산</strong> : {{ userStore.user.money }} 만원</p>
          <p><strong>목표자산</strong> : {{ userStore.user.target_asset }} 만원</p>
          <button @click="goUpdate" class="btn btn-success mt-3">수정</button>
        </div>
      </div>
    </div>
    <div v-else>
      <h4 class="fw-bold">기본정보수정</h4>
      <hr>
      <form @submit.prevent="updateUser" style="font-size: 20px;">
        <p><strong>아이디</strong> : {{ userStore.user.username }}</p>
        <div class="">
          <label for="nickname" class="form-label fw-bold">별명</label>
          <input type="text" class="form-control" id="nickname" v-model.trim="user.nickname">
        </div>
        <div class="">
          <label for="age" class="form-label fw-bold">나이</label>
          <input type="age" class="form-control" id="age" v-model.trim="user.age">
        </div>
        <div class="">
          <label for="address" class="form-label fw-bold">주소</label>
          <input type="address" class="form-control" id="address" v-model.trim="user.address">
        </div>
        <div class="">
          <label for="salary" class="form-label fw-bold">연봉(만원)</label>
          <input type="salary" class="form-control" id="salary" v-model.trim="user.salary">
        </div>
        <div class="">
          <label for="mbti" class="form-label fw-bold">MBTI</label>
          <input type="mbti" class="form-control" id="mbti" v-model.trim="user.mbti">
        </div>
        <div class="">
          <label for="money" class="form-label fw-bold">현재자산(만원)</label>
          <input type="money" class="form-control" id="money" v-model.trim="user.money">
        </div>
        <div class="">
          <label for="target_asset" class="form-label fw-bold">목표자산(만원)</label>
          <input type="target_asset" class="form-control" id="target_asset" v-model.trim="user.target_asset">
        </div>
        <button type="submit" class="btn btn-success mt-3">수정완료</button>
      </form>
    </div>
  </div>
</template>

<script setup>
import ProductChart from '@/components/ProductChart.vue'
import { ref, onMounted } from 'vue'
import { useUserStore } from '@/stores/user'
import { useRouter } from 'vue-router'
import { useFinanceStore } from '@/stores/finance'
const userStore = useUserStore()
const financeStore = useFinanceStore()
const allProducts = ref([])
const userProducts = ref([])
const router = useRouter()
const user = ref(userStore.user)
const status = ref('1')

const gender = ref('')

// 회원정보 수정
const goUpdate = function () {
  status.value = '2'
}
// 뒤로 가기
const goBack = function () {
  router.back()
}

const updateUser = () => {
  status.value = '1'
  userStore.userUpdate({
    // username: user.value.username,
    password: user.value.password,
    // email: user.value.email,
    nickname: user.value.nickname,
    age: user.value.age,
    address: user.value.address,
    salary: user.value.salary,
    money: user.value.money,
    target_asset: user.value.target_asset,
    mbti: user.value.mbti
  })
}
</script>

<style scoped>

</style>