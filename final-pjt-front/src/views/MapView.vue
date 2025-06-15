<template>
  <div class="welcome">
  <h1>은행검색</h1>
  <p>선택지역 및 회원장소 주변 은행을 검색할 수 있습니다</p>
</div>
<div style="background-color: gainsboro; padding: 20px;">
  <div style="background-color: white; border: 1px solid; border-radius: 10px;">
  <div id="app" class="" style="z-index: 1;">
    <KakaoMap class="kakao-map" />
  </div>
</div>
</div>
</template>

<script>
import KakaoMap from "@/components/KakaoMap.vue";

export default {
  name: "App",
  components: {
    KakaoMap,
  },
};
</script>

<style scoped>
.welcome {
  background-image: url('@/assets/upup2.png');
  background-size: 150px; /* 배경 이미지를 커버하도록 설정 */
  background-repeat: no-repeat;
  background-position: 10px; /* 이미지를 가운데 정렬 */
  padding: 20px;
  border-bottom: 20px solid green;
  background-color: white;
  text-align: end;
  height: 160px;
}
</style>
