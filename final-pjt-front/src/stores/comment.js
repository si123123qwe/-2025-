import { ref } from 'vue'
import { defineStore } from 'pinia'
import { useUserStore } from '@/stores/user'
import { useArticleStore } from '@/stores/article'
import axios from 'axios'

export const useCommentStore = defineStore('comment', () => {
  const userStore = useUserStore()
  const articleStore = useArticleStore()
  const API_URL = 'http://127.0.0.1:8000'
  const name = userStore.name

  // 댓글 작성 함수
  const commentCreate = function (article_pk, content) {
    axios({
      method: 'post',
      url: `${API_URL}/api/v1/articles/${article_pk}/comments/`,
      data: {
        content
      },
      headers: {
        Authorization: `Token ${userStore.token}`
      }
    })
      .then((res) =>{
        // console.log(res)
        articleStore.articleDetail.comment_set.push(res.data)
      })
      .catch((err) => {
        console.log(err)
      })
  }

  // 댓글 삭제 함수
  const commentDelete = function(comment_pk) {
    axios({
      method: 'delete',
      url: `${API_URL}/api/v1/comments/${comment_pk}`,
      headers: {
        Authorization: `Token ${userStore.token}`
      }
    })
    .then((res) => {
      articleStore.articleDetail.comment_set = articleStore.articleDetail.comment_set.filter((comment) => {
        return comment.id != comment_pk
      })
    })
  }
  return { commentCreate, commentDelete, API_URL, name }
}, { persist: true })
