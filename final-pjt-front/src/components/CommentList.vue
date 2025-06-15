<template>
  <div>
    <div>
      <strong>{{ cnt }} 번째 댓글 </strong>
      <span>{{ comment.username }} : <span v-if="!isEditing">{{ editedContent }}</span></span>
      
      <!-- 수정 중인 경우 댓글 수정 폼 표시 -->
      <span v-if="isEditing">
        <input v-model.trim="editedContent" id="editedContent" type="text">
        <button style="margin-left: 5px; font-size: 15px; padding: 5px;" @click="saveEditedComment" class="product-type-buttons-submit">저장</button>
        <button style="margin-left: 5px; font-size: 15px; padding: 5px;" @click="cancelEdit" class="product-type-buttons-submit">취소</button>
      </span>
      
      <span v-if="comment.username === store.name">
        <button style="margin-left: 5px; font-size: 15px; padding: 5px;" class="product-type-buttons-submit" @click="toggleEdit" v-if="!isEditing">
          수정
        </button>
        <button style="margin-left: 5px; font-size: 15px; padding: 5px;" class="product-type-buttons-submit" @click="commentDelete">
          삭제
        </button>
      </span>
    </div>
    <hr>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useCommentStore } from '@/stores/comment'
import { useArticleStore } from '@/stores/article'
import axios from 'axios';

const store = useCommentStore()
const articleStore = useArticleStore()
const props = defineProps({
  comment: Object,
  cnt: Number
})

// 댓글 수정 여부를 나타내는 상태
const isEditing = ref(false);

// 수정된 댓글 내용을 저장하는 상태
const editedContent = ref(props.comment.content);

// 댓글 수정 토글 함수
const toggleEdit = function () {
  isEditing.value = !isEditing.value;
}

// 수정된 댓글을 저장하는 함수
const saveEditedComment = function () {
  // API를 호출하여 수정된 내용을 서버에 저장하는 로직을 구현해야 합니다.
  axios({
    method: 'put',
    url: `${store.API_URL}/api/v1/comments/${props.comment.id}/`,
    data: {
      content: editedContent.value
    }
  })
    .then((res) => {
      // 성공적으로 수정된 경우
      const commentId = props.comment.id
      articleStore.articleDetail.comment_set[props.cnt-1] = res.data
      isEditing.value = false
    })
    .catch((err) => {
      console.error(err);
    });
}

// 수정 취소 함수
const cancelEdit = function () {
  // 수정 취소 시, 편집 중인 내용을 원래의 내용으로 되돌립니다.
  editedContent.value = props.comment.content;
  
  // 수정 모드를 종료합니다.
  isEditing.value = false;
}

// 댓글 삭제 함수
const commentDelete = function () {
  store.commentDelete(props.comment.id);
}
</script>

<style scoped>
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