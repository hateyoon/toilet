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
            });
        })
        .catch(error => console.error('Error fetching toilet data:', error));
}

