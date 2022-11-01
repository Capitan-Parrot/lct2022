    <section>
      <div style="height: 1146px;" class="container-fluid">
        <div class="ya_map" id="myMap">
          <script src="https://api-maps.yandex.ru/2.1/?apikey=dd9e4a35-e52d-4224-9e27-9129905e173d&lang=ru_RU">
          </script>
            <script>
            let center = [55.75211, 37.62209];

            function init() {
                let map = new ymaps.Map('myMap', {
                    center: center,
                    zoom: 14
                });

              map.controls.remove('geolocationControl'); // удаляем геолокацию
              map.controls.remove('searchControl'); // удаляем поиск
              map.controls.remove('trafficControl'); // удаляем контроль трафика
              map.controls.remove('typeSelector'); // удаляем тип
              map.controls.remove('fullscreenControl'); // удаляем кнопку перехода в полноэкранный режим
              map.controls.remove('rulerControl'); // удаляем контрол правил
            }

            ymaps.ready(init);
          </script>

        
      <div class="container-fluid">
        <div class="d-flex flex-row">
          <div class="p-2">
            <div class="left_navigation">
              
            </div>
          </div>
        </div>
      </div>
      
        </div>
      </div>
    </section



   <div clsss="container-fluid">
      <div class="row">
        <div class="col-3">
          <div class="left_navigation">
              
          </div>
        </div>
        <div class="col-9">
          <div class="ya_map" id="myMap">
            <script src="https://api-maps.yandex.ru/2.1/?apikey=dd9e4a35-e52d-4224-9e27-9129905e173d&lang=ru_RU">
            </script>
              <script>
              let center = [55.75211, 37.62209];

              function init() {
                  let map = new ymaps.Map('myMap', {
                      center: center,
                      zoom: 14
                  });

                map.controls.remove('geolocationControl'); // удаляем геолокацию
                map.controls.remove('searchControl'); // удаляем поиск
                map.controls.remove('trafficControl'); // удаляем контроль трафика
                map.controls.remove('typeSelector'); // удаляем тип
                map.controls.remove('fullscreenControl'); // удаляем кнопку перехода в полноэкранный режим
                map.controls.remove('rulerControl'); // удаляем контрол правил
              }

              ymaps.ready(init);
            </script>
          </div>        
        </div>
      </div>
    </div>  




