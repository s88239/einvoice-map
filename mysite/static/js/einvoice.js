invoice_idx = shop_data[0].length-1; // 發票list位於商家list的位置
item_idx = shop_data[0][invoice_idx][0].length-1; // list位於發票list的位置
function get_invoice_list_string(invoice_array){
    var items_array = invoice_array[invoice_idx][0][item_idx]; // 該張發票所有購買商品
    var invoice_list = '<center><a href="javascript:showBlock(\'detail\', false)">close</a><h1><font color="blue">'
    + invoice_array[3] + invoice_array[4]
    + '</font></h1></center><table class="table"><tr><th>順序</th><th>日期</th><th>發票號碼</th><th>總金額</th><th>#</th><th>商品名稱</th><th>數量</th><th>單價</th><th>總價</th></tr>';
    for(var i=0;i<invoice_array[invoice_idx].length;++i){ // 第幾張發票
        var items_array = invoice_array[invoice_idx][i][item_idx]; // 該張發票所有購買商品
        var item_num = items_array.length; // 該張發票商品筆數
        var invoice_list = invoice_list  + '<tr><td rowspan="' + item_num + '">' + (i+1) + '</td>'; // 順序
        for(var j=0;j<invoice_array[invoice_idx][i].length-1;++j){ // 日期 發票號碼 總金額
            invoice_list = invoice_list + '<td rowspan="' + item_num + '">' + invoice_array[invoice_idx][i][j] + '</td>';
        }
        for(var j=0;j<item_num;++j){ // 購買品項 商品名稱 數量 單價 總價
            if(j!=0) invoice_list += '<tr>';
            for(var kk=0;kk<items_array[j].length;++kk){
                invoice_list = invoice_list + '<td>' + items_array[j][kk] + '</td>';
            }
            invoice_list += '</tr>';
        }
    }
    invoice_list += '</table>';
    return invoice_list;
}
function show_all_shop(){
    showBlock('detail',false);
    showBlock('TGMap',false);
    var invoice_list = '<center><p><font color="blue" size="+4">商店清單</font></p></center>'
    + '<table class="table table-hover"><tr><th>順序</th><th>商店名稱</th><th>分店名稱</th><th>商店地址</th><th>頻率</th><th>消費金額</th><th>最常購買品項</th><th>cluster</th>';
    for(i=0;i<shop_data.length;++i){
        invoice_list += '<tr><td>'+(i+1)+'</td>';
        for(j=3;j<shop_data[i].length-1;++j){
            invoice_list += '<td>' + shop_data[i][j] + '</td>';
        }
    }
    invoice_list += '</table>';
    document.getElementById('main_text').innerHTML = invoice_list;
}
function show_all_einvoice(){
    showBlock('detail',false);
    showBlock('TGMap',false);
    var invoice_list = '<center><p><font color="blue" size="+4">電子發票清單</font></p></center>'
    + '<table class="table table-hover"><tr><th>順序</th><th>消費日期</th><th>載具</th><th>商店名稱</th><th>消費金額</th><th>發票號碼</th>';
    var count = 1;
    for(i=einvoice_list.length-1;i>=0;--i,++count){
        invoice_list += '<tr><td>' + count + '</td>'; // 順序
        for(j=1;j<7;++j){
            if(j==2){ // invoice.card_type
                if(einvoice_list[i][j] == '3J0002') carrier_type = '手機條碼';
                else if(einvoice_list[i][j] == '1K0001') carrier_type = '悠遊卡';
                else if(einvoice_list[i][j] == '2G0001') carrier_type = 'iCash';
                else carrier_type = '其他載具';
                invoice_list += '<td>' + carrier_type + ' ' + einvoice_list[i][++j] + '</td>';
            }
            else{
                invoice_list += '<td>' + einvoice_list[i][j] + '</td>';
            }
        }
    }
    invoice_list += '</table>';
    document.getElementById('main_text').innerHTML = invoice_list;
}
function show_map_div(){
    document.getElementById('main_text').innerHTML = '';
    showBlock('detail',false);
    showBlock('TGMap',true);
}
function showBlock(blockid, status){
    document.getElementById(blockid).style.display = (status==true)?"block":"none";
}