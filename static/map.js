var myMap;
const filenames = {1: ['Roads', [40, 40]],
              2: ['Yards', [40, 33]],
              3: ['Parks', [40, 40]],
              66: ['Ads', [69, 40]],
              78: ['PublicTransport', [40, 34]],
              89: ['StreetLight', [40, 25]],
              2201: ['SocHelp', [40, 22]]}
ymaps.ready(init);
function init()
{
    myMap = new ymaps.Map("map", {
        center: [51.76, 55.09],
        zoom: 10
    });
    for (var p in calls)
    {
        // Создание метки.
        var myGeoObject = new ymaps.Placemark(calls[p][0], // координаты точки
            { balloonContent: calls[p][2] > 0 ? '<a href="/calls/' + calls[p][2].toString() + '" target="_blank" >Смотреть вызов</a>' : ''},
            {
            // Опции.
            // Необходимо указать данный тип макета.
            iconLayout: 'default#image',
            // Своё изображение иконки метки.
            iconImageHref: `/static/icons/${filenames[calls[p][1]][0]}.png`,
            // Размеры метки.
            iconImageSize: [40, 40],
            // Смещение левого верхнего угла иконки относительно
            // её "ножки" (точки привязки).
            iconImageOffset: [-20, -35]
            });
            //{ preset: 'islands#blueDotIcon' });
        // Размещение геообъекта на карте.
        myMap.geoObjects.add(myGeoObject);
    }

    myMap.controls.remove('fullscreenControl');
    myMap.controls.remove('trafficControl');
    if (calls.length > 1) {
        myMap.setBounds(myMap.geoObjects.getBounds());
    }
}


