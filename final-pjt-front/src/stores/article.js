import { ref } from 'vue'
import { defineStore } from 'pinia'
import { useUserStore } from '@/stores/user'
import axios from 'axios'
import router from '../router'

export const useArticleStore = defineStore('article', () => {
  const userStore = useUserStore()
  const articles = ref([])
  const API_URL = 'http://127.0.0.1:8000'
  const name = userStore.name

  // 게시글 전체 불러오기
  const getArticles = function () {
    axios({
      method: 'get',
      url: `${API_URL}/api/v1/articles/`,
      headers: {
        Authorization: `Token ${userStore.token}`
      }
    })
      .then((res) =>{
        console.log(res.data)
        articles.value = res.data
      })
      .catch((err) => {
        console.log(err)
      })
  }

  // 게시글 단일 불러오기
  const articleDetail = ref([])
  const getArticleDetail = function (article_pk) {
    axios({
      method: 'get',
      url: `${API_URL}/api/v1/articles/${article_pk}`,
      headers: {
        Authorization: `Token ${userStore.token}`
      }
    })
    .then((res) => {
      articleDetail.value = res.data
      console.log(articleDetail.value);
    })
    .catch((err) => {
      console.log(err);
    })
  }

  // 게시글 단일 삭제
  const articleDelete = function (article_pk) {
    axios({
      method: 'delete',
      url: `${API_URL}/api/v1/articles/${article_pk}`,
      headers: {
        Authorization: `Token ${userStore.token}`
      }
    })
    .then((res) => {
      // const storedData = localStorage.getItem('article');
      // if (storedData) {
      //   // 로컬 스토리지에서 데이터를 가져와서 파싱
      //   const data = JSON.parse(storedData);
  
      //   // 삭제할 상품의 productCode를 사용하여 배열에서 해당 아이템 찾기
      //   const indexToRemove = data.findIndex(item => item.id === article_pk);
  
      //   // 해당 아이템이 존재하면 배열에서 삭제
      //   if (indexToRemove !== -1) {
      //     data.splice(indexToRemove, 1);
  
      //     // 배열을 다시 로컬 스토리지에 저장
      //     localStorage.setItem('article', JSON.stringify(data));
      //   }
      // }
      router.push({ name: 'articles' })
    })
  }

  return { articles, articleDetail, getArticles, getArticleDetail, articleDelete, API_URL, name }
}, { persist: true })
