var pMap = null;
function InitWnd() {
    var pOMap = document.getElementById("TGMap");
    pMap = new TGOS.TGOnlineMap(pOMap, TGOS.TGCoordSys.EPSG3857); // set coordinate to WGS84
    pMap.setCenter(new TGOS.TGPoint(center_point[0], center_point[1]) );  // set the center of the initial map
    pMap.setZoom(13); // Zooming scale
    addPosition(shop_data);
}
function getRandomColor() {
    var letters = '0123456789ABCDEF'.split('');
    var color = '#';
    for (var i = 0; i < 6; i++ ) {
        color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
}
function getSymbol(color, freq){
    size = (freq+10)*1.2; // set the size dending on the frequency of shopping times
    pTGSymbo = new TGOS.TGSymbol(); // 建立幾何物件
    pTGSymbo.symbolStyle = TGOS.TGSymbolStyle.TRIANGLE; // 設定標記的符號
    pTGSymbo.xPixel = size; // 設定標記寬度
    pTGSymbo.yPixel = size; // 設定標記高度
    pTGSymbo.fillColor = color; // 設定填入顏色
    pTGSymbo.fillOpacity = 0.7; // 設定透明度
    pTGSymbo.strokeWeight = 2; // 設定框線寬度
    pTGSymbo.strokeOpacity = 0.4; // 設定框線透明度
    pTGSymbo.strokeColor = "#000000"; // 設定框線顏色
    pTGSymbo.anchor.x = size/2; // 設定錨點x座標
    pTGSymbo.anchor.y = size/2; // 設定錨點y座標
    pTGSymbo.rotation = 0; // 設定符號旋轉方向
    return pTGSymbo;
}
function addPosition(data){
    var InfoWindowOptions = {
         maxWidth:4000, //訊息視窗的最大寬度
         pixelOffset: new TGOS.TGSize(5, -30), //InfoWindow起始位置的偏移量
                                               //使用TGSize設定
                                               //向右X為正, 向上Y為負
         zIndex:99 //視窗堆疊順序
    };
    var multi_point = [];
    var current_cluster = 1, current_color = "#AA2222";
    symbol = getSymbol();
    for(var i = 0; i < data.length; i++) {
        if(current_cluster!=data[i][data[i].length-2]) current_color = getRandomColor();
        var symbol = getSymbol(current_color,parseInt(data[i][6]));
        console.log(data);
        var point = new TGOS.TGPoint(parseFloat(data[i][1]),parseFloat(data[i][2])); // create its position
        
        var delimeter = (data[i][3]=='' || data[i][4]=='')?'':'-';
        var pTGMarker = new TGOS.TGMarker(pMap,point,data[i][3] + delimeter + data[i][4], symbol, {flat:false}); // establish the point on map

        if(current_cluster==data[i][data[i].length-2]) multi_point.push(pTGMarker);
        else{
            addMarkerClusters(multi_point);
            multi_point = [pTGMarker];
            current_cluster = data[i][data[i].length-2];
        }
        //-----------------establish a message box--------------------
        var InfoWindowOptions = {
              maxWidth:4000, // 訊息視窗的最大寬度
              pixelOffset: new TGOS.TGSize(5, -30) //InfoWindow起始位置的偏移量, 使用TGSize設定, 向右X為正, 向上Y為負
        };
        var invoice_message = '<h2><font color="#CE0000">' + data[i][3]+ delimeter+data[i][4]+'</font></h2>' // 商店名稱
        + data[i][5] // 地址
        +'<br />頻率：<font color="blue" size="+1"><b>' + data[i][6] + '</b></font>' // 頻率
        +'<br />總消費金額：<font color="red">' + data[i][7] + '</font>' // 總消費金額
        +'<br />最常購買商品：<font color="#009100">' + data[i][8] + '</font>'; //最常購買商品
        messageBox = new TGOS.TGInfoWindow(invoice_message, point, InfoWindowOptions); // the content in message box

        TGOS.TGEvent.addListener(pTGMarker, "mouseover", function (pTGMarker, messageBox) { // when mouse over the point
             return function () {
                messageBox.open(pMap, pTGMarker);
             }
        } (pTGMarker, messageBox));

        TGOS.TGEvent.addListener(pTGMarker, "mouseout", function (messageBox) { // when mouse out the point
                 return function () {
                            messageBox.close();
                 }
        } (messageBox));
        TGOS.TGEvent.addListener(pTGMarker, "click", function (invoice_array){ // when click the point
            return function (){
                showBlock('detail',true);
                document.getElementById('detail').innerHTML = get_invoice_list_string(current_shop_data);
                }
            }(data[i]) );
    }
    addMarkerClusters(multi_point); // add these point to the same cluster
}
function addMarkerClusters(markers) {                           //使用群聚標記點功能
    mCluster = new TGOS.TGMarkerCluster(pMap, markers,{}); //建立群聚標記點物件
    mCluster.setMaxZoom(12);                             //設定群聚標記點最大縮放範圍
    mCluster.setVisible(true);                         //設定群聚標記點是否為顯示狀態
    mCluster.setSearchBounds(30);                      //設定群聚標記點的搜尋範圍(單位px)
    mCluster.redrawAll(true);                         //是否重新繪製群聚標記點物件
}