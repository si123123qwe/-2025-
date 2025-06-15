<template>
    <div>
        <!-- 검색하기 옵션 설정 -->
        <div class="search-options">
            <!-- 은행 -->
            <label for="bank">은행 선택:</label>
            <select v-model="selectCompany">
                <option value="">전체</option>
                <option v-for="company in financeStore.companys" :key="company.fin_co_no" :value="company.fin_co_no">{{ company.kor_co_nm }}</option>
            </select>

            <button @click="applyOptions">검색하기</button>
        </div>
  
        <!-- 검색 결과 상품 테이블 -->
        <div class="search-results">
            <table>
              <thead>
                  <tr>
                  <!-- 클릭시 정렬 -->
                  <th @click="financeStore.sortProducts('dcls_month')">공시제출월</th>
                  <th @click="financeStore.sortProducts('kor_co_nm')">금융회사명</th>
                  <th @click="financeStore.sortProducts('fin_prdt_nm')">상품명</th>
                  <th>대출 종류</th>
                  <th>금리 유형</th>
                  <th>평균 금리</th>
                  <th>상환 방식</th>
                  </tr>
              </thead>
              <tbody>
                  <!-- 상품 나열, 클릭 시 상품 상세 페이지로 이동 -->
                  <tr v-for="product in paginatedProducts" :key="product.product.id">
                  <td>{{ product.product.dcls_month }}</td>
                  <td>{{ product.product.kor_co_nm }}</td>
                  <td class="clickable-text" @click="goDetail(product.product.fin_prdt_cd)">{{ product.product.fin_prdt_nm }}</td>

                  <td v-if="'mrtg_type' in product.options[0]">주택 담보 대출</td>
                  <td v-if="'mrtg_type' in product.options[0]">{{ product.options[0].lend_rate_type_nm }}</td>
                  <td v-if="'mrtg_type' in product.options[0]">{{ ((product.options[0].lend_rate_min + product.options[0].lend_rate_max) / 2).toFixed(2) }}%</td>
                  <td v-if="'mrtg_type' in product.options[0]">{{ product.options[0].rpay_type_nm }}</td>

                  <td v-if="'crdt_prdt_type' in product.options[0]">신용 대출</td>
                  <td v-if="'crdt_prdt_type' in product.options[0]">{{ product.options[0].crdt_lend_rate_type_nm }}</td>
                  <td v-if="'crdt_prdt_type' in product.options[0]">{{ product.options[0].crdt_grad_avg }}%</td>
                  <td v-if="'crdt_prdt_type' in product.options[0]">--</td>
                  
                  <td v-if="!product.options[0]['mrtg_type'] && 'rpay_type' in product.options[0]">전세 자금 대출</td>
                  <td v-if="!product.options[0]['mrtg_type'] && 'rpay_type' in product.options[0]">{{ product.options[0].lend_rate_type_nm }}</td>
                  <td v-if="!product.options[0]['mrtg_type'] && 'rpay_type' in product.options[0]">{{ ((product.options[0].lend_rate_min + product.options[0].lend_rate_max) / 2).toFixed(2) }}%</td>
                  <td v-if="!product.options[0]['mrtg_type'] && 'rpay_type' in product.options[0]">{{ product.options[0].rpay_type_nm }}</td>
                  </tr>
              </tbody>
            </table>
    
            <!-- 테이블 페이지 구현 -->
            <div class="pagination">
            <!-- 페이지 이동시 페이지 갱신, 테이블 갱신 -->
            <button v-if="currentPage > 1" @click="changePage(currentPage - 1)">이전</button>
            <button v-for="page in pages" :key="page" @click="changePage(page)" :class="{ active: page === currentPage }">{{ page }}</button>
            <button v-if="currentPage < totalPages" @click="changePage(currentPage + 1)">다음</button>
            </div>
        </div>
    </div>
</template>

<script setup>
  import { ref, onMounted, computed, watch } from 'vue'
  import { useFinanceStore } from '@/stores/finance'
  import { useRouter } from 'vue-router'
  
  const financeStore = useFinanceStore()
  
  onMounted(() => {
    console.log('mounted')
    // 회사 목록 조회
    financeStore.getCompanys()
    // 검색 상품 목록 조회
    financeStore.searchLoanProducts()
  })
  
  // 회사 옵션
  const selectCompany = ref('')    
  const router = useRouter()
    
  // 예금 상품 상세페이지로 이동
  const goDetail = function (finPrdtCd) {
    router.push({name:'loan_product_detail', params:{fin_prdt_cd: finPrdtCd}})
  }
  
  // 검색 결과 상품 목록
  const filteredProducts = computed(() => financeStore.filteredProducts)
    
  // 검색하기 옵션 적용
  const applyOptions = function () {
    const fin_co_no = selectCompany.value || '전체'
    financeStore.searchLoanProducts(fin_co_no)
  }
  
  // 페이지 구현
  const currentPage = ref(1)

  // 한 페이지에 20개의 행만 출력
  const itemsPerPage = 20

  // 총 페이지 계산
  const totalPages = computed(() => Math.ceil(filteredProducts.value.length / itemsPerPage))

  // 페이지
  const pages = computed(() => {
    const pagesArray = []
    for (let i = 1; i <= totalPages.value; i++) {
        pagesArray.push(i)
    }
    return pagesArray
  })
  
  // 현재 페이지에 출력할 상품 목록
  const paginatedProducts = computed(() => {
    const start = (currentPage.value - 1) * itemsPerPage;
    const end = start + itemsPerPage
    return filteredProducts.value.slice(start, end)
  })
  
  // 페이지 갱신
  const changePage = function (page) {
    if (page >= 1 && page <= totalPages.value) {
        currentPage.value = page
    }
  }

</script>

<style scoped>
.search-options {
  margin-bottom: 20px;
  text-align: center;
}

.search-options h3 {
  font-size: 1.5em;
}

.search-options h4 {
  font-size: 1.2em;
  color: #555;
}

.search-options label {
  margin-right: 10px;
}

.search-options select {
  margin-right: 20px;
  padding: 5px;
}

.search-options button {
  background-color: #27ae60;
  color: #ffffff;
  padding: 8px;
  border: none;
  cursor: pointer;
  transition: background-color 0.3s ease;
  border-radius: 5px;
}

.search-options button:hover {
  background-color: green !important;
}

.search-results table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 20px;
  border: 1px solid #ddd;
}

.search-results th, .search-results td {
  border: 1px solid #ddd;
  padding: 10px;
  text-align: center;
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

.clickable-text {
  color: #3498db;
  cursor: pointer;
  transition: color 0.3s ease;
}

.clickable-text:hover {
  color: #2980b9;
}

.pagination {
  margin-top: 20px;
  justify-content: center;
}

.pagination button {
  margin-right: 5px;
  background-color: #27ae60;
  color: #ffffff;
  padding: 8px;
  border: none;
  cursor: pointer;
  transition: background-color 0.3s ease;
  border-radius: 5px;
  width: 50px;
}

.pagination button:hover {
  background-color: green !important;
}

.pagination button.active {
  font-weight: bold;
}

</style>