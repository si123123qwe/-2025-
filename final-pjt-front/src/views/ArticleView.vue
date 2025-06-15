<template>
  <div class="welcome">
  <h1>게시판</h1>
  <p>다른 이용자와 소통할 수 있습니다</p>
  <RouterLink v-if="userStore.isLogin" :to="{ name: 'article_create' }" class="create-link">
    게시글작성
  </RouterLink>
</div>
<div style="background-color: gainsboro; padding: 20px">
  <div class="board-container">
    
    <div v-if="store.articles.length > 0">
      <ArticleList :articles="store.articles" />
    </div>
    <div v-else>
      <h3 class="no-articles-message" style="text-align: center;">글이 없습니다</h3>
    </div>
  </div>
  <p>　</p>
  <p>　</p>
  <p>　</p>
  <p>　</p>
  <p>　</p>
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
import { onMounted } from 'vue'
import { useArticleStore } from '@/stores/article'
import { useUserStore } from '@/stores/user'
import { RouterLink } from 'vue-router'
import ArticleList from '@/components/ArticleList.vue'

const store = useArticleStore()
const userStore = useUserStore()

onMounted(() => {
  store.getArticles()
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
.board-container {
  max-width: 800px;
  margin: auto;
  padding: 20px;
  background-color: white;
  border: 1px solid;
  border-radius: 10px;
}

.create-link {
  margin-bottom: 10px;
  display: inline-block;
  text-decoration: none;
  padding: 5px 10px;
  background-color: rgb(70, 213, 91);
  color: #fff;
  border-radius: 5px;
}

.create-link:hover {
  background-color: rgb(86, 222, 95) !important;
}

.no-articles-message {
  color: #888;
}
</style>