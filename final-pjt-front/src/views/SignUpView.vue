<template>
  <div class="welcome">
    <h1>회원가입</h1>
    <p>자산up!과 함께 자산을 증가시켜보아요</p>
  </div>
  <div style="background-color: gainsboro; padding: 20px;">
    <!-- 회원가입 form -->
    <div class="signup-container">

    <form @submit.prevent="signUp" class="signup-form">
      <div class="">
        <label for="username" class="form-label fw-bold">아이디</label>
        <input type="text" id="username" class="form-control" v-model.trim="username" required>
      </div>

      <div class="">
        <label for="password1" class="form-label fw-bold">비밀번호</label>
        <input type="password" id="password1" class="form-control" v-model.trim="password1" required>
      </div>

      <div class="">
        <label for="password2" class="form-label fw-bold">비밀번호확인</label>
        <input type="password" id="password2" class="form-control" v-model.trim="password2" required>
      </div>

      <div class="">
        <label for="nickname" class="form-label fw-bold">별명</label>
        <input type="text" id="nickname" class="form-control" v-model.trim="nickname">
      </div>

      <div class="">
        <label class="form-label fw-bold">성별</label>
        <div class="gender-radio">
            <input type="radio" id="male" value="M" v-model="gender" required>
            <label for="male">남자</label>
            <input type="radio" id="female" value="F" v-model="gender" required>
            <label for="female">여자</label>
        </div>
      </div>

      <div class="">
        <label for="age" class="form-label fw-bold">나이</label>
        <input type="number" id="age" class="form-control" v-model.trim="age">
      </div>

      <div class="">
        <label for="address" class="form-label fw-bold">주소</label>
        <input type="text" id="address" class="form-control" v-model.trim="address" required>
      </div>

      <div class="">
        <label for="salary" class="form-label fw-bold">연봉(만원)</label>
        <input type="number" id="salary" class="form-control" v-model.trim="salary">
      </div>

      <div class="">
        <label for="mbti" class="form-label fw-bold">MBTI</label>
        <input type="text" id="mbti" class="form-control" v-model.trim="mbti">
      </div>

      <div class="">
        <label for="money" class="form-label fw-bold">현재자산(만원)</label>
        <input type="number" id="money" class="form-control" v-model.trim="money">
      </div>

      <div class="">
        <label for="target_asset" class="form-label fw-bold">목표자산(만원)</label>
        <input type="number" id="target_asset" class="form-control" v-model.trim="target_asset">
      </div>

      <div class="text-center">
        <button type="submit" class="btn btn-success">회원가입</button>
      </div>
    </form>
</div>
    <div v-if="showWarning" class="warning-modal">
      <div class="warning-content">
        <p>{{ warningMessage }}</p>
        <button @click="hideWarning" class="btn btn-primary">닫기</button>
      </div>
    </div>
    <p>　</p>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useUserStore } from '@/stores/user'

const username = ref(null)
const password1 = ref(null)
const password2 = ref(null)
const gender = ref(null)
const age = ref(null)
const nickname = ref(null)
const address = ref(null)
const salary = ref(null)
const money = ref(null)
const mbti = ref(null)
const target_asset = ref(null)

const userStore = useUserStore()
const showWarning = ref(false)
const warningMessage = ref('')

// 회원가입 함수
const signUp = function () {

  if (!username.value) {
    showWarning.value = true
    warningMessage.value = '아이디를 입력해주세요'
    return
  }
  if (!password1.value) {
    showWarning.value = true
    warningMessage.value = '비밀번호를 입력해주세요'
    return
  }
  if (password2.value !== password1.value) {
    showWarning.value = true
    warningMessage.value = '비밀번호가 일치하지 않습니다.'
    return
  }
  if (!gender.value) {
    showWarning.value = true
    warningMessage.value = '성별을 선택해주세요.'
    return
  }
  if (!address.value) {
    showWarning.value = true
    warningMessage.value = '주소를 입력해주세요.'
    return
  }

  const payload = {
    username: username.value,
    password1: password1.value,
    password2: password2.value,
    nickname: nickname.value,
    gender: gender.value,
    age: age.value,
    address: address.value,
    salary: salary.value,
    money: money.value,
    mbti: mbti.value,
    target_asset: target_asset.value,
  }
  userStore.signUp(payload)
}

// 경고 메시지 숨기기
const hideWarning = function () {
  showWarning.value = false
}
</script>

<style scoped>
/* 가운데 정렬을 위한 스타일 */
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


.signup-container {
  border: 2px solid #4CAF50; /* 초록색 테두리 */
  border-radius: 10px; /* 테두리 둥글게 */
  padding: 20px;
  max-width: 400px;
  margin: 0 auto;
  background-color: white;
  text-align: center;;
}
.warning-modal {
  display: flex;
  justify-content: center;
  align-items: center;
  position: fixed;
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;
  background-color: rgba(0, 0, 0, 0.3);
}

.warning-content {
  background-color: white;
  padding: 20px;
  border-radius: 5px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.3);
  text-align: center;
}

.signup-form {
  display: grid;
  gap: 10px;
  max-width: 400px;
  margin: 0 auto;
}

.gender-radio {
  display: flex;
  gap: 10px;
  justify-content: center;
}
</style>
