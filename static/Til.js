$(document).ready(function () {
    getBaseCardsInfo();
});

function getBaseCardsInfo(){
    $.ajax({
        type : "GET",
        url : "recentCrawling",
        data : {},
        success: function (response){

        }
    })
}


function makeCard(cardInfo){
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

