<template>
  <div style="padding-left: 50px; padding-top: 20px;">

    <form @submit.prevent="moveTo">
      <select name="" id="" v-model="citySelected" @change="getDistrict(citySelected)">
        <option value="">시/도</option>
        <option 
          v-for="city in store.infos.result"
          :key="city.cd"
          :value="{ cd: city.cd, addr_name: city.addr_name }"
        >
          {{ city.addr_name }}
        </option>
      </select>
      <select name="" id="" v-model="districtSelected" @change="getDong(districtSelected)">
        <option value="">시/군/구</option>
        <option 
          v-for="district in districts"
          :key="district.cd"
          :value="{ cd: district.cd, addr_name: district.addr_name}"
        >
          {{ district.addr_name }}
        </option>
      </select>
      <select name="" id="" v-model="dongSelected" @change="getAddress()">
        <option value="">읍/면/동</option>
        <option 
          v-for="dong in dongs"
          :key="dong.cd"
          :value="dong.addr_name"
        >
          {{ dong.addr_name }}
        </option>
      </select>
      <select name="" id="" v-model="bankSelected" @change="getAddress()">
        <option value="">전체</option>
        <option 
          v-for="company in financeStore.companys"
          :key="company.fin_co_no"
          :value="company.kor_co_nm"
        >
          {{ company.kor_co_nm }}
        </option>
      </select>
      |
      <button class="btn btn-success" style="font-size: 10px; padding: 5px;" type="submit">검색</button>
      |
      <button class="btn btn-success" style="font-size: 10px; padding: 5px;" type="button" @click="searchHome">우리집근처</button>
    </form>
    <hr>
    <div class="map_wrap">
      <div id="map" style="position:relative;overflow:hidden;"></div>

      <div id="menu_wrap" class="bg_white">
          <div class="option">
          </div>
          <ul id="placesList"></ul>
          <div id="pagination"></div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useAddressStore } from '@/stores/address'
import { useFinanceStore } from '@/stores/finance'
import { useUserStore } from '@/stores/user'
import axios from 'axios'

