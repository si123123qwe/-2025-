<template>
  <div class="welcome">
<div>
  <h1>게시글수정</h1>
</div>
<div class="product-type-buttons">
  <button @click="goBack">뒤로가기</button>
</div>
</div>
<div style="background-color: gainsboro; padding: 20px;">
  <form @submit.prevent="updateArticle" style="background-color: white; border: 1px solid; border-radius: 10px; padding: 20px; text-align: center;;">
    <!-- 제목 입력 -->
    <div style="margin-bottom: 15px;">
      <label for="title" style="font-weight: bold;">제목</label>
      <input type="text" v-model.trim="updatedArticle.title" id="title" style="width: 100%; padding: 8px; border-radius: 5px; border: 1px solid #ccc;">
    </div>

    <!-- 내용 입력 -->
    <div style="margin-bottom: 15px;">
      <label for="content" style="font-weight: bold;">내용</label>
      <textarea v-model.trim="updatedArticle.content" id="content" style="width: 100%; height: 200px; padding: 8px; border-radius: 5px; border: 1px solid #ccc;"></textarea>
    </div>
    <button class="product-type-buttons-submit" type="submit">게시글수정</button>
  </form>
  <hr>
</div>
</template>

<script setup>
import axios from 'axios'
import { ref, onMounted, watch } from 'vue'
import { useArticleStore } from '@/stores/article'
import { useUserStore } from '@/stores/user'
import { useRouter, useRoute } from 'vue-router'

const store = useArticleStore()
const userStore = useUserStore()
const route = useRoute()
const router = useRouter()
const updatedArticle = ref({ title: '', content: '' })

// 게시글 내용 불러오기
onMounted(() => {
store.getArticleDetail(route.params.article_id)
})

watch(() => store.articleDetail, (val) => {
updatedArticle.value.title = val.title
updatedArticle.value.content = val.content
})

// 게시글 수정 함수
const updateArticle = function () {
axios({
  method: 'put',
  url: `${store.API_URL}/api/v1/articles/${route.params.article_id}/`,
  data: updatedArticle.value,
  headers: {
    Authorization: `Token ${userStore.token}`
  }
})
  .then((res) => {
    console.log(res.data)
    router.push({ name: 'article_detail', params: { id: route.params.article_id } })
  })
  .catch((err) => {
    console.log(err.response.data)
  })
}

// 뒤로 가기
const goBack = function () {
router.back()
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

.product-type-buttons {
margin-bottom: 20px;
}

.product-type-buttons button {
margin-top: 10px;
background-color: #2ecc71;
color: #ffffff;
padding: 8px;
border: none;
cursor: pointer;
transition: background-color 0.3s ease;
border-radius: 5px;
}

.product-type-buttons button:hover {
background-color: #27ae60;
}

.product-type-buttons-submit {
margin-top: 10px;
background-color: #2ecc71;
color: #ffffff;
padding: 8px;
border: none;
cursor: pointer;
transition: background-color 0.3s ease;
border-radius: 5px;
}

.product-type-buttons-submit:hover {
background-color: #27ae60;
}

</style>