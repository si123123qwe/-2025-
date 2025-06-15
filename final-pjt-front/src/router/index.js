import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/stores/user'
import MainView from '@/views/MainView.vue'
import SignUpView from '@/views/SignUpView.vue'
import LogInView from '@/views/LogInView.vue'
import ArticleView from '@/views/ArticleView.vue'
import ArticleCreateView from '@/views/ArticleCreateView.vue'
import ArticleDetailView from '@/views/ArticleDetailView.vue'
import ArticleUpdateView from '@/views/ArticleUpdateView.vue'
import MapView from '@/views/MapView.vue'
import ExchangeView from '@/views/ExchangeView.vue'
import FinanceComparsionView from '@/views/FinanceComparsionView.vue'
import DepositProductDetailView from '@/views/ProductDetail/DepositProductDetailView.vue'
import SavingProductDetailView from '@/views/ProductDetail/SavingProductDetailView.vue'
import ProfileView from '@/views/ProfileView.vue'
import UserUpdateView from '@/views/UserUpdateView.vue'
import PortfolioUpdate from '@/components/PortfolioUpdate.vue'
import TopMbti from '@/components/TopMbti.vue'
import TopAgeGender from '@/components/TopAgeGender.vue'
import RecommendProduct from '@/components/RecommendProduct.vue'
import BasicInfoUpdate from '@/components/BasicInfoUpdate.vue'
import ChartLine from '@/components/ChartLine.vue'
import SubscribeProductView from '@/views/ProductView/SubscribeProductView.vue'
import ProductView from '@/views/ProductView.vue'
import FinanceProductView from '@/views/ProductView/FinanceProductView.vue'
import AnnuityProductDetailView from '@/views/ProductDetail/AnnuityProductDetailView.vue'
import LoanProductDetailView from '@/views/ProductDetail/LoanProductDetailView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'main',
      component: MainView
    },
    {
      path: '/compare',
      name: 'compare',
      component: FinanceProductView
    },
    {
      path: '/deposit-product-detail/:fin_prdt_cd',
      name: 'deposit_product_detail',
      component: DepositProductDetailView
    },
    {
      path: '/saving-product-detail/:fin_prdt_cd',
      name: 'saving_product_detail',
      component: SavingProductDetailView
    },
    {
      path: '/annuity-saving-product-detail/:fin_prdt_cd',
      name: 'annuity_saving_product_detail',
      component: AnnuityProductDetailView
    },
    {
      path: '/loan-product-detail/:fin_prdt_cd',
      name: 'loan_product_detail',
      component: LoanProductDetailView
    },
    {
		path: '/signup',
		name: 'signup',
		component: SignUpView
		},
    {
		path: '/login',
		name: 'login',
		component: LogInView
		},
    {
		path: '/profile',
		name: 'profile',
		component: ProfileView
		},
    {
		path: '/basic-info',
		name: 'basic-info',
		component: BasicInfoUpdate
		},
    {
		path: '/protfolio',
		name: 'portfolio',
		component: PortfolioUpdate
		},
    {
		path: '/update',
		name: 'update',
		component: UserUpdateView
	},
	{
		path: '/articles',
		name: 'articles',
		component: ArticleView
	},
    {
		path: '/article-create',
		name: 'article_create',
		component: ArticleCreateView
	},
    {
		path: '/article-detail/:article_id',
		name: 'article_detail',
		component: ArticleDetailView
	},
	{
		path: '/article-update/:article_id',
		name: 'article_update',
		component: ArticleUpdateView
	},
    {
		path: '/map',
		name: 'map',
		component: MapView
	},
    {
		path: '/exchange',
		name: 'exchange',
		component: ExchangeView
	},
    {
		path: '/age-gender',
		name: 'age-gender',
		component: TopAgeGender
	},
    {
		path: '/mbti',
		name: 'mbti',
		component: TopMbti
	},
    {
		path: '/recommend',
		name: 'recommend',
		component: RecommendProduct
	},
    {
		path: '/subscription',
		name: 'subscription',
		component: ChartLine
	},
    {
		path: '/subscribe/:fin_prdt_cd',
		name: 'subscribe',
		component: SubscribeProductView
	},
	{
		path: '/product',
		name: 'product',
		component: ProductView
	},
  ]
})

// 메인페이지 로그인 상태로만 이용 가능
router.beforeEach((to, from) => {
  const userStore = useUserStore()
  if ((to.name === 'signup' || to.name === 'login') && (userStore.isLogin)) {
    window.alert('이미 로그인이 되어있습니다.')
    return { name: 'login' }
  }
  if ((to.name === 'exchange' || to.name === 'map') && (!userStore.isLogin)) {
    window.alert('로그인이 필요합니다.')
    return { name: 'login' }
  }
  // 여기서 특정 조건을 확인하여 이동을 막을 수 있습니다.
  if (to.name === 'product') {
    // 특정 조건을 확인하여 이동을 막는 경우
    // 예를 들어, 로그인하지 않은 경우
    const userStore = useUserStore();
    if (!userStore.isLogin) {
      window.alert('로그인이 필요합니다.');
      next(false); // 이동을 막습니다.
      return;
    }
  }
})
export default router
