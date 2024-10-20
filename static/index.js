// let map;

// function initMap() {
//     const center = { lat: 37.6569377884, lng: 126.7718356549 }; // 기본 중심 좌표

//     map = new google.maps.Map(document.getElementById("map"), {
//         zoom: 15,
//         center: center,
//     });

//     fetch('/toilets')
//         .then(response => response.json())
//         .then(data => {
//             console.log(data); // 데이터 확인
//             data.forEach(toilet => {
//                 const marker = new google.maps.Marker({
//                     position: { lat: toilet.latitude, lng: toilet.longitude },
//                     map: map,
//                     title: toilet.name,
//                 });
//             });
//         })
//         .catch(error => console.error('Error fetching toilet data:', error));
// }

let map;

function initMap() {
    const center = { lat: 37.6569377884, lng: 126.7718356549 }; // 기본 중심 좌표

    map = new google.maps.Map(document.getElementById("map"), {
        zoom: 15,
        center: center,
    });

    fetch('/toilets')
        .then(response => response.json())
        .then(data => {
            console.log(data); // 데이터 확인
            data.forEach(toilet => {
                const marker = new google.maps.Marker({
                    position: { lat: toilet.latitude, lng: toilet.longitude },
                    map: map,
                    title: toilet.name,
                });

                // InfoWindow 설정
                const infoWindow = new google.maps.InfoWindow({
                    content: `<h3>${toilet.name}</h3>`,
                });

                // 마커에 mouseover 이벤트 추가
                marker.addListener('mouseover', () => {
                    infoWindow.open(map, marker);
                });

                // 마커에 mouseout 이벤트 추가하여 InfoWindow 닫기
                marker.addListener('mouseout', () => {
                    infoWindow.close();
                });
            });
        })
        .catch(error => console.error('Error fetching toilet data:', error));
}

initMap();
