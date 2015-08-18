invoice_idx = shop_data[0].length-1; // 發票list位於商家list的位置
item_idx = shop_data[0][invoice_idx][0].length-1; // list位於發票list的位置
function showBlock(blockid, status){
    document.getElementById(blockid).style.display = (status==true)?"block":"none";
}
function show_map_div(){
    document.getElementById('main_text').innerHTML = '';
    showBlock('detail',false);
    showBlock('TGMap',true);
}
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
    window.scrollTo(0, 0); // Scroll back to the top
}
function show_all_einvoice(){
    showBlock('detail',false);
    showBlock('TGMap',false);
    var invoice_list = '<center><p><font color="blue" size="+4">電子發票清單</font></p></center>'
    + '<table class="table table-hover"><tr><th>順序</th><th>消費日期</th><th width="20%">載具</th><th>商店名稱</th><th>消費金額</th><th>發票號碼</th>';
    var count = 1;
    for(i=einvoice_list.length-1;i>=0;--i,++count){
        invoice_list += '<tr><td>' + count + '</td>'; // 順序
        for(j=0;j<6;++j){
            if(j==1){ // invoice.card_type
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
    window.scrollTo(0, 0);  // Scroll back to the top
}


// ======== used function when doing accounting  ============//

// get today's date
today_date = new Date();
today_year = today_date.getFullYear() - 1911; // 換算成民國年份
today_month = today_date.getMonth() + 1; // 取得正確月份
today_day = today_date.getDate();

function get_formated_date(yyy, mm, dd){
    var date_string = yyy + '/' ;
    if(mm<10) date_string += '0';
    date_string += mm + '/';
    if(dd<10) date_string += '0';
    date_string += dd;
    return date_string;
}
function isString(test_string){
    return (typeof test_string === 'string' || test_string instanceof String);
}

function get_query_date_string(type){ // get html string to create <slect> menu to choose option with year/month/day
    var query_date_str = '';
    var onclick_string = '';
    if(type=='y' || type=='m' || type=='d'){
        query_date_str = '<select id="select_year">\
        <option selected>' + today_year + '</option>\
        <option>' + (today_year - 1) + '</option>\
        </select>年';
    }
    if(type=='m' || type=='d'){
        query_date_str += '<select id="select_month">';
        for(var i = 1; i<=12; ++i){
            query_date_str += '<option';
            if(i==today_month) query_date_str+=' selected>';
            else query_date_str+='>';
            query_date_str += i + '</option>';
        }
        query_date_str += '</select>月';
    }
    if(type == 'd'){
        query_date_str += '<select id="select_day">';
        for(var i=1; i<=31; ++i){
            query_date_str += '<option';
            if(i==today_day) query_date_str+=' selected>';
            else query_date_str+='>';
            query_date_str += i + '</option>';
        }
        query_date_str += '</select>日';
    }
    if(type=='o'){
        query_date_str = '<input id="input1_year" placeholder="年" size="3" maxlength="3" value="' + (today_year-1) + '">年\
        <input id="input1_month" placeholder="月" size="3" maxlength="2" value="1">月\
        <input id="input1_day" placeholder="日" size="3" maxlength="2" value="1">日  <font color="blue">至</font>  \
        <input id="input2_year" placeholder="年" size="3" maxlength="3" value="' + today_year + '">年\
        <input id="input2_month" placeholder="月" size="3" maxlength="2" value="' +today_month + '">月\
        <input id="input2_day" placeholder="日" size="3" maxlength="2" value="' + today_day + '">日';
    }

    switch(type){
        case 'y':
            onclick_string = "['select_year', 1, 1], ['select_year', 12, 31]";
            break;
        case 'm':
            onclick_string = "['select_year', 'select_month', 1], ['select_year', 'select_month', 31]";
            break;
        case 'd':
            onclick_string = "['select_year', 'select_month', 'select_day'], ['select_year', 'select_month', 'select_day']";
            break;
        case 'o':
            onclick_string = "['input1_year', 'input1_month', 'input1_day'], ['input2_year', 'input2_month', 'input2_day']";
            break;
        default:
    }
    return query_date_str + '　<input type="button" class="btn btn-danger" value="提交" onClick="change_query_date(' + onclick_string + ');">';
}
function change_query_date_div(type){ // change the panel which is the place for user to input
    document.getElementById('query_date').innerHTML =  get_query_date_string(type) ;
}

function change_query_date(start_date_param, end_date_param){ // change the content of accounting table when user press submit button
    for(var i=0; i<start_date_param.length; ++i){
        if( isString(start_date_param[i]) ) start_date_param[i] = document.getElementById(start_date_param[i]).value;
    }
    for(var i=0; i<end_date_param.length; ++i){
        if( isString(end_date_param[i]) ) end_date_param[i] = document.getElementById(end_date_param[i]).value;
    }
    document.getElementById('accounting_table').innerHTML = get_accounting_table(
        get_formated_date( start_date_param[0], start_date_param[1], start_date_param[2] ),
        get_formated_date( end_date_param[0], end_date_param[1], end_date_param[2] )
    );
}


einvoice_list_item_idx = einvoice_list[0].length-1; // list位於sorted發票list的位置
total_price_idx = 4;
shop_idx = 3;
function get_accounting_table(start_date, end_date){
    if(start_date ==null) start_date = einvoice_list[0][0];
    if(end_date == null) end_date = einvoice_list[einvoice_list.length-1][0];
    var item_count = 0; // 計算商品數目
    var total_amount = 0; // 計算總金額
    accounting_table_str = '<table class="table table-hover">\
    <tr><th>順序</th><th>日期</th><th>商店名稱</th><th>商品名稱</th><th>數量</th><th>單價</th><th>總價</th></tr>';
    for(var i=einvoice_list.length-1;i>=0;--i){ // query sorted invoice list
        var cur_date = einvoice_list[i][0];
        if(start_date <= cur_date && cur_date <= end_date){
            var shop_detail = '<td>' + cur_date + '</td><td>' + einvoice_list[i][shop_idx] + '</td>';
            var items_array = einvoice_list[i][einvoice_list_item_idx];
            for(var j=0;j<items_array.length;++j){ // 購買品項 商品名稱 數量 單價 總價
                if( parseInt(items_array[j][total_price_idx]) == 0) continue;
                var item_detail = '';
                ++item_count;
                total_amount += parseInt(items_array[j][total_price_idx]);
                for(var kk=1;kk<items_array[j].length;++kk){
                    item_detail += '<td>' + items_array[j][kk] + '</td>';
                }
                accounting_table_str += '<tr><td>' + item_count + '</td>' + shop_detail + item_detail + '</tr>';
            }
        }
    }
    accounting_table_str += '</table><font color="blue" size="+2">消費總金額：' + total_amount + '</font>';
    return accounting_table_str;
}
function accounting(){ // show the accounting page
    showBlock('detail',false);
    showBlock('TGMap',false);
    var accounting_list = '<center><p><font color="blue" size="+4">記帳</font></p>'
    + '<div class="btn-group" data-toggle="buttons">\
  <label class="btn btn-default" onClick="change_query_date_div(\'y\');">\
    <input type="radio" name="options" id="option1" autocomplete="off">年\
  </label>\
  <label class="btn btn-default active" onClick="change_query_date_div(\'m\');">\
    <input type="radio" name="options" id="option2" autocomplete="off" checked>月\
  </label>\
  <label class="btn btn-default" onClick="change_query_date_div(\'d\');">\
    <input onClick="alert(\'fuck\');" type="radio" name="options" id="option3" autocomplete="off">日\
  </label>\
  <label class="btn btn-default" onClick="change_query_date_div(\'o\');">\
    <input type="radio" name="options" id="option3" autocomplete="off">自訂\
  </label>\
</div>\
<br />\
<div id="query_date" style="padding: 10px">' + get_query_date_string('m') + '</div>\
</center>';
    var start_date = get_formated_date(today_year, today_month, 1);
    var end_date = get_formated_date(today_year, today_month, today_day);
    document.getElementById('main_text').innerHTML =  accounting_list
     + '<div id="accounting_table">' +get_accounting_table(start_date, end_date) + '</div>';
    window.scrollTo(0, 0);  // Scroll back to the top
}