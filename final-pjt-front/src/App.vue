<template>
  <header>
    <nav id="app">
      <div class="nav-links">
        <!-- 고정된 Home 링크 -->
<!-- 고정된 Home 이미지 -->
        <router-link :to="{ name: 'main' }" class="nav-link fixed-home">
          <img src="@/assets/assetup.png" alt="Home" style="width: 70px; height: 30px; padding: 0px;">
        </router-link>      </div>
      <div class="auth-links">
        <!-- 금융상품 비교 페이지로 이동 -->
        <RouterLink :to="{ name: 'compare' }" class="nav-link">상품비교</RouterLink> |
        <!-- 환율계산기 -->
        <RouterLink :to="{ name: 'exchange' }" class="nav-link">환율정보</RouterLink> |
        <!-- 카카오맵 보기 -->
        <RouterLink :to="{ name: 'map' }" class="nav-link">은행검색</RouterLink> |
        <!-- 게시판으로 이동 -->
        <RouterLink :to="{ name: 'articles' }" class="nav-link">게시판</RouterLink> |
        <!-- 회원가입 페이지로 이동 -->
        <div v-if="!userStore.isLogin" >
          <RouterLink :to="{ name: 'signup' }" class="nav-link">회원가입</RouterLink>
        </div>
        <div v-if="!userStore.isLogin">|</div>
        <span v-if="!userStore.isLogin">
          <RouterLink :to="{ name: 'login' }" class="nav-link">로그인</RouterLink>
        </span>
        <!-- 프로필 페이지로 이동 -->
        <RouterLink v-if="userStore.isLogin" :to="{ name: 'profile' }" class="nav-link">마이페이지</RouterLink>
        <div v-if="userStore.isLogin">|</div>
        <!-- 로그아웃 -->
        <span v-if="userStore.isLogin" @click="userStore.logOut" class="nav-link">로그아웃</span>
      </div>
    </nav>
  </header>
  <body>
    <RouterView />
    <footer>
      문의 <span style="font-family: 'Courier New', Courier, monospace;">:</span> asthyeon@gmail.com / ggobug94@gmail.com
    </footer>
  </body>
</template>

<script setup>
import { onMounted } from 'vue'
import { RouterLink, RouterView } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { useRecommendStore } from '@/stores/recommend'

const userStore = useUserStore()
const recommendStore = useRecommendStore()

onMounted(() => {
  recommendStore.updateAsset()
  const joinDate = new Date();
  joinDate.setDate(joinDate.getDate() - 365) // 현재 날짜에서 75일 전

  recommendStore.calculateUpdatedPrincipal(200, 5, joinDate)
})
</script>

<style scoped>
@font-face {
  font-family: 'NanumSquareNeo-Variable';
  src: url('https://cdn.jsdelivr.net/gh/projectnoonnu/noonfonts_11-01@1.0/NanumSquareNeo-Variable.woff2') format('woff2');
  font-weight: normal;
  font-style: normal;
}

body {
  font-family: 'NanumSquareNeo-Variable', sans-serif;
  margin: 0;
}

header {
  font-family: 'NanumSquareNeo-Variable', sans-serif;
  background-color: green;
  padding: 10px 20px;
  color: white;

}

#app {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.nav-links {
  display: flex;
  gap: 10px;
  margin-right: auto; /* 나머지 링크들을 왼쪽으로 붙입니다. */
}

.auth-links {
  display: flex;
  gap: 10px;
}

.nav-link {
  color: white;
  text-decoration: none;
}

.nav-link:hover {
  text-decoration: underline;
}

.fixed-home {
  margin-right: auto;
}

footer {
  background-color: green;
  position: relative;
  bottom: 0;
  width: 100%;
  color: white;
  text-align: end;
  padding-right: 20px;
  z-index: 2;
}
</style>