<template>
    <div class="welcome">
  <div>
    <h1>게시글상세</h1>
  </div>
  <div class="product-type-buttons">
    <button @click="goBack">뒤로가기</button>
  </div>
</div>
  <div style="background-color: gainsboro; padding: 20px;">
    <div style="background-color: white; border: 1px solid; border-radius: 10px; padding: 20px;">
    <div v-if="store.articleDetail">
      <p>작성자 : {{ store.articleDetail.username }}</p>
      <p>제목 : {{ store.articleDetail.title }}</p>
      <p>내용 : {{ store.articleDetail.content }}</p>
      <p>작성일 : {{ store.articleDetail.created_at }}</p>
      <p>수정일 : {{ store.articleDetail.updated_at }}</p>
      <div>
        <p>좋아요 : {{ likeCnt }}</p>
      </div>
      <div v-if="userStore.isLogin && (store.articleDetail.username != userStore.name)">
        <button class="product-type-buttons-submit" @click="toggleLike">
          {{ likeButtonText }}
        </button>
      </div>
      <div v-if="store.articleDetail.username === userStore.name">
        <button style="margin-right: 5px; padding: 5px; margin-left: 5px;" class="product-type-buttons-submit" @click="goUpdate">게시글수정</button>
        <button style="padding: 5px; margin-left: 5px;" class="product-type-buttons-submit" @click="articleDelete">게시글삭제</button>
      </div>
      <hr>
      <hr>
      <h4>댓글 목록</h4>
      <hr>
      <div>
        <CommentList 
          v-for="(comment, index) in store.articleDetail.comment_set"
          :key="comment.id"
          :comment="comment"
          :cnt="index + 1"
        />
      </div>
      <hr>
      <div v-if="userStore.isLogin">
        <h4>댓글 작성</h4>
        <hr>
        <form @submit.prevent="commentCreate">
          <label for="content">댓글</label>
          <input style="margin-left: 5px;" type="text" v-model.trim="newComment" id="content">
          <input style="font-size: 15px; padding: 5px; margin-left: 5px;" type="submit" value="작성" class="product-type-buttons-submit">
        </form>
      </div>
    </div>
  </div>
  <p>　</p>
  </div>
</template>

<script setup>
import axios from 'axios'
import { onMounted, ref, computed, watch } from 'vue'
import { useArticleStore } from '@/stores/article'
import { useCommentStore } from '@/stores/comment'
import { useUserStore } from '@/stores/user'
import { useRouter, useRoute } from 'vue-router'
import CommentList from '@/components/CommentList.vue'

const store = useArticleStore()
const commentStore = useCommentStore()
const userStore = useUserStore()
const route = useRoute()
const router = useRouter()
const newComment = ref('')
const cnt = ref(0)

onMounted(() => {
  store.getArticleDetail(route.params.article_id)
})

// 게시글 업데이트 함수
const goUpdate = function () {
  router.push({ name: 'article_update', params: { article_id: route.params.article_id }})
}

// 게시글 삭제 함수
const articleDelete = function () {
  store.articleDelete(route.params.article_id)
}

// 좋아요 함수
const toggleLike = function () {
  axios({
    method: 'post',
    url: `${store.API_URL}/api/v1/articles/${route.params.article_id}/like/`,
    data: {
      is_liked: !store.articleDetail.like_authors?.includes(userStore.name),
    },
    headers: {
      Authorization: `Token ${userStore.token}`,
    },
  })
    .then((res) => {
      console.log(res.data);

      // 서버 응답에서 is_liked와 like_users 값을 반영      
      if (res.data.is_liked){
        store.articleDetail.like_authors.push(userStore.user.id)
      } else {
        const indexToRemove = store.articleDetail.like_authors.indexOf(userStore.user.id)
        if (indexToRemove !== -1) {
          store.articleDetail.like_authors.splice(indexToRemove, 1);
        }
      }
    })
    .catch((err) => {
      console.log(err)
    });
}

// 댓글 작성 함수
const commentCreate = function () {
  commentStore.commentCreate(route.params.article_id, newComment.value)
  newComment.value = ''
  cnt.value += 1
}

// 뒤로 가기
const goBack = function () {
  router.back()
}

const likeCnt = computed(() => {
  return (store.articleDetail.like_authors || []).length
})

// 좋아요 버튼 텍스트를 계산하는 computed 속성 추가
const likeButtonText = computed(() => {
  if (store.articleDetail.like_authors && store.articleDetail.like_authors.includes(userStore.user.id)) {
    return '좋아요 취소'
  } else {
    return '좋아요'
  }
});

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
