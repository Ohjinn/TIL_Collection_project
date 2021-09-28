// $(document).ready(function () {
//     getBaseCardsInfo();
// });
//
// function getBaseCardsInfo(){
//     $.ajax({
//         type : "GET",
//         url : "recentCrawling",
//         data : {},
//         success: function (response){
//
//         }
//     })
// }
//
//
// function makeCard(cardInfo){
//     let tempHtml = `<div class="card hotboxs">
//                         <img class="card-img-top card-rows" src="../static/tistoryImage.ico" alt="Card image cap">
//                         <div class="card-body">
//                             <h5 class="card-title">${cardInfo['name']}</h5>
//                             <p class="card-text">주소</p>
//                             <a href="#" class="btn btn-dark">Go somewhere</a>
//                         </div>
//                     </div>`
//     $("#addingBox").append(tempHtml);
// }
//
// function reset() {
//     location.reload();
// }
$(document).ready(function () {
    showLocation();
    getBaseCardsInfo();
});


function getBaseCardsInfo() {
    $.ajax({
        type: "GET",
        url: "recentCrawling",
        data: {},
        success: function (response) {
        }
    })
}

function showLocation(position) {   // 위치 정보 호출 성공시
    let latitude = position.coords.latitude   // 위도
    let longitude = position.coords.longitude  // 경도
    let apiKey = '97329c7c315676010b49d9b9dc79185c';
    let weatherUrl = "https://api.openweathermap.org/data/2.5/weather?lat=" + latitude
        + "&lon=" + longitude
        + "&appid=" + apiKey;
    let options = {method: 'GET'}
    $.ajax(weatherUrl, options).then((response) => {
        console.log(response) // jSON 타입 위치 및 날씨 정보 로그 확인
        let icon = response.weather[0].icon
        let iconUrl = "http://openweathermap.org/img/wn/" + icon + ".png"
        let img = document.querySelector("#wicon")
        img.src = iconUrl
        let w_icon_id = icon[0] + icon[1];
        if (w_icon_id == '01') {
            $("#weather_comment").text("맑은 하늘이네요! 코딩공부하기 좋은 날~♥");
        } else if (w_icon_id == '02') {
            $("#weather_comment").text("약간 구름낀 날씨네요! 코딩공부하기 좋은 날~♥");
        } else if (w_icon_id == '03') {
            $("#weather_comment").text("구름이 조금 더 꼈지만 코딩 공부하기 좋은 날씨네요!♥");
        } else if (w_icon_id == '04') {
            $("#weather_comment").text("구름이 좀 끼고 우중충하니까 코딩공부하기 좋은 날~♥");
        } else if (w_icon_id == '09') {
            $("#weather_comment").text("소나기가 내리는 지금은 코딩공부하기 좋은 날~♥");
        } else if (w_icon_id == '10') {
            $("#weather_comment").text("비가 와요! 코딩공부하기 좋은 날~♥");
        } else if (w_icon_id == '11') {
            $("#weather_comment").text("천둥 번개가 치는 지금은?! 코딩공부하기 좋은 날~♥");
        } else if (w_icon_id == '13') {
            $("#weather_comment").text("눈이 와요~! 코딩공부하기 좋은 날~♥");
        } else
            $("#weather_comment").text("안개가 낀 날씨도 역시! 코딩공부하기 좋은 날~♥");

        $("#tempr").text(Math.round(parseFloat((response.main.temp - 273))) + '˚'); // 현재 온도
    }).catch((error) => {
        console.log(error)
    })

    // $.ajax({
    //     type: "GET",
    //     url: "https://api.openweathermap.org/data/2.5/weather?lat=" + latitude
    //         + "&lon=" + longitude
    //         + "&appid=" + apiKey,
    //     data: {},
    //     success: function (response) {
    //         let icon = response["weather"]["icon"];
    //         let currentTemperature = response["main"]["temp"]-273;
    //         let iconUrl = "http://openweathermap.org/img/wn/" + icon + "@2x.png";
    //         let img = document.querySelector("#wicon");
    //         img.src = iconUrl;
    //         let temp_html = `${currentTemperature}<span class="tempr" id="weather tempr"></span></div><div class="weather">${img.src}<img class="wicon" id="weather wicon" src="">`;
    //         console.log(temp_html);
    //         $('#weather').append(temp_html);
    // $("#tempr").text(parseInt(response.main.temp - 273) + '˚');
    //     }
    // })
}

function showError(position) {
    // 실패 했을 때 처리
    alert("위치 정보를 얻을 수 없습니다.")
}

window.addEventListener('load', () => {
    if (window.navigator.geolocation) {
        window.navigator.geolocation.getCurrentPosition(showLocation, showError)
    }
})

function makeCard(cardInfo) {
    let tempHtml = `<div class="card hotboxs">
                        <img class="card-img-top card-rows" src="../static/tistoryImage.ico" alt="Card image cap">
                        <div class="card-body">
                            <h5 class="card-title">${cardInfo['name']}</h5>
                            <p class="card-text">주소</p>
                            <a href="#" class="btn btn-dark">Go somewhere</a>
                        </div>
                    </div>`
    $("#addingBox").append(tempHtml);
}

function reset() {
    location.reload();
}
