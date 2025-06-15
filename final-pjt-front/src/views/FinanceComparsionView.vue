<template>
  <div class="comparison-container">
    <h1>금융상품 비교</h1>

    <!-- 상품 유형 선택 버튼 -->
    <div class="product-type-buttons">
      <button @click="changeToDeposit" :class="{ active: productType === 'deposit' }">정기예금</button>
      <button @click="changeToSaving" :class="{ active: productType === 'saving' }">적금</button>
    </div>

    <!-- 검색하기 옵션 설정 -->
    <div class="search-options">
      <h3>검색하기</h3>
      <h4>검색조건을 입력하세요</h4>
      <label for="bank">은행 선택:</label>
      <select v-model="selectCompany">
        <option value="">전체</option>
        <option v-for="company in financeStore.companys" :key="company.fin_co_no" :value="company.fin_co_no">{{ company.kor_co_nm }}</option>
      </select>

      <label for="term">예치기간 선택:</label>
      <select v-model="selectedTerm">
        <option value="">전체</option> 
        <option v-for="term in terms" :key="term" :value="term">{{ term }}개월</option>
      </select>

      <button @click="applyOptions">검색하기</button>
    </div>

    <!-- 검색 결과 상품 테이블 -->
    <div class="search-results">
      <table>
        <thead>
          <tr>
            <!-- 클릭시 정렬 (금리 : 내림차순, 나머지 컬럼 : 오름차순 정렬, 이미 정렬된 상태일 경우 토글 : 내림차순 <-> 오름차순) -->
            <th @click="financeStore.sortProducts('dcls_month')">공시제출월</th>
            <th @click="financeStore.sortProducts('kor_co_nm')">금융회사명</th>
            <th @click="financeStore.sortProducts('fin_prdt_nm')">상품명</th>
            <!-- 예치기간 -->
            <th v-for="term in selectedTerms" :key="term" @click="financeStore.sortProducts(term)">
              {{ term }}개월 금리
            </th>
          </tr>
        </thead>
        <tbody>
          <!-- 상품 나열, 클릭 시 상품 상세 페이지로 이동 -->
          <tr v-for="product in paginatedProducts" :key="product.product.id" @click="goDetail(product.product.fin_prdt_cd)">
            <td>{{ product.product.dcls_month }}</td>
            <td>{{ product.product.kor_co_nm }}</td>
            <td>{{ product.product.fin_prdt_nm }}</td>
            <!-- 금리는 상품의 옵션에서 가져오기 -->
            <td v-for="term in selectedTerms" :key="term">
              {{ getInterestRate(product.options, term) || '--' }}
            </td>
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
import { useRouter, RouterLink } from 'vue-router'


const financeStore = useFinanceStore()

onMounted(() => {
  console.log('mounted')
  // 회사 목록 조회
  financeStore.getCompanys()
  // 적금 상품 목록 조회
  financeStore.getSavingProducts()
  // 예금 상품 목록 조회
  financeStore.getDepositProducts()
  // 검색 상품 목록 조회
  financeStore.searchDepositProducts()
})

// 회사 옵션
const selectCompany = ref('')    
const selectedTerm = ref('')
const terms = [6, 12, 24, 36]

const router = useRouter()

const productType = ref('deposit')

const changeToDeposit = function () {
  productType.value = 'deposit'
  financeStore.searchDepositProducts()
}

const changeToSaving = function () {
  productType.value = 'saving'
  financeStore.searchSavingProducts()
}

// 상품 상세페이지로 이동
const goDetail = function (finPrdtCd) {
  if (productType.value === 'deposit') {
    router.push({name:'deposit_product_detail', params:{fin_prdt_cd: finPrdtCd}})
  } else {
    router.push({name:'saving_product_detail', params:{fin_prdt_cd: finPrdtCd}})
  }
}

// 금리 가져오기
const getInterestRate = function (options, term) {
  const option = options.find(opt => opt.save_trm === term);
  // -1인 경우나 빈 값인 경우에는 '--'으로 반환
  return option && option.intr_rate !== '-1' ? `${option.intr_rate}%` : '--';
}

// 검색 결과 상품 목록
const filteredProducts = computed(() => financeStore.filteredProducts)

// 예치기간 목록
const selectedTerms = ref(selectedTerm.value ? [Number(selectedTerm.value)] : terms)

// 검색 결과 조회 상품 목록이 갱신되면 예치기간 목록도 갱신
watch(() => filteredProducts.value, () => {
selectedTerms.value = selectedTerm.value ? [Number(selectedTerm.value)] : terms
});

// 검색하기 옵션 적용
const applyOptions = function (type) {
  const fin_co_no = selectCompany.value || '전체'
  const save_trm = selectedTerm.value ? Number(selectedTerm.value) : 0
  if (type == 'deposit') {
    financeStore.searchDepositProducts(fin_co_no, save_trm)
  } else {
    financeStore.searchSavingProducts(fin_co_no, save_trm)
  }
}

// 페이지 구현
const currentPage = ref(1)
// 한 페이지에 20개의 행만 출력
const itemsPerPage = 20
// 총 페이지 계산
const totalPages = computed(() => Math.ceil(filteredProducts.value.length / itemsPerPage))
// 
const pages = computed(() => {
const pagesArray = []
for (let i = 1; i <= totalPages.value; i++) {
  pagesArray.push(i)
}
return pagesArray
});

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
/* 스타일이 필요한 경우 추가 */
.comparison-container {
  background-color: white;
  padding: 20px;
  border-radius: 5px;
  margin-bottom: 20px;
}

.product-type-buttons {
  margin-bottom: 20px;
}

.product-type-buttons button {
  margin-right: 10px;
  background-color: #2ecc71;
  color: #ffffff;
  padding: 8px;
  border: none;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.product-type-buttons button:hover {
  background-color: #27ae60;
}

.search-options {
  margin-bottom: 20px;
}

.search-options label {
  margin-right: 10px;
}

.search-options select {
  margin-right: 20px;
  padding: 5px;
}

.search-options button {
  background-color: #3498db;
  color: #ffffff;
  padding: 8px;
  border: none;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.search-options button:hover {
  background-color: #2980b9;
}

.search-results {
  /* 스크롤이 필요한 경우 설정 */
  /* max-height: 400px;
  overflow-y: auto; */
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 20px;
}

table, th, td {
  border: 1px solid #ddd;
}

th, td {
  padding: 10px;
  text-align: left;
}

th {
  background-color: #f2f2f2;
}

.pagination {
  margin-top: 20px;
}

.pagination button {
  margin-right: 5px;
}

.pagination button.active {
  font-weight: bold;
}
</style>