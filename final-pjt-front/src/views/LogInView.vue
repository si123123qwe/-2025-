<template>
  <div class="welcome">
  <h1>로그인</h1>
  <p>오늘도 자산Up!에 오신 것을 환영합니다</p>
</div>
  <div style="background-color: gainsboro; padding: 20px;">
    <div class="login-container">
      <form @submit.prevent="logIn" class="login-form">
        <label for="username" class="fw-bold">아이디</label>
        <input class="form-control" type="text" id="username" v-model.trim="username" required>

        <label for="password" class="fw-bold">비밀번호</label>
        <input class="form-control" type="password" id="password" v-model.trim="password" required>
        <div class="text-center">
          <input type="submit" value="로그인" class="btn btn-success">
        </div>
      </form>
    </div>
    <p>　</p>
    <p>　</p>
    <p>　</p>
    <p>　</p>
    <p>　</p>
    <p>　</p>
    <p>　</p>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useUserStore } from '@/stores/user'

const username = ref(null)
const password = ref(null)

const userStore = useUserStore()

// 로그인 함수
const logIn = function () {
  const payload = {
    username: username.value,
    password: password.value
  }
  userStore.logIn(payload)
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
/* 추가한 스타일 */
.login-container {
  border: 2px solid #4CAF50; /* 초록색 테두리 */
  border-radius: 10px; /* 테두리 둥글게 */
  padding: 20px;
  max-width: 400px;
  margin: 0 auto;
  background-color: white;
  text-align: center;;
}

/* 기존 스타일 */
.login-form {
  display: grid;
  gap: 10px;
}
</style>
