import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { useRouter } from 'vue-router'
import axios from 'axios'

export const useFinanceStore = defineStore('finance', () => {
  const API_URL = 'http://127.0.0.1:8000'
  const token = ref(null)
  const router = useRouter()

  // 금융회사 목록
  const companys = ref([])
  // 전체 정기예금 상품 목록
  const depositProductList = ref([])
  // 정기예금 옵션 목록
  const depositProductOptionList = ref([])
  // 전체 적금 상품 목록
  const savingProductList = ref([])
  // 적금 옵션 목록
  const savingProductOptionList = ref([])
  const savingOptionList = ref([])
  const productType = ref('')

  // 전체 회사 조회
  const getCompanys = function () {
    axios({
        method: 'get',
        url: `${API_URL}/finances/get-companys/`
    }).then(res => {
        console.log('금융회사 조회 완료')
        companys.value = res.data
    }).catch(err => console.log(err))
  }

  const company = ref({})
  // 단일 회사 조회
  const getCompanyDetail = function (finCoNo) {
    axios({
        method: 'get',
        url: `${API_URL}/finances/get-company-detail/${finCoNo}/`
    }).then(res => {
        console.log('금융회사 조회 완료')
        company.value = res.data
    }).catch(err => console.log(err))
  }

  const filteredProducts = ref([])

  // 예금 상품 검색
  const searchDepositProducts = function (fin_co_no, save_trm) {
      fin_co_no = fin_co_no || '전체'
      save_trm = save_trm || 0
      console.log(fin_co_no, save_trm)
    axios({
        method: 'get',
        url: `${API_URL}/finances/search-deposit-products/${fin_co_no}/${save_trm}/`
    }).then(res => {
        console.log('예금 검색 완료')
        filteredProducts.value = res.data
        productType.value = 'deposit'
    }).catch(err => console.log(err))
  }

  // 적금 상품 검색
  const searchSavingProducts = function (fin_co_no, save_trm) {
      fin_co_no = fin_co_no || '전체'
      save_trm = save_trm || 0
    axios({
        method: 'get',
        url: `${API_URL}/finances/search-saving-products/${fin_co_no}/${save_trm}/`
    }).then(res => {
        console.log('적금 검색 완료')
        filteredProducts.value = res.data
        productType.value = 'saving'
    }).catch(err => console.log(err))
  }

  // 연금 저축 상품 검색
  const searchAnnuitySavingProducts = function (fin_co_no, pnsn_recp_trm) {
      fin_co_no = fin_co_no || '전체'
      pnsn_recp_trm = pnsn_recp_trm || '전체'
    axios({
        method: 'get',
        url: `${API_URL}/finances/search-annuity-saving-products/${fin_co_no}/${pnsn_recp_trm}/`
    }).then(res => {
        console.log('연금 저축 검색 완료')
        filteredProducts.value = res.data
    }).catch(err => console.log(err))
  }

  // 연금 저축 상품 검색
  const searchLoanProducts = function (fin_co_no) {
      fin_co_no = fin_co_no || '전체'
    axios({
        method: 'get',
        url: `${API_URL}/finances/search-loan-products/${fin_co_no}/`
    }).then(res => {
        console.log('대출 상품 검색 완료')
        filteredProducts.value = res.data
    }).catch(err => console.log(err))
  }

  const loanProduct = ref({})
  // 단일 대출 상품 조회
  const getLoanProductDetail = function (finPrdtCd) {
    console.log(finPrdtCd)
    axios({
        method: 'get',
        url: `${API_URL}/finances/get-loan-product-detail/${finPrdtCd}/`,
    }).then(res => {
        console.log('단일 대출 상품 조회 완료')
        loanProduct.value = res.data
        console.log(loanProduct.value)
    }).catch(err => console.log(err))
  }

  // 예금 상품 목록 조회
  const getDepositProducts = function () {
    axios({
        method: 'get',
        url: `${API_URL}/finances/get-deposit-products/`,
    }).then(res => {
        console.log('예금 상품 조회 완료')
        depositProductList.value = res.data
    }).catch(err => console.log(err))
  }
  
  // 적금 상품 목록 조회
  const getSavingProducts = function () {
      axios({
          method: 'get',
          url: `${API_URL}/finances/get-saving-products/`
        }).then(res => {
            console.log('적금 상품 조회 완료')
            savingProductList.value = res.data
        }).catch(err => console.log(err))
    }
    
  const annuitySavingProductList = ref([])

  // 연금 상품 목록 조회
  const getAnnuitySavingProducts = function () {
    axios({
        method: 'get',
        url: `${API_URL}/finances/get-annuity-saving-products/`
    }).then(res => {
        console.log('연금 상품 조회 완료')
        annuitySavingProductList.value = res.data
    }).catch(err => console.log(err))
  }

  const loanProductsList = ref([])
  // 대출 상품 목록 조회
  const getLoanProducts = function () {
    axios({
        method: 'get',
        url: `${API_URL}/finances/get-loan-products/`
    }).then(res => {
        console.log('대출 상품 조회 완료')
        loanProductsList.value = res.data
    }).catch(err => console.log(err))
  }

  // 단일 예금 상품
  const depositProduct = ref(null)
  const savingProduct = ref(null)
  
  // 단일 예금 상품 상세 정보 조회
  const getDepositProductDetail = function (finPrdtCd) {
    axios({
        method: 'get',
        url: `${API_URL}/finances/get-deposit-product-detail/${finPrdtCd}/`
    }).then(res => {
        console.log('단일 예금 상품 상세 조회 성공')
        console.log(res.data)
        depositProduct.value = res.data
        console.log(depositProduct.value[0].product);

    }).catch(err => console.log(err))
  }

  // 단일 적금 상품 상세 정보 조회
  const getSavingProductDetail = function (finPrdtCd) {
    axios({
        method: 'get',
        url: `${API_URL}/finances/get-saving-product-detail/${finPrdtCd}/`
    }).then(res => {
        console.log('단일 적금 상품 상세 조회 성공')
        console.log(res.data)
        savingProduct.value = res.data
    }).catch(err => console.log(err))
  }

  const anniutyProduct = ref(null)
  // 단일 연금 상품 상세 정보 조회
  const getAnnuitySavingProductDetail = function (finPrdtCd) {
    axios({
        method: 'get',
        url: `${API_URL}/finances/get-annuity-saving-product-detail/${finPrdtCd}/`
    }).then(res => {
        console.log('단일 연금 상품 상세 조회 성공')
        anniutyProduct.value = res.data
    }).catch(err => console.log(err))
  }

  // 단일 예금 상품의 옵션 목록 조회
  const getDepositProductOptions = function (finPrdtCd) {
    axios({
        method:'get',
        url: `${API_URL}/finances/get-deposit-product-options/${finPrdtCd}/`
    }).then(res => {
        console.log('단일 예금 상품 옵션 조회 성공');
        depositProductOptionList.value = res.data
    }).catch(err => console.log(err))
  }

  // 단일 적금 상품의 옵션 목록 조회
  const getSavingProductOptions = function (finPrdtCd) {
    axios({
        method:'get',
        url: `${API_URL}/finances/get-saving-product-options/${finPrdtCd}/`
    }).then(res => {
        console.log('단일 적금 상품 옵션 조회 성공');
        savingProductOptionList.value = res.data
        console.log(savingProductOptionList.value)
    }).catch(err => console.log(err))
  }

  const depostiOptionLIst = ref([])

  // 예금 옵션 조회
  const getDepositOptions = function () {
    axios({
        method:'get',
        url: `${API_URL}/finances/get-deposit-options/`
    }).then(res => {
        console.log('예금 상품 옵션 조회 성공')
        depostiOptionLIst.value = res.data

    }).catch(err => console.log(err))
  }

  const getInterestRate = function (options, term) {
    const option = options.find(opt => opt.save_trm === term)
    return option ? option.intr_rate : '--'
  }

  // 열 정렬 상태
  const columnSortStates = {
    dcls_month: false,
    kor_co_nm: false,
    fin_prdt_nm: false,
    6: false,
    12: false,
    24: false,
    36: false,
    pnsn_kind_nm: false,
    prdt_type_nm: false,
    dcls_rate: false,
    avg_prft_rate: false
  }

  // 상품 정렬
  const sortProducts = function (key) {
    console.log(key)
    console.log('정렬되었습니다.')
    const isSorted = columnSortStates[key]

    Object.keys(columnSortStates).forEach(column => {
        if (column !== key) {
            columnSortStates[column] = false
        }
    })

    if (key === 'dcls_month' || key === 'fin_prdt_nm' || key === 'kor_co_nm' || key === 'pnsn_kind_nm' || key === 'prdt_type_nm' || key === 'lend_rate_type_nm' || key === 'rpay_type_nm') {
        filteredProducts.value.sort((a, b) => {
            const valueA = a.product[key]
            const valueB = b.product[key]

            return isSorted ? valueB.localeCompare(valueA) : valueA.localeCompare(valueB)
        })
    } else if (key === 'dcls_rate' || key === 'avg_prft_rate' || key === 'lend_rate_avg') {
        filteredProducts.value.sort((a, b) => {
          const valueA = a.product[key]
          const valueB = b.product[key]

          return isSorted ? valueB - valueA : valueA - valueB
        })
    } else if ([6, 12, 24, 36].includes(key)) {
        const term = Number(key)
        console.log(term)
        filteredProducts.value.sort((a, b) => {
            const optionA = a.options.find(opt => opt.save_trm === term)
            const optionB = b.options.find(opt => opt.save_trm === term)

            if (!optionA) return 1
            if (!optionB) return -1

            if (optionA && optionB) {  
                return isSorted ? optionA.intr_rate - optionB.intr_rate : optionB.intr_rate - optionA.intr_rate
            } else {
                return 0
            }
        })
    }
    columnSortStates[key] = !isSorted
  }

  const allProductList = ref([])

  // 모든 상품 조회 및 저장(옵션 목록 포함)
  const getAllProducts = () => {
    console.log('모든 상품 조회합니다');
    axios({
        method: 'get',
        url: `${API_URL}/finances/get-all-products/`
    }).then((res) => {
        allProductList.value = res.data
        // console.log(allProductList.value);
        console.log('모든 상품이 저장되었습니다.');
    }).catch(err => console.log(err))
  }

  const OneProduct = ref({})
  // 단일 상품 조회
  const getOneProduct = (finPrdtCd) => {
    axios({
        method: 'get',
        url: `${API_URL}/finances/get-all-product-detail/${finPrdtCd}`
    }).then((res) => {
      OneProduct.value = res.data
      console.log(OneProduct.value)
      console.log('단일 상품 조회 완료.')
    }).catch(err => console.log(err))
  }
  
  return {
    companys, company, 
    depositProductList, depositProduct, savingProduct, depostiOptionLIst, depositProductOptionList,
    savingProductList, savingOptionList, productType, savingProductOptionList, allProductList, annuitySavingProductList, OneProduct,
    getCompanys, getDepositProducts, getDepositOptions, getDepositProductOptions, getDepositProductDetail,
    getSavingProducts, getSavingProductOptions,
    getSavingProductDetail,
    filteredProducts, searchDepositProducts, searchSavingProducts, sortProducts, getAllProducts, getAnnuitySavingProducts, getOneProduct,
    searchAnnuitySavingProducts, anniutyProduct, getAnnuitySavingProductDetail, getCompanyDetail, getLoanProducts, loanProductsList, searchLoanProducts, getLoanProductDetail, loanProduct }
}, { persist: true })
