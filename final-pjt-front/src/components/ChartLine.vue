<template>
  <!-- 가입 상품 -->
  <div style="background-color: white; border: 1px solid; border-radius: 10px; padding: 20px; text-align: center;">
    <h1>내가 가입한 상품</h1>
    <div class="chart-container">
      <canvas id="lineChart" width="100" height="100"></canvas>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Chart, LineController, LinearScale, PointElement, LineElement, CategoryScale } from 'chart.js'
import { useUserStore } from '@/stores/user'
import { useFinanceStore } from '@/stores/finance'
import { useRecommendStore } from '@/stores/recommend'

Chart.register(LineController, LinearScale, PointElement, LineElement, CategoryScale)

const userStore = useUserStore()
const financeStore = useFinanceStore()
const recommendStore = useRecommendStore()

const chartData = ref({
  labels: [],
  datasets: [],
})

const saveTrms = [6, 12, 24, 36]

onMounted(() => {
  financeStore.getAllProducts()
  generateChartData()
  drawLineChart()
});

const generateChartData = () => {
  userStore.user.financial_products.forEach(product => {

    const productChartData = {
      labels: [],
      datasets: [],
    }
    let data = []
    let productDetail
    let saveTrm

    // 상품 코드가 일치하는 상품 정보 가져오기
    financeStore.getOneProduct(product[1])

    // 금리 유형, 금리, 최고 우대 금리 구하기
    for (const term of [6, 12, 24, 36]) {
      // 모든 예치 기간 순회
      productDetail = recommendStore.calculateAssetGrowthRate(product[1], term)
      // 맨 처음에 구한 값으로 결정
      if (productDetail) {
        saveTrm = term // 예치기간 할당
        break
      }
    }

    // 함수에서 올바른 결과가 나오지 않으면 종료
    if (!productDetail) {
      console.error('Error calculating asset growth rate for product:', product[1])
      return 
    }
    
    // 금리 유형, 금리, 최고 우대 금리 할당
    const { intr_rate_type_nm, interestRate, interestRate2 } = productDetail

    const currentDate = new Date () // 현재 날짜
    const joinDate = new Date(
      2000 + parseInt(product[0].substring(0, 2)),
      parseInt(product[0].substring(2, 4)) - 1,
      parseInt(product[0].substring(4, 6))
    ) // 상품 가입일

    // x축 라벨 생성 (현재 날짜부터 6개월)
    for (let i = 0; i <= 5; i++) {
      const currentLabelDate = new Date(currentDate)
      currentLabelDate.setMonth(currentLabelDate.getMonth() + i)
      productChartData.labels.push(`${currentLabelDate.getFullYear()}-${(currentLabelDate.getMonth() + 1).toString().padStart(2, '0')}`)
    }

    for (let i = 0; i < saveTrm; i++) {
      // 예치 기간
      const currentDepositPeriod = i + 1
      let cumulativeInterest
      const endDate = new Date(joinDate.getFullYear(), joinDate.getMonth() + currentDepositPeriod, joinDate.getDate())

      // 예치금 혹은 월납입금
      const monthlyDeposit = product[2]

      // 가입일로부터 몇 개월이 지났는지 계산
      const monthsSinceJoin = (currentDate.getFullYear() - joinDate.getFullYear()) * 12 + currentDate.getMonth() - joinDate.getMonth()

      // 해당 기간에 속하는 데이터만 계산
      if (monthsSinceJoin >= 0 && monthsSinceJoin < saveTrm) {
        cumulativeInterest = 0 // 누적 이자 초기화
        // 예금
        if (financeStore.OneProduct.product.fin_prdt_nm.includes('예금')) {
          if (intr_rate_type_nm === '단리') {
            // 단리
            cumulativeInterest = recommendStore.calculateDailyInterest(monthlyDeposit, interestRate, currentDepositPeriod * 30)
            console.log(cumulativeInterest)
          } else {
            // 복리
            cumulativeInterest = recommendStore.calculateCompoundInterestDaily(monthlyDeposit, interestRate, currentDepositPeriod * 30)
            console.log(cumulativeInterest)
          }
        } else {
          // 적금
          if (intr_rate_type_nm === '단리') {
            // 단리
            cumulativeInterest = recommendStore.calculateSimpleInterest(monthlyDeposit, interestRate, joinDate, endDate)
          } else {
            // 복리
            cumulativeInterest = recommendStore.calculateUpdatedPrincipal(monthlyDeposit, interestRate, joinDate, endDate)
          }
        }
        // 각 상품별 가입일자를 기준으로 하기
        const startLabelIndex = productChartData.labels.indexOf(`${joinDate.getFullYear()}-${(joinDate.getMonth() + 1).toString().padStart(2, '0')}`)

        // 데이터 삽입
        productChartData.datasets.push({ x: productChartData.labels[startLabelIndex + i], y: cumulativeInterest })
      }
    }

    chartData.value.datasets.push({
      label: financeStore.OneProduct.product.kor_co_nm,
      borderColor: `rgba(${Math.floor(Math.random() * 256)}, ${Math.floor(Math.random() * 256)}, ${Math.floor(
        Math.random() * 256
      )}, 1)`,
      borderWidth: 1.5,
      data: productChartData.datasets,
    })
    if (chartData.value.labels.length === 0) {
      chartData.value.labels = productChartData.labels
    }
  })
}

// 차트 그리기
const drawLineChart = () => {
  const ctx = document.getElementById('lineChart').getContext('2d')
  new Chart(ctx, {
    type: 'line',
    data: chartData.value,
    options: {
      responsive: true,
      maintainAspectRatio: true,
      plugins: {
        title: {
          display: true,
          text: '상품별 누적 이자', // 원하는 차트 상단의 제목을 설정
          position: 'top', // 상단에 표시하도록 설정
          font: {
            size: 16,
          },
        },
      },
      tooltip: {
        mode: 'nearest', // 가장 가까운 데이터로 툴팁을 표시
        intersect: false, // 선이 교차할 때만 툴팁을 표시
      },
      scales: {
        y: {
          axis: 'y',
          display:true,
          title: {
            display: true,
            align: 'end',   // 끝에 출력
            color: '#808080',
            font: {
              size: 12,
              family: "'Noto Sans KR', sans-serif",
              weight: 300,
            },
            text: '단위 : 만원' // 단위 표시
          },
          beginAtZero: false,
          callback: (value) => `₩${value.toFixed(2)} 만원`,
        },
        x: {
          type: 'category',
        },
      },
    },
  })
}
</script>

<style scoped>
.chart-container {
  max-width: 1000px; /* 원하는 최대 너비 설정 */
  max-height: 600px; /* 원하는 최대 높이 설정 */
  margin: auto; /* 가운데 정렬을 위한 마진 설정 */
}
.container {
  text-align: center;
}
</style>
