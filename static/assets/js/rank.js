
let PROCESSING = false;

function showProcessing() {
    let keyword = $('#keyword').val();
    let company = $('#company').val();

    $('#contentsDiv').html("<div class=\"large-12 cell\">\n" +
                        "                <div class=\"callout\">\n" +
                        "                    <div class=\"grid-x grid-padding-x\">\n" +
                        "                        <div class=\"large-8 medium-2 cell\">&nbsp;&nbsp;<i>"+ keyword +"</i> 중 <b>"+  company +"</b> 검색중입니다.</div>\n" +
                        "                    </div>\n" +
                        "                </div>\n" +
                        "            </div>");
}

function makeRankRowTag(rank) {
    $('#contentsDiv').html("<div class=\"large-12 cell\">\n" +
                        "                <div class=\"callout\">\n" +
                        "                    <div class=\"grid-x grid-padding-x\">\n" +
                        "                        <div class=\"large-2 medium-2 cell\"><img src=\""+ rank.imageurl +"\" /></div>\n" +
                        "                        <div class=\"large-2 medium-2 cell\">"+ rank.rank +" 위 (최근 순위 : "+  rank.latestRank + "위 - "+ rank.latestSearchDate +")</div>\n" +
                        "                        <div class=\"large-8 medium-2 cell\">"+ rank.title +"</div>\n" +
                        "                    </div>\n" +
                        "                </div>\n" +
                        "            </div>");
}

function requestRankData() {
    let keyword = $('#keyword').val();
    let company = $('#company').val();
    if (PROCESSING) {
        alert('현재 처리중입니다...');
    } else {

        if (keyword == '' || company == '') {
            alert("검색어를 입력해 주세요!");
            return;
        }
        PROCESSING = true;

        showProcessing();

        $.ajax({
            url:'/rank/search?keyword='+ keyword +'&company=' + company,
            dataType:'json',
            success:function(rank) {
                PROCESSING = false;
                makeRankRowTag(rank);
            },
            error:function() {
                PROCESSING = false;
                alert('검색실패!');
            }
        })
    }
}

$(document).ready(function() {
    $('#searchBtn').click(requestRankData);
    $('#company').keydown(function(event) {

        if (event.which == 13) {
            requestRankData();
        }

    });
});






//
// let a = 2;
//
// switch (a) {
//     case 1:
//         console.log(a);
//         break;
//     default:
//         console.log("nop!");
//         break;
// }
//
// if (a == 1) {
//     console.log(a);
// } else {
//     console.log("nop");
// }
//
// for (let idx = 0; idx < 3; idx++) { // ++ : + 1
//     console.log("for : " + idx);
// }
//
// let loop = 0;
// while (loop < 3) {
//     console.log("while : " + loop);
//     loop = loop + 1; //loop++, loop += 1
// }
//
// loop = 0;
// do {
//     console.log("do while : " + loop);
//     loop++;
// } while(loop < 0);
//
//
//
// let arr = [1,2,3,4];
//
// for (let idx = 0, len = arr.length; idx < len; idx++) {
//     console.log("arr[" + idx + "] : " + arr[idx]);
// }
//
//
//
// myFun('rankService');
//
// function myFun(param) {
//     console.log("myFun : " + param);
// }
//
// // myFun2("rankService");
//
// let myFun2 = function(param) {
//     console.log("myFun2 : " + param.target);
// }
//
// myFun2("rankService");


// window.addEventListener('DOMContentLoaded', function() {
//     // 초기화데이타
//     document.getElementById('keyword').value = "대용량보온병";
// });


// $(document).ready(function() {
    // $('#keyword').val("유아보온병");
// });

// $(document).ready(function() {
//     let tags = $(".grid-container h5");
//     $(tags[0]).append("<div style='background-color: #3adb76'>안여</div>");
// });
