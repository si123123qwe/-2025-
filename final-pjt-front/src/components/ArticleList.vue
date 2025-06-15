<template>
  <div class="search-results">
    <table>
      <thead>
        <tr>
          <th style="width: 100px; text-align: center;">글번호</th>
          <th style="text-align: center;">제목</th>
          <th style="width: 150px; text-align: center;">작성자</th>
        </tr>
      </thead>
      <tbody>
        <tr 
          v-for="(article, index) in revesedArticles"
          :key="article.id"
          :article="article"
        >
          <td style="text-align: center;">{{ store.articles.length - index }}</td>
          <td style="text-align: center;">
            <RouterLink :to="{ name: 'article_detail', params: { article_id: article.id }}">
              {{ article.title }}
            </RouterLink>
          </td>
          <td style="text-align: center;">{{ article.username }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { useArticleStore } from '@/stores/article'
import { RouterLink } from 'vue-router'
import { computed } from 'vue';

const store = useArticleStore()

const revesedArticles = computed(() => {
  return store.articles.slice().reverse()
})
</script>

<style scoped>
.search-results table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 20px;
  border: 1px solid #ddd;
}

.search-results th, .search-results td {
  border: 1px solid #ddd;
  padding: 10px;
  text-align: left;
}

.search-results th {
  background-color: #27ae60;
  color: #ffffff;
  cursor: pointer;
}

.search-results th:hover {
  background-color: #27ae60;
}

.search-results tbody tr:hover {
  background-color: #f5f5f5;
}
</style>