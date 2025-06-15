<template>
  <div>
    <h1>기본정보수정</h1>
    <form @submit.prevent="updateUser">
      <!-- <label for="username">아이디 : </label>
      <input type="text" id="username" v-model.trim="user.username"><br>       -->
      <!-- <label for="email"> email : </label>
      <input type="email" id="email" v-model.trim="user.email"><br> -->
      <strong>아이디</strong> : {{ userStore.user.username }}
      <br>
      <label for="nickname">별명</label>
      <input type="nickname" id="nickname" v-model.trim="user.nickname"><br>
      <label for="age">나이</label>
      <input type="age" id="age" v-model.trim="user.age"><br>
      <label for="address">주소</label>
      <input type="address" id="address" v-model.trim="user.address"><br>
      <label for="salary">연봉</label>
      <input type="salary" id="salary" v-model.trim="user.salary"><br>
      <label for="mbti">MBTI</label>
      <input type="mbti" id="mbti" v-model.trim="user.mbti"><br>
      <label for="money">현재자산</label>
      <input type="money" id="money" v-model.trim="user.money"><br>
      <label for="target_asset">목표자산</label>
      <input type="target_asset" id="target_asset" v-model.trim="user.target_asset"><br>

      <input type="submit" value="수정하기">
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()
const user = ref(userStore.user)

const updateUser = () => {
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