export default {
  name: "KakaoMap",
  data() {
    return {
      // map 객체 설정
      map: null,
      markers: [],
      infowindow: null,
    };
  },
  setup() {
    const citySelected = ref('')
    const districts = ref(null)
    const districtSelected = ref('')
    const financeStore = useFinanceStore()
    const store = useAddressStore()
    const userStore = useUserStore()
    const address = ref('')
    const address2 = ref('')
    const bankSelected = ref('')
    const dongs = ref(null)
    const dongSelected = ref('')
    const cit = ref('')
    const dis = ref('')
    const don = ref('')
    const ban = ref('')

    // '구'를 얻는 함수
    const getDistrict = function (citySelected) {
      dis.value = ''
      don.value = ''
      districtSelected.value = ''
      dongSelected.value = ''
      districts.value = ''
      dongs.value = ''
      axios({
        method: 'get',
        url: `https://sgisapi.kostat.go.kr/OpenAPI3/addr/stage.json?accessToken=${store.token}&cd=${citySelected.cd}`
      })
      .then((res) => {
        districts.value = res.data.result
        if (citySelected) {
          cit.value = citySelected.addr_name  
        } else {
          cit.value = ''
        }
        address.value = cit.value + dis.value + don.value
        address2.value = cit.value + dis.value + don.value + ban.value
        console.log(address);
        console.log(address2);
      })
      .catch((err) => {
        console.log(err);
      })
    }

    // '동'을 얻는 함수
    const getDong = function (districtSelected) {
      don.value = ''
      dongs.value = ''
      dongSelected.value = ''
      axios({
        method: 'get',
        url: `https://sgisapi.kostat.go.kr/OpenAPI3/addr/stage.json?accessToken=${store.token}&cd=${districtSelected.cd}`
      })
      .then((res) => {
        dongs.value = res.data.result
        if (districtSelected) {
          dis.value = districtSelected.addr_name  
        } else {
          dis.value = ''  
        }
        address.value = cit.value + dis.value + don.value
        address2.value = cit.value + dis.value + don.value + ban.value
        console.log(address);
        console.log(address2);
      })
      .catch((err) => {
        console.log(err);
      })
    }

    // 검색할 주소 얻기
    const getAddress = function () {
      don.value = dongSelected.value
      ban.value = bankSelected.value
      address.value = cit.value + dis.value + don.value
      address2.value = cit.value + dis.value + don.value + ban.value
      console.log(address);
      console.log(address2);
    }

    const removeCity = function () {
      cit.value = ''
    }

    return {
      citySelected, 
      districts,
      districtSelected, 
      bankSelected,
      dongs,
      dongSelected,
      store,
      getDistrict,
      address,
      address2,
      getAddress,
      financeStore,
      getDong,
      cit,
      dis,
      don,
      ban,
      removeCity,
      userStore,
    }

  },
  mounted() {
    if (window.kakao && window.kakao.maps) {
      this.initMap();
    } else {
      const script = document.createElement("script");
      const API_KEY = import.meta.env.VITE_KAKAO_API_KEY;
      script.src = `//dapi.kakao.com/v2/maps/sdk.js?appkey=${API_KEY}&libraries=services,clusterer,drawing&autoload=false`;
      script.onload = () => window.kakao.maps.load(this.initMap); 

      document.head.appendChild(script);
    }
  },
  methods: {
    initMap() {
      const self = this 

      // 주소-좌표 변환 객체를 생성합니다
      var geocoder = new kakao.maps.services.Geocoder();

      console.log(1);
      
      // 주소로 좌표를 검색합니다
      geocoder.addressSearch(self.userStore.user.address, function(result, status) {
        console.log(2);
        // 정상적으로 검색이 완료됐으면 
        if (status === kakao.maps.services.Status.OK) {
          console.log(3);
          var coords = new kakao.maps.LatLng(result[0].y, result[0].x);

          
          // console.log(coords);
          console.log(self.userStore.user.address);
          const container = document.getElementById("map");
          const options = {
            center: coords,
            level: 4,
          };
          
          //지도 객체를 등록합니다.
          //지도 객체는 반응형 관리 대상이 아니므로 initMap에서 선언합니다.
          self.map = new kakao.maps.Map(container, options);
          
          // 결과값으로 받은 위치를 마커로 표시합니다
          var marker = new kakao.maps.Marker({
            map: self.map,
            position: coords
          });
          self.infowindow = new kakao.maps.InfoWindow({});          
          // 마커와 검색결과 항목에 mouseover 했을때
          // 해당 장소에 인포윈도우에 장소명을 표시합니다
          // mouseout 했을 때는 인포윈도우를 닫습니다
          kakao.maps.event.addListener(marker, 'mouseover', function() {
            var content = '<div style="width:150px;text-align:center;padding:6px 0;">우리집</div>';
            self.infowindow.setContent(content);
            self.infowindow.open(self.map, marker);
          });

          kakao.maps.event.addListener(marker, 'mouseout', function() {
            self.infowindow.close();
          }); 
        } 
      });          
    },
    
    // 지도 이동 함수
    moveTo() {
      console.log('1');
      const self = this
      if (!self.address) {
        alert('지역을 입력해주세요.');
        return
      }

      self.infowindow = new kakao.maps.InfoWindow({zIndex:1});

      // 주소-좌표 변환 객체를 생성합니다
      var geocoder = new kakao.maps.services.Geocoder();

      // 좌표
      const loc_y = ref(null)
      const loc_x = ref(null)
      console.log('2');
      // 주소로 좌표를 검색합니다
      geocoder.addressSearch(self.address, function (result, status) {
        console.log('3');
        // 정상적으로 검색이 완료됐으면 
        if (status === kakao.maps.services.Status.OK) {
          console.log('OK');
          var coords = new kakao.maps.LatLng(result[0].y, result[0].x);

          loc_y.value = result[0].y
          loc_x.value = result[0].x

          // 지도의 중심을 결과값으로 받은 위치로 이동시킵니다
          self.map.setCenter(coords);
          console.log(`이동위치: ${coords}`);
          console.log(self.bankSelected);
          // 은행 선택 여부에 따라 키워드검색 전체 검색 나누기
          if (!self.bankSelected) {
            self.searchAll()
          } else {
            self.searchDetail()
          }
        } 
      });
    },
    
    // 전체 검색 함수
    searchAll() {

      const self = this
      
      // 장소 검색 객체를 생성합니다
      var ps = new kakao.maps.services.Places(self.map); 
  
      // 카테고리로 은행을 검색합니다
      ps.categorySearch('BK9', placesSearchCB, {useMapBounds:true}); 
  
      // 장소검색이 완료됐을 때 호출되는 콜백함수 입니다
      function placesSearchCB(data, status, pagination) {
          if (status === kakao.maps.services.Status.OK) {

              // 정상적으로 검색이 완료됐으면
              // 검색 목록과 마커를 표출합니다
              displayPlaces(data);

              // 페이지 번호를 표출합니다
              displayPagination(pagination);

          } else if (status === kakao.maps.services.Status.ZERO_RESULT) {

              alert('검색 결과가 존재하지 않습니다.');
              return;

          } else if (status === kakao.maps.services.Status.ERROR) {

              alert('검색 결과 중 오류가 발생했습니다.');
              return;

          }
      }

      function displayPlaces(places) {

          var listEl = document.getElementById('placesList'), 
          menuEl = document.getElementById('menu_wrap'),
          fragment = document.createDocumentFragment(), 
          bounds = new kakao.maps.LatLngBounds(), 
          listStr = '';
          
          // 검색 결과 목록에 추가된 항목들을 제거합니다
          removeAllChildNods(listEl);

          // 지도에 표시되고 있는 마커를 제거합니다
          removeMarker();
          
          for ( var i=0; i<places.length; i++ ) {

              // 마커를 생성하고 지도에 표시합니다
              var placePosition = new kakao.maps.LatLng(places[i].y, places[i].x),
                  marker = addMarker(placePosition, i), 
                  itemEl = getListItem(i, places[i]); // 검색 결과 항목 Element를 생성합니다

              // 검색된 장소 위치를 기준으로 지도 범위를 재설정하기위해
              // LatLngBounds 객체에 좌표를 추가합니다
              bounds.extend(placePosition);

              // 마커와 검색결과 항목에 mouseover 했을때
              // 해당 장소에 인포윈도우에 장소명을 표시합니다
              // mouseout 했을 때는 인포윈도우를 닫습니다
              (function(marker, title) {
                  kakao.maps.event.addListener(marker, 'mouseover', function() {
                      displayInfowindow(marker, title);
                  });

                  kakao.maps.event.addListener(marker, 'mouseout', function() {
                      self.infowindow.close();
                  });

                  itemEl.onmouseover =  function () {
                      displayInfowindow(marker, title);
                  };

                  itemEl.onmouseout =  function () {
                      self.infowindow.close();
                  };
              })(marker, places[i].place_name);

              fragment.appendChild(itemEl);
          }

          // 검색결과 항목들을 검색결과 목록 Element에 추가합니다
          listEl.appendChild(fragment);
          menuEl.scrollTop = 0;

          // 검색된 장소 위치를 기준으로 지도 범위를 재설정합니다
          self.map.setBounds(bounds);
      }  
      // 검색결과 항목을 Element로 반환하는 함수입니다
      function getListItem(index, places) {

          var el = document.createElement('li'),
          itemStr = '<span class="markerbg marker_' + (index+1) + '"></span>' +
                      '<div class="info">' +
                      '   <h5>' + places.place_name + '</h5>';

          if (places.road_address_name) {
              itemStr += '    <span>' + places.road_address_name + '</span>' +
                          '   <span class="jibun gray">' +  places.address_name  + '</span>';
          } else {
              itemStr += '    <span>' +  places.address_name  + '</span>'; 
          }
                      
            itemStr += '  <span class="tel">' + places.phone  + '</span>' +
                      '</div>';           

          el.innerHTML = itemStr;
          el.className = 'item';

          return el;
      }
      // 마커를 생성하고 지도 위에 마커를 표시하는 함수입니다
      function addMarker(position, idx, title) {
          var imageSrc = 'https://t1.daumcdn.net/localimg/localimages/07/mapapidoc/marker_number_blue.png', // 마커 이미지 url, 스프라이트 이미지를 씁니다
              imageSize = new kakao.maps.Size(36, 37),  // 마커 이미지의 크기
              imgOptions =  {
                  spriteSize : new kakao.maps.Size(36, 691), // 스프라이트 이미지의 크기
                  spriteOrigin : new kakao.maps.Point(0, (idx*46)+10), // 스프라이트 이미지 중 사용할 영역의 좌상단 좌표
                  offset: new kakao.maps.Point(13, 37) // 마커 좌표에 일치시킬 이미지 내에서의 좌표
              },
              markerImage = new kakao.maps.MarkerImage(imageSrc, imageSize, imgOptions),
                  marker = new kakao.maps.Marker({
                  position: position, // 마커의 위치
                  image: markerImage 
              });

          marker.setMap(self.map); // 지도 위에 마커를 표출합니다
          self.markers.push(marker);  // 배열에 생성된 마커를 추가합니다

          return marker;
      }

      // 지도 위에 표시되고 있는 마커를 모두 제거합니다
      function removeMarker() {
          for ( var i = 0; i < self.markers.length; i++ ) {
              self.markers[i].setMap(null);
          }   
          self.markers = [];
      }

      // 검색결과 목록 하단에 페이지번호를 표시는 함수입니다
      function displayPagination(pagination) {
          var paginationEl = document.getElementById('pagination'),
              fragment = document.createDocumentFragment(),
              i; 

          // 기존에 추가된 페이지번호를 삭제합니다
          while (paginationEl.hasChildNodes()) {
              paginationEl.removeChild (paginationEl.lastChild);
          }

          for (i=1; i<=pagination.last; i++) {
              var el = document.createElement('a');
              el.href = "#";
              el.innerHTML = i;

              if (i===pagination.current) {
                  el.className = 'on';
              } else {
                  el.onclick = (function(i) {
                      return function() {
                          pagination.gotoPage(i);
                      }
                  })(i);
              }

              fragment.appendChild(el);
          }
          paginationEl.appendChild(fragment);
      }

      // 검색결과 목록 또는 마커를 클릭했을 때 호출되는 함수입니다
      // 인포윈도우에 장소명을 표시합니다
      function displayInfowindow(marker, title) {
          var content = '<div style="padding:5px;z-index:1;">' + title + '</div>';

          self.infowindow.setContent(content);
          self.infowindow.open(self.map, marker);
      }

      // 검색결과 목록의 자식 Element를 제거하는 함수입니다
      function removeAllChildNods(el) {   
          while (el.hasChildNodes()) {
              el.removeChild (el.lastChild);
          }
      }      
      // // 지도에 마커를 표시하는 함수입니다
      // function displayMarker(place) {
      //     // 마커를 생성하고 지도에 표시합니다
      //     var marker = new kakao.maps.Marker({
      //         map: self.map,
      //         position: new kakao.maps.LatLng(place.y, place.x) 
      //     });
  
      //     // 마커에 클릭이벤트를 등록합니다
      //     kakao.maps.event.addListener(marker, 'click', function() {
      //         // 마커를 클릭하면 장소명이 인포윈도우에 표출됩니다
      //         self.infowindow.setContent('<div style="padding:5px;font-size:12px;">' + place.place_name + '</div>');
      //         self.infowindow.open(self.map, marker);
      //     });
      // }


    },

    // 집 주변 검색 함수
    searchHome() {

      const self = this

      // 주소-좌표 변환 객체를 생성합니다
      var geocoder = new kakao.maps.services.Geocoder();

      console.log(1);
      
      // 주소로 좌표를 검색합니다
      geocoder.addressSearch(self.userStore.user.address, function(result, status) {
        console.log(2);
        // 정상적으로 검색이 완료됐으면 
        if (status === kakao.maps.services.Status.OK) {
          console.log(3);
          var coords = new kakao.maps.LatLng(result[0].y, result[0].x);

          // 지도의 중심을 결과값으로 받은 위치로 이동시킵니다
          map.setCenter(coords);
          console.log(coords);          
        }
      })      
      
      // 장소 검색 객체를 생성합니다
      var ps = new kakao.maps.services.Places(self.map); 
  
      // 카테고리로 은행을 검색합니다
      ps.categorySearch('BK9', placesSearchCB, {useMapBounds:true}); 
  
      // 장소검색이 완료됐을 때 호출되는 콜백함수 입니다
      function placesSearchCB(data, status, pagination) {
          if (status === kakao.maps.services.Status.OK) {

              // 정상적으로 검색이 완료됐으면
              // 검색 목록과 마커를 표출합니다
              displayPlaces(data);

              // 페이지 번호를 표출합니다
              displayPagination(pagination);

          } else if (status === kakao.maps.services.Status.ZERO_RESULT) {

              alert('검색 결과가 존재하지 않습니다.');
              return;

          } else if (status === kakao.maps.services.Status.ERROR) {

              alert('검색 결과 중 오류가 발생했습니다.');
              return;

          }
      }

      function displayPlaces(places) {

          var listEl = document.getElementById('placesList'), 
          menuEl = document.getElementById('menu_wrap'),
          fragment = document.createDocumentFragment(), 
          bounds = new kakao.maps.LatLngBounds(), 
          listStr = '';
          
          // 검색 결과 목록에 추가된 항목들을 제거합니다
          removeAllChildNods(listEl);

          // 지도에 표시되고 있는 마커를 제거합니다
          removeMarker();
          
          for ( var i=0; i<places.length; i++ ) {

              // 마커를 생성하고 지도에 표시합니다
              var placePosition = new kakao.maps.LatLng(places[i].y, places[i].x),
                  marker = addMarker(placePosition, i), 
                  itemEl = getListItem(i, places[i]); // 검색 결과 항목 Element를 생성합니다

              // 검색된 장소 위치를 기준으로 지도 범위를 재설정하기위해
              // LatLngBounds 객체에 좌표를 추가합니다
              bounds.extend(placePosition);

              // 마커와 검색결과 항목에 mouseover 했을때
              // 해당 장소에 인포윈도우에 장소명을 표시합니다
              // mouseout 했을 때는 인포윈도우를 닫습니다
              (function(marker, title) {
                  kakao.maps.event.addListener(marker, 'mouseover', function() {
                      displayInfowindow(marker, title);
                  });

                  kakao.maps.event.addListener(marker, 'mouseout', function() {
                      self.infowindow.close();
                  });

                  itemEl.onmouseover =  function () {
                      displayInfowindow(marker, title);
                  };

                  itemEl.onmouseout =  function () {
                      self.infowindow.close();
                  };
              })(marker, places[i].place_name);

              fragment.appendChild(itemEl);
          }

          // 검색결과 항목들을 검색결과 목록 Element에 추가합니다
          listEl.appendChild(fragment);
          menuEl.scrollTop = 0;

          // 검색된 장소 위치를 기준으로 지도 범위를 재설정합니다
          self.map.setBounds(bounds);
      }  
      // 검색결과 항목을 Element로 반환하는 함수입니다
      function getListItem(index, places) {

          var el = document.createElement('li'),
          itemStr = '<span class="markerbg marker_' + (index+1) + '"></span>' +
                      '<div class="info">' +
                      '   <h5>' + places.place_name + '</h5>';

          if (places.road_address_name) {
              itemStr += '    <span>' + places.road_address_name + '</span>' +
                          '   <span class="jibun gray">' +  places.address_name  + '</span>';
          } else {
              itemStr += '    <span>' +  places.address_name  + '</span>'; 
          }
                      
            itemStr += '  <span class="tel">' + places.phone  + '</span>' +
                      '</div>';           

          el.innerHTML = itemStr;
          el.className = 'item';

          return el;
      }
      // 마커를 생성하고 지도 위에 마커를 표시하는 함수입니다
      function addMarker(position, idx, title) {
          var imageSrc = 'https://t1.daumcdn.net/localimg/localimages/07/mapapidoc/marker_number_blue.png', // 마커 이미지 url, 스프라이트 이미지를 씁니다
              imageSize = new kakao.maps.Size(36, 37),  // 마커 이미지의 크기
              imgOptions =  {
                  spriteSize : new kakao.maps.Size(36, 691), // 스프라이트 이미지의 크기
                  spriteOrigin : new kakao.maps.Point(0, (idx*46)+10), // 스프라이트 이미지 중 사용할 영역의 좌상단 좌표
                  offset: new kakao.maps.Point(13, 37) // 마커 좌표에 일치시킬 이미지 내에서의 좌표
              },
              markerImage = new kakao.maps.MarkerImage(imageSrc, imageSize, imgOptions),
                  marker = new kakao.maps.Marker({
                  position: position, // 마커의 위치
                  image: markerImage 
              });

          marker.setMap(self.map); // 지도 위에 마커를 표출합니다
          self.markers.push(marker);  // 배열에 생성된 마커를 추가합니다

          return marker;
      }

      // 지도 위에 표시되고 있는 마커를 모두 제거합니다
      function removeMarker() {
          for ( var i = 0; i < self.markers.length; i++ ) {
              self.markers[i].setMap(null);
          }   
          self.markers = [];
      }

      // 검색결과 목록 하단에 페이지번호를 표시는 함수입니다
      function displayPagination(pagination) {
          var paginationEl = document.getElementById('pagination'),
              fragment = document.createDocumentFragment(),
              i; 

          // 기존에 추가된 페이지번호를 삭제합니다
          while (paginationEl.hasChildNodes()) {
              paginationEl.removeChild (paginationEl.lastChild);
          }

          for (i=1; i<=pagination.last; i++) {
              var el = document.createElement('a');
              el.href = "#";
              el.innerHTML = i;

              if (i===pagination.current) {
                  el.className = 'on';
              } else {
                  el.onclick = (function(i) {
                      return function() {
                          pagination.gotoPage(i);
                      }
                  })(i);
              }

              fragment.appendChild(el);
          }
          paginationEl.appendChild(fragment);
      }

      // 검색결과 목록 또는 마커를 클릭했을 때 호출되는 함수입니다
      // 인포윈도우에 장소명을 표시합니다
      function displayInfowindow(marker, title) {
          var content = '<div style="padding:5px;z-index:1;">' + title + '</div>';

          self.infowindow.setContent(content);
          self.infowindow.open(self.map, marker);
      }

      // 검색결과 목록의 자식 Element를 제거하는 함수입니다
      function removeAllChildNods(el) {   
          while (el.hasChildNodes()) {
              el.removeChild (el.lastChild);
          }
      }      
      // // 지도에 마커를 표시하는 함수입니다
      // function displayMarker(place) {
      //     // 마커를 생성하고 지도에 표시합니다
      //     var marker = new kakao.maps.Marker({
      //         map: self.map,
      //         position: new kakao.maps.LatLng(place.y, place.x) 
      //     });
  
      //     // 마커에 클릭이벤트를 등록합니다
      //     kakao.maps.event.addListener(marker, 'click', function() {
      //         // 마커를 클릭하면 장소명이 인포윈도우에 표출됩니다
      //         self.infowindow.setContent('<div style="padding:5px;font-size:12px;">' + place.place_name + '</div>');
      //         self.infowindow.open(self.map, marker);
      //     });
      // }


    },    

    // 키워드 검색 함수
    searchDetail() {

      const self = this
      
      // 장소 검색 객체를 생성합니다
      var ps = new kakao.maps.services.Places();  

      // 검색 결과 목록이나 마커를 클릭했을 때 장소명을 표출할 인포윈도우를 생성합니다
      self.infowindow = new kakao.maps.InfoWindow({zIndex:1});

      var keyword = self.address2
      console.log(self.address2);

      // 장소검색 객체를 통해 키워드로 장소검색을 요청합니다
      ps.keywordSearch(keyword, placesSearchCB); 


      // 장소검색이 완료됐을 때 호출되는 콜백함수 입니다
      function placesSearchCB(data, status, pagination) {
          if (status === kakao.maps.services.Status.OK) {

              // 정상적으로 검색이 완료됐으면
              // 검색 목록과 마커를 표출합니다
              displayPlaces(data);

              // 페이지 번호를 표출합니다
              displayPagination(pagination);

          } else if (status === kakao.maps.services.Status.ZERO_RESULT) {

              alert('검색 결과가 존재하지 않습니다.');
              return;

          } else if (status === kakao.maps.services.Status.ERROR) {

              alert('검색 결과 중 오류가 발생했습니다.');
              return;

          }
      }

      // 검색 결과 목록과 마커를 표출하는 함수입니다
      function displayPlaces(places) {

          var listEl = document.getElementById('placesList'), 
          menuEl = document.getElementById('menu_wrap'),
          fragment = document.createDocumentFragment(), 
          bounds = new kakao.maps.LatLngBounds(), 
          listStr = '';
          
          // 검색 결과 목록에 추가된 항목들을 제거합니다
          removeAllChildNods(listEl);

          // 지도에 표시되고 있는 마커를 제거합니다
          removeMarker();
          
          for ( var i=0; i<places.length; i++ ) {

              // 마커를 생성하고 지도에 표시합니다
              var placePosition = new kakao.maps.LatLng(places[i].y, places[i].x),
                  marker = addMarker(placePosition, i), 
                  itemEl = getListItem(i, places[i]); // 검색 결과 항목 Element를 생성합니다

              // 검색된 장소 위치를 기준으로 지도 범위를 재설정하기위해
              // LatLngBounds 객체에 좌표를 추가합니다
              bounds.extend(placePosition);

              // 마커와 검색결과 항목에 mouseover 했을때
              // 해당 장소에 인포윈도우에 장소명을 표시합니다
              // mouseout 했을 때는 인포윈도우를 닫습니다
              (function(marker, title) {
                  kakao.maps.event.addListener(marker, 'mouseover', function() {
                      displayInfowindow(marker, title);
                  });

                  kakao.maps.event.addListener(marker, 'mouseout', function() {
                    self.infowindow.close();
                  });

                  itemEl.onmouseover =  function () {
                      displayInfowindow(marker, title);
                  };

                  itemEl.onmouseout =  function () {
                    self.infowindow.close();
                  };
              })(marker, places[i].place_name);

              fragment.appendChild(itemEl);
          }

          // 검색결과 항목들을 검색결과 목록 Element에 추가합니다
          listEl.appendChild(fragment);
          menuEl.scrollTop = 0;

          // 검색된 장소 위치를 기준으로 지도 범위를 재설정합니다
          self.map.setBounds(bounds);
      }

      // 검색결과 항목을 Element로 반환하는 함수입니다
      function getListItem(index, places) {

          var el = document.createElement('li'),
          itemStr = '<span class="markerbg marker_' + (index+1) + '"></span>' +
                      '<div class="info">' +
                      '   <h5>' + places.place_name + '</h5>';

          if (places.road_address_name) {
              itemStr += '    <span>' + places.road_address_name + '</span>' +
                          '   <span class="jibun gray">' +  places.address_name  + '</span>';
          } else {
              itemStr += '    <span>' +  places.address_name  + '</span>'; 
          }
                      
            itemStr += '  <span class="tel">' + places.phone  + '</span>' +
                      '</div>';           

          el.innerHTML = itemStr;
          el.className = 'item';

          return el;
      }

      // 마커를 생성하고 지도 위에 마커를 표시하는 함수입니다
      function addMarker(position, idx, title) {
          var imageSrc = 'https://t1.daumcdn.net/localimg/localimages/07/mapapidoc/marker_number_blue.png', // 마커 이미지 url, 스프라이트 이미지를 씁니다
              imageSize = new kakao.maps.Size(36, 37),  // 마커 이미지의 크기
              imgOptions =  {
                  spriteSize : new kakao.maps.Size(36, 691), // 스프라이트 이미지의 크기
                  spriteOrigin : new kakao.maps.Point(0, (idx*46)+10), // 스프라이트 이미지 중 사용할 영역의 좌상단 좌표
                  offset: new kakao.maps.Point(13, 37) // 마커 좌표에 일치시킬 이미지 내에서의 좌표
              },
              markerImage = new kakao.maps.MarkerImage(imageSrc, imageSize, imgOptions),
                  marker = new kakao.maps.Marker({
                  position: position, // 마커의 위치
                  image: markerImage 
              });

          marker.setMap(self.map); // 지도 위에 마커를 표출합니다
          self.markers.push(marker);  // 배열에 생성된 마커를 추가합니다

          return marker;
      }

      // 지도 위에 표시되고 있는 마커를 모두 제거합니다
      function removeMarker() {
          for ( var i = 0; i < self.markers.length; i++ ) {
              self.markers[i].setMap(null);
          }   
          self.markers = [];
      }

      // 검색결과 목록 하단에 페이지번호를 표시는 함수입니다
      function displayPagination(pagination) {
          var paginationEl = document.getElementById('pagination'),
              fragment = document.createDocumentFragment(),
              i; 

          // 기존에 추가된 페이지번호를 삭제합니다
          while (paginationEl.hasChildNodes()) {
              paginationEl.removeChild (paginationEl.lastChild);
          }

          for (i=1; i<=pagination.last; i++) {
              var el = document.createElement('a');
              el.href = "#";
              el.innerHTML = i;

              if (i===pagination.current) {
                  el.className = 'on';
              } else {
                  el.onclick = (function(i) {
                      return function() {
                          pagination.gotoPage(i);
                      }
                  })(i);
              }

              fragment.appendChild(el);
          }
          paginationEl.appendChild(fragment);
      }

      // 검색결과 목록 또는 마커를 클릭했을 때 호출되는 함수입니다
      // 인포윈도우에 장소명을 표시합니다
      function displayInfowindow(marker, title) {
          var content = '<div style="padding:5px;z-index:1;">' + title + '</div>';

          self.infowindow.setContent(content);
          self.infowindow.open(self.map, marker);
      }

      // 검색결과 목록의 자식 Element를 제거하는 함수입니다
      function removeAllChildNods(el) {   
          while (el.hasChildNodes()) {
              el.removeChild (el.lastChild);
          }
      }
    }
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style>
#map {
  width: 585px;
  height: 585px;
}
.map_wrap, .map_wrap * {margin:0;padding:0;font-family:'Malgun Gothic',dotum,'돋움',sans-serif;font-size:12px;}
.map_wrap a, .map_wrap a:hover, .map_wrap a:active{color:#000;text-decoration: none;}
.map_wrap {position:relative;width:100%;height:600px;}
#menu_wrap {position:absolute;top:0;left:585px;bottom:0;width:250px;margin:10px 0 30px 10px;padding:5px;overflow-y:auto;background:rgba(255, 255, 255, 0.7);z-index: 1;font-size:12px;border-radius: 10px;}
.bg_white {background:#fff;}
#menu_wrap hr {display: block; height: 1px;border: 0; border-top: 2px solid #5F5F5F;margin:3px 0;}
#menu_wrap .option{text-align: center;}
#menu_wrap .option p {margin:10px 0;}  
#menu_wrap .option button {margin-left:5px;}
#placesList li {list-style: none;}
#placesList .item {position:relative;border-bottom:1px solid #888;overflow: hidden;cursor: pointer;min-height: 65px;}
#placesList .item span {display: block;margin-top:4px;}
#placesList .item h5, #placesList .item .info {text-overflow: ellipsis;overflow: hidden;white-space: nowrap;}
#placesList .item .info{padding:10px 0 10px 55px;}
#placesList .info .gray {color:#8a8a8a;}
#placesList .info .jibun {padding-left:26px;background:url(https://t1.daumcdn.net/localimg/localimages/07/mapapidoc/places_jibun.png) no-repeat;}
#placesList .info .tel {color:#009900;}
#placesList .item .markerbg {float:left;position:absolute;width:36px; height:37px;margin:10px 0 0 10px;background:url(https://t1.daumcdn.net/localimg/localimages/07/mapapidoc/marker_number_blue.png) no-repeat;}
#placesList .item .marker_1 {background-position: 0 -10px;}
#placesList .item .marker_2 {background-position: 0 -56px;}
#placesList .item .marker_3 {background-position: 0 -102px}
#placesList .item .marker_4 {background-position: 0 -148px;}
#placesList .item .marker_5 {background-position: 0 -194px;}
#placesList .item .marker_6 {background-position: 0 -240px;}
#placesList .item .marker_7 {background-position: 0 -286px;}
#placesList .item .marker_8 {background-position: 0 -332px;}
#placesList .item .marker_9 {background-position: 0 -378px;}
#placesList .item .marker_10 {background-position: 0 -423px;}
#placesList .item .marker_11 {background-position: 0 -470px;}
#placesList .item .marker_12 {background-position: 0 -516px;}
#placesList .item .marker_13 {background-position: 0 -562px;}
#placesList .item .marker_14 {background-position: 0 -608px;}
#placesList .item .marker_15 {background-position: 0 -654px;}
#pagination {margin:10px auto;text-align: center;}
#pagination a {display:inline-block;margin-right:10px;}
#pagination .on {font-weight: bold; cursor: default;color:#777;}
</style>
