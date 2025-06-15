<template>
  <div>
    <h4>{{ index }} 번째 글</h4>
    <p>작성자 : {{ article.username }}</p>
    <p>제목 : {{ article.title }}</p>
    <p>내용 : {{ article.content }}</p>
    <RouterLink :to="{ name: 'article_detail', params: { article_id: articleId }}">
      [Detail]
    </RouterLink>
    <hr>
  </div>
</template>

<script setup>
import { RouterLink } from 'vue-router'

const props = defineProps({
  article: Object,
  index: Number
})

const articleId = props.article.id

console.log(props.article.id);

</script>
