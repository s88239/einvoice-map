invoice_idx = shop_data[0].length-1; // 發票list位於商家list的位置
item_idx = shop_data[0][invoice_idx][0].length-1; // list位於發票list的位置
enterprise_array = []; // format at each term: [enterprise,branch_idx_array,freq,total amount]
function showBlock(blockid, status){
    document.getElementById(blockid).style.display = (status==true)?"block":"none";
}
function show_map_div(){
    showBlock('main_text',false);
    showBlock('detail',false);
    showBlock('einvoice_detail',false);
    showBlock('TGMap',true);
}
function get_invoice_list_table_at_shop(invoice_array){
    var invoice_list_table_str = '<table class="table">\
    <tr class="row header">\
        <th class="cell">順序</th><th>日期</th><th class="cell">發票號碼</th><th class="cell">總金額</th><th class="cell">#</th><th class="cell">商品名稱</th><th class="cell">數量</th><th class="cell">單價</th><th class="cell">總價</th></tr>';
    for(var i=0;i<invoice_array[invoice_idx].length;++i){ // 第幾張發票
        var items_array = invoice_array[invoice_idx][i][item_idx]; // 該張發票所有購買商品
        var item_num = items_array.length; // 該張發票商品筆數
        var invoice_list_table_str = invoice_list_table_str  + '<tr class="row"><td class="cell" rowspan="' + item_num + '">' + (i+1) + '</td>'; // 順序
        for(var j=0;j<invoice_array[invoice_idx][i].length-1;++j){ // 日期 發票號碼 總金額
            invoice_list_table_str = invoice_list_table_str + '<td class="cell" rowspan="' + item_num + '">' + invoice_array[invoice_idx][i][j] + '</td>';
        }
        for(var j=0;j<item_num;++j){ // 購買品項 商品名稱 數量 單價 總價
            if(j!=0) invoice_list_table_str += '<tr class="row">';
            invoice_list_table_str += '<td class="cell">' + (j+1) + '</td>';
            for(var kk=0;kk<items_array[j].length;++kk){
                invoice_list_table_str = invoice_list_table_str + '<td class="cell">' + items_array[j][kk] + '</td>';
            }
            invoice_list_table_str += '</tr>';
        }
    }
    invoice_list_table_str += '</table>';
    return invoice_list_table_str;
}
function get_invoice_list_string(invoice_array){
    var delimeter = (invoice_array[3]=='' || invoice_array[4]=='')?'':'-';
    var invoice_list = '<center><a href="javascript:showBlock(\'detail\', false)">close</a><h1><font color="blue">'
    + invoice_array[3] + delimeter + invoice_array[4]
    + '</font></h1>';
    return invoice_list + get_invoice_list_table_at_shop(invoice_array);
}
function show_all_shop(){
    showBlock('detail',false);
    showBlock('einvoice_detail',false);
    showBlock('TGMap',false);
    showBlock('main_text',true);
    var invoice_list = '<div class="title" align="center"><h2>商店清單</h2></div>\
    <div class="col-lg-4 col-lg-offset-4" style="margin-bottom: 20px">\
        <div class="input-group">\
          <input id="search" type="text" class="form-control" aria-label="..." placeholder="e.g. 統一超商-台大">\
          <div class="input-group-btn">\
            <button type="button" class="btn btn-default dropdown-toggle" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">搜尋 <span class="caret"></span></button>\
            <ul class="dropdown-menu dropdown-menu-right">\
              <li><a href="javascript: search_shop(\'name\');">商店名稱</a></li>\
              <li><a href="javascript: search_shop(\'address\');">商品地址</a></li>\
              <li><a href="javascript: search_shop(\'item_name\');">商品名稱</a></li>\
            </ul>\
          </div>\
        </div>\
    </div>\
    <table id="shop_table" class="table">\
        <tr class="row header blue"><th class="cell">順序</th><th class="cell">商店名稱</th><th class="cell">分店名稱</th><th class="cell">商店地址</th><th class="cell">頻率</th><th class="cell">消費金額</th><th class="cell">最常購買品項</th><th class="cell">cluster</th>';
    for(i=0;i<shop_data.length;++i){
        invoice_list += get_row_of_shop(i, i+1);
    }
    invoice_list += '</table>';
    document.getElementById('main_text').innerHTML = invoice_list;
    document.getElementById('main_text').scrollTop = 0; // Scroll back to the top
}
function search_shop(search_col){
    var count = 0;
    var search_goal = document.getElementById('search').value;
    var result_str = '<tr class="row header blue"><th class="cell">順序</th><th class="cell">商店名稱</th><th class="cell">分店名稱</th><th class="cell">商店地址</th><th class="cell">頻率</th><th class="cell">消費金額</th><th class="cell">最常購買品項</th><th class="cell">cluster</th>';
    var find_item_flag = false;
    for(var shop_idx=0 ; shop_idx < shop_data.length; ++shop_idx){
        if( search_col=='item_name' ){
            for(var current_invoice_idx=0; current_invoice_idx<shop_data[shop_idx][invoice_idx].length; ++current_invoice_idx){ // 第幾張發票
                var items_array = shop_data[shop_idx][invoice_idx][current_invoice_idx][item_idx]; // 該張發票所有購買商品
                for( var current_item_idx=0; current_item_idx<items_array.length; ++current_item_idx){
                    if( items_array[current_item_idx][0].indexOf(search_goal)!=-1 ){
                        result_str += get_row_of_shop(shop_idx, ++count);
                        find_item_flag = true;
                        break;
                    }
                }
                if( find_item_flag==true){
                    find_item_flag = false;
                    break;
                }
            }
        }
        else{
            if( search_col=='name' ){
                search_goal_split = search_goal.split("-");
                search_shop_val = shop_data[shop_idx][3];
                search_branch_val = shop_data[shop_idx][4];
                if(search_goal_split.length==1){
                    if(search_shop_val.indexOf(search_goal)!=-1 || search_branch_val.indexOf(search_goal)!=-1 ){
                        result_str += get_row_of_shop(shop_idx, ++count);
                    }
                }
                else if( search_shop_val.indexOf(search_goal_split[0])!=-1
                    && search_branch_val.indexOf(search_goal_split[1])!=-1 ){
                    result_str += get_row_of_shop(shop_idx, ++count);
                }
            }
            else if( search_col=='address' ){
                var current_shop_address = shop_data[shop_idx][5].replace("臺","台");
                current_broken_address = break_address(current_shop_address);
                var search_goal = search_goal.replace("臺","台");
                search_broken_address = break_address(search_goal);
                if( ( search_broken_address[0]=='' || search_broken_address[0]==current_broken_address[0] ) 
                    && (search_broken_address[1]=='' || search_broken_address[1]==current_broken_address[1])
                    && (search_broken_address[2]=='' || current_broken_address[2].indexOf(search_broken_address[2])!=-1 )
                    || current_shop_address.indexOf(search_goal)!=-1 ){
                    result_str += get_row_of_shop(shop_idx, ++count);
                }
            }
        }
    }
    document.getElementById('shop_table').innerHTML = result_str;
}
function get_row_of_shop(shop_idx, count){
    var invoice_list = '<tr class="row" onClick="show_einvoice(' + shop_idx + ');"><td class="cell">' + count + '</td>';
    for(j=3;j<shop_data[shop_idx].length-1;++j){
        invoice_list += '<td class="cell">' + shop_data[shop_idx][j] + '</td>';
    }
    return invoice_list;
}
function break_address(address){ // 分解地址成 [縣市,鄉鎮市區,其他]
    var county = '';
    var town = '';
    var others = '';
    if( (current_position = address.indexOf('縣'))!=-1 ){
        county = address.substring(0,current_position+1);
        test_char = ['鄉','鎮','市'];
        for(var test_idx=0; test_idx<test_char.length; ++test_idx){
            current_position = address.indexOf(test_char[test_idx]);
            town = address.substring(3,current_position+1);
            others = address.substring(current_position+1);
            break;
        }
    }
    else if( (current_position = address.indexOf('市'))!=-1 ){
        county = address.substring(0,current_position+1);
        test_city = ['台北','新北','基隆','桃園','新竹','台中','嘉義','台南','高雄']; // 直轄市、省轄市
        city_flag = false;
        for( city_idx in test_city){
            if( county.indexOf(test_city[city_idx])!=-1 ){
                county = address.substring(0,3);
                city_flag = true;
            }
        }
        if(city_flag==false){ // 縣轄市
            town = county;
            county = ''; // 沒有縣名
            others = address.substring(3);
        }
        else if( (current_position = address.indexOf('區'))!=-1){
            town = address.substring(3,current_position+1);
            others = address.substring(current_position+1);
        }
        else{
            town = ''; // 沒有區名
            others = address.substring(3);
        }
    }
    else{
        if( (current_position = address.indexOf('鄉'))!=-1
            || (current_position = address.indexOf('鎮'))!=-1
            || (current_position = address.indexOf('區'))!=-1){
            town = address.substring(0,current_position+1);
            others = address.substring(current_position+1);
        }
        else{
            others = address;
        }
    }
    return [county,town,others];
}

einvoice_list_item_idx = einvoice_list[0].length-1; // list位於sorted發票list的位置
total_price_idx = 4;
shop_idx = 3;
function show_einvoice(target_shop_idx){
    invoice_array = shop_data[target_shop_idx];
    var delimeter = (invoice_array[3]=='' || invoice_array[4]=='')?'':'-';
    var invoice_list = '<button type="button" class="btn btn-info" onClick="showBlock(\'einvoice_detail\', false);showBlock(\'main_text\', true);">返回電子發票列表</button>\
    <font color="white"><center><h1>'+ invoice_array[3] + delimeter + invoice_array[4] + '</h1>'
    + invoice_array[5] // 地址
    +'</font><h3><font color="#FFAFFE"><b>頻率：' + invoice_array[6] + '</font>　<font color="FFD8AF">總消費金額：' + invoice_array[7] + '</font></b></h3>' // 頻率及總消費金額
    +'<font color="white" size="+1">最常購買商品：' + invoice_array[8] + '</font></center><br />'; //最常購買商品
    showBlock('main_text',false);
    showBlock('einvoice_detail',true);
    document.getElementById('einvoice_detail').innerHTML = invoice_list + get_invoice_list_table_at_shop(shop_data[target_shop_idx]);
}
function show_all_einvoice(){
    showBlock('detail',false);
    showBlock('einvoice_detail',false);
    showBlock('TGMap',false);
    showBlock('main_text',true);
    var invoice_list = '<div class="title" align="center"><h2>電子發票清單</h2></div>\
    <div class="col-lg-4 col-lg-offset-4" style="margin-bottom: 20px">\
        <div class="input-group">\
          <input id="search" type="text" class="form-control" aria-label="..." placeholder="Search">\
          <div class="input-group-btn">\
            <button type="button" class="btn btn-default dropdown-toggle" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">搜尋 <span class="caret"></span></button>\
            <ul class="dropdown-menu dropdown-menu-right">\
              <li><a href="javascript: search_einvoice(\'name\');">商店名稱</a></li>\
              <li><a href="javascript: search_einvoice(\'item_name\');">商品名稱</a></li>\
            </ul>\
          </div>\
        </div>\
    </div>\
    <table id="einvoice_table" class="table"><tr class="row header blue"><th class="cell">順序</th><th class="cell">消費日期</th><th class="cell" width="20%">載具</th><th class="cell">商店名稱</th><th class="cell">消費金額</th><th class="cell">發票號碼</th></tr>';
    var einvoice_count = 1;
    for(i=einvoice_list.length-1;i>=0;--i,++einvoice_count){
        invoice_list += get_row_of_einvoice(i, einvoice_count);
    }
    invoice_list += '</table>';
    document.getElementById('main_text').innerHTML = invoice_list;
    document.getElementById('main_text').scrollTop = 0; // Scroll back to the top of div
}
function show_items(target_einvoice_idx){
    var total_amount = einvoice_list[target_einvoice_idx][total_price_idx]; // 發票總金額
    var items_table_str = '<table width="100%"><tr><td><button type="button" class="btn btn-info" onClick="showBlock(\'einvoice_detail\', false);showBlock(\'main_text\', true);">返回電子發票列表</button></td>'
    + '<td align="right"><span class="label label-default">' + einvoice_list[target_einvoice_idx][5] + '</span></td></tr></table>'
    + '<center><font color="white" size="+1"><h3>' + einvoice_list[target_einvoice_idx][0] + '</h3></font>'
    + '<h2><font color="white">' + einvoice_list[target_einvoice_idx][3] + '</font></h2>\
    <h3><font color="white">消費總金額：' + total_amount + '</font></h3></center>\
    <table class="table">\
    <tr class="row header green"><th class="cell">#</th><th class="cell">商品名稱</th><th class="cell">數量</th><th class="cell">單價</th><th class="cell">總價</th></tr>';
    var items_array = einvoice_list[target_einvoice_idx][einvoice_list_item_idx];
    for(var i=0;i<items_array.length;++i){ // # 商品名稱 數量 單價 總價
        items_table_str += '<tr class="row"><td class="cell">' + (i+1) + '</td>';
        for(var j=0;j<items_array[i].length;++j){
            items_table_str += '<td class="cell">' + items_array[i][j] + '</td>';
        }
        items_table_str += '</tr>';
    }
    items_table_str += '</table>';
    showBlock('main_text',false);
    showBlock('einvoice_detail',true);
    document.getElementById('einvoice_detail').innerHTML = items_table_str;
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

    if(type=='s'){
        query_date_str = '<div class="col-lg-4 input-group">\
              <input id="search" type="text" class="form-control" aria-label="..." placeholder="Search">\
              <div class="input-group-btn">\
                <button type="button" class="btn btn-default dropdown-toggle" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">搜尋 <span class="caret"></span></button>\
                <ul class="dropdown-menu dropdown-menu-right">\
                  <li><a href="javascript: search_item(\'name\');">商店名稱</a></li>\
                  <li><a href="javascript: search_item(\'item_name\');">商品名稱</a></li>\
                </ul>\
              </div>\
            </div>\
        </div>';
        return query_date_str;
    }
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

function get_accounting_table(start_date, end_date){
    if(start_date ==null) start_date = einvoice_list[0][0];
    if(end_date == null) end_date = einvoice_list[einvoice_list.length-1][0];
    item_count = 1;
    var total_amount = 0; // 計算總金額
    accounting_table_str = '<table id="item_table" class="table">\
    <tr class="row header green"><th class="cell">順序</th><th class="cell">日期</th><th class="cell">商店名稱</th><th class="cell">商品名稱</th><th class="cell">數量</th><th class="cell">單價</th><th class="cell">總價</th></tr>';
    for(var i=einvoice_list.length-1;i>=0;--i){ // query sorted invoice list
        var cur_date = einvoice_list[i][0];
        if(start_date <= cur_date && cur_date <= end_date){
            total_amount += parseInt(einvoice_list[i][total_price_idx]);
            accounting_table_str += get_row_of_einvoice_with_item(i);
        }
    }
    return '<div id="total_amount" align="center"><h2>' + total_amount + '</h2></div>' + accounting_table_str;
}
function accounting(){ // show the accounting page
    showBlock('detail',false);
    showBlock('einvoice_detail',false);
    showBlock('TGMap',false);
    showBlock('main_text',true);
    var accounting_list = '<div class="title" align="center"><h2>記帳</h2></div>\
    <center><div class="btn-group" data-toggle="buttons">\
      <label class="btn btn-default" onClick="change_query_date_div(\'y\');">\
        <input type="radio" name="options" id="option1" autocomplete="off">年\
      </label>\
      <label class="btn btn-default active" onClick="change_query_date_div(\'m\');">\
        <input type="radio" name="options" id="option2" autocomplete="off" checked>月\
      </label>\
      <label class="btn btn-default" onClick="change_query_date_div(\'d\');">\
        <input type="radio" name="options" id="option3" autocomplete="off">日\
      </label>\
      <label class="btn btn-default" onClick="change_query_date_div(\'o\');">\
        <input type="radio" name="options" id="option3" autocomplete="off">自訂\
      </label>\
      <label class="btn btn-default" onClick="change_query_date_div(\'s\');">\
        <input type="radio" name="options" id="option3" autocomplete="off">搜尋\
      </label>\
    </div>\
    <br />\
    <div id="query_date" style="padding-top: 10px">' + get_query_date_string('m') + '</div>\
    <h3><span class="label label-warning">消費總金額</span></h3>\
    </center>';
    var start_date = get_formated_date(today_year, today_month, 1);
    var end_date = get_formated_date(today_year, today_month, today_day);
    document.getElementById('main_text').innerHTML =  accounting_list
    + '<div id="accounting_table">' + get_accounting_table(start_date, end_date) + '</div>';
    document.getElementById('main_text').scrollTop = 0; // Scroll back to the top of div
}
function search_einvoice(search_col){
    var search_goal = document.getElementById('search').value;
    var result_str = '<tr class="row header blue"><th class="cell">順序</th><th class="cell">消費日期</th><th class="cell" width="20%">載具</th><th class="cell">商店名稱</th><th class="cell">消費金額</th><th class="cell">發票號碼</th></tr>'
    + search_each_einvoice('einvoice', search_col, search_goal);
    document.getElementById('einvoice_table').innerHTML = result_str;
}
function get_row_of_einvoice(einvoice_idx, count){
    var invoice_list = '<tr class="row" onClick="show_items(' + einvoice_idx + ');"><td>' + count + '</td>'; // 順序
    for(var j=0;j<6;++j){
        if(j==1){ // invoice.card_name
            invoice_list += '<td class="cell">' + einvoice_list[einvoice_idx][j] + ' ' + einvoice_list[einvoice_idx][++j] + '</td>';
        }
        else{
            invoice_list += '<td class="cell">' + einvoice_list[einvoice_idx][j] + '</td>';
        }
    }
    invoice_list += '</tr>';
    return invoice_list;
}
function search_item(search_col){
    item_count = 1;
    var search_goal = document.getElementById('search').value;
    var accounting_table_str = '<tr class="row header green"><th class="cell">順序</th><th class="cell">日期</th><th class="cell">商店名稱</th><th class="cell">商品名稱</th><th class="cell">數量</th><th class="cell">單價</th><th class="cell">總價</th></tr>'
    + search_each_einvoice('item', search_col, search_goal);
    document.getElementById('item_table').innerHTML = accounting_table_str;
}

function get_row_of_einvoice_with_item(einvoice_idx){
    var accounting_table_str = '';
    var shop_detail = '<td class="cell">' + einvoice_list[einvoice_idx][0] + '</td>';

    // **** get the full name of seller ***** //
    var shop_idx = einvoice_list[einvoice_idx][einvoice_list_item_idx-1];
    var shop_row = shop_data[shop_idx];
    var delimeter = (shop_row[3]=='' || shop_row[4]=='')?'':'-';
    shop_detail += '<td class="cell"><a href="javascript: show_einvoice(' + shop_idx + ');">'
    + shop_row[3] + delimeter + shop_row[4] + '</a></td>';

    var items_array = einvoice_list[einvoice_idx][einvoice_list_item_idx];
    for(var j=0;j<items_array.length;++j){ // # 商品名稱 數量 單價 總價
        if( parseInt(items_array[j][3]) == 0) continue; // 總價為0的item不列入
        var item_detail = '';
        for(var kk=0;kk<items_array[j].length;++kk){
            item_detail += '<td class="cell">' + items_array[j][kk] + '</td>';
        }
        accounting_table_str += '<tr class="row"><td class="cell">' + item_count + '</td>' + shop_detail + item_detail + '</tr>';
        ++item_count;
    }
    return accounting_table_str;
}
function get_row_of_item(einvoice_idx, current_item_idx, count){
    var accounting_table_str = '<tr class="row"><td class="cell">' + count + '</td>\
    <td class="cell">' + einvoice_list[einvoice_idx][0] + '</td>\
    <td class="cell">' + einvoice_list[einvoice_idx][shop_idx] + '</td>';
    var items_array = einvoice_list[einvoice_idx][einvoice_list_item_idx];
    for(var i=0;i<items_array[current_item_idx].length;++i){
        accounting_table_str += '<td class="cell">' + items_array[current_item_idx][i] + '</td>';
    }
    accounting_table_str += '</tr>';
    return accounting_table_str;
}
function search_each_einvoice(type, search_col, search_goal){
    var count = 0;
    var total_amount = 0;
    var result_str = '';
    var search_val = '';
    for(var i=einvoice_list.length-1; i >= 0; --i){
        if( search_col=='item_name' ){
            var items_array = einvoice_list[i][einvoice_list_item_idx];
            for(var j=0; j < items_array.length; ++j){
                if(items_array[j][0].indexOf(search_goal)!=-1){
                    total_amount += parseInt(einvoice_list[i][einvoice_list_item_idx][j][3]);
                    if(type=='einvoice'){
                        result_str += get_row_of_einvoice(i, ++count);
                        break;
                    }
                    else if(type=='item') result_str += get_row_of_item(i, j, ++count);
                }
            }
        }
        else{
            if( search_col=='name' ){
                shop_idx = einvoice_list[i][einvoice_list_item_idx-1];
                search_val = [einvoice_list[i][3], shop_data[shop_idx][3], shop_data[shop_idx][3]]; // 發票商家名稱, 商店名, 分店名
                for( current_search_val in search_val ){
                    if( search_val.indexOf(search_goal)!=-1 ){
                        if(type=='einvoice') result_str += get_row_of_einvoice(i, ++count);
                        else if(type=='item') result_str += get_row_of_einvoice_with_item(i);
                        total_amount += parseInt(einvoice_list[i][total_price_idx]);
                    }
                }
            }
        }
    }
    if(type=='item') document.getElementById('total_amount').innerHTML = '<h2>' + total_amount + '</h2>';
    return result_str;
}
function sorting(raw_data, invert){
    return sorted_data = (invert==true)?raw_data.sort(function(a, b){return b[1]-a[1]})
                                        :raw_data.sort(function(a, b){return a[1]-b[1]});
}
function get_statistics_str(type){
    if( type=='freq' ){
        type_idx = 6;
        type_name = '頻率';
    }
    else if( type=='amount' ){
        type_idx = 7;
        type_name = '消費總金額';
    }
    else return;
    var statistics_str = '<table class="table"><tr class="row header blue"><th class="cell">名次</th>\
    <th class="cell">商店名稱</th><th class="cell">分店名稱</th>\
    <th class="cell">' + type_name + '</th><th class="cell">比率</th></tr>';
    var total_num = 0;

    // ****** start sorting ******//
    var raw_data = [];
    for(var i=0; i<shop_data.length; ++i){
        total_num += shop_data[i][type_idx];
        raw_data.push( [i,shop_data[i][type_idx]] );
    }
    sorted_data = sorting(raw_data, true);
    // ****** end of sorting ******//

    for(var sort_idx = 0; sort_idx < sorted_data.length ; ++sort_idx){
        var ratio = sorted_data[sort_idx][1]/total_num * 100;
        var shop_idx = sorted_data[sort_idx][0];
        statistics_str += '<tr class="row" onClick="show_einvoice(' + shop_idx + ');"><td class="cell">' + (sort_idx+1) + '</td>\
        <td class="cell">' + shop_data[shop_idx][3] + '</td><td class="cell">' + shop_data[shop_idx][4] + '</td>\
        <td class="cell">' + shop_data[shop_idx][type_idx] + '</td><td class="cell">' + ratio.toFixed(2) + '</td></tr>';
    }
    statistics_str += '</table>';
    return statistics_str;
}
function get_statistics(type){
    document.getElementById('query_statistics').innerHTML = get_statistics_str(type);
}
function statistics(){
    showBlock('detail',false);
    showBlock('einvoice_detail',false);
    showBlock('TGMap',false);
    showBlock('main_text',true);
    var statistics_str = '<div class="title" align="center"><h2>統計資料</h2></div>\
    <center><div class="btn-group" data-toggle="buttons">\
      <label class="btn btn-default active" onClick="get_statistics(\'freq\');">\
        <input type="radio" name="options" id="option1" autocomplete="off" checked>依頻率\
      </label>\
      <label class="btn btn-default" onClick="get_statistics(\'amount\');">\
        <input type="radio" name="options" id="option2" autocomplete="off">依金額\
      </label>\
      <label class="btn btn-default" onClick="get_enterprise_statistics(\'freq\');">\
        <input type="radio" name="options" id="option3" autocomplete="off">依公司頻率\
      </label>\
      <label class="btn btn-default" onClick="get_enterprise_statistics(\'amount\');">\
        <input type="radio" name="options" id="option3" autocomplete="off">依公司金額\
      </label>\
    </div>\
    <div id="query_statistics" style="padding-top: 10px">' + get_statistics_str('freq') + '</div>';
    document.getElementById('main_text').innerHTML = statistics_str;
    document.getElementById('main_text').scrollTop = 0; // Scroll back to the top of div
    //return statistics_str;
}
function get_enterprise_statistics(type){
    calculate_enterprise_statistics();
    if( type=='freq' ){
        type_idx = 2;
        type_name = '頻率';
    }
    else if( type=='amount' ){
        type_idx = 3;
        type_name = '消費總金額';
    }
    else return;
    var enterprise_str = '<table class="table"><tr class="row header blue"><th class="cell">名次</th>\
    <th class="cell">商店名稱</th><th class="cell">分店名稱</th>\
    <th class="cell">' + type_name + '</th><th class="cell">比率</th></tr>';
    var total_num = 0;

    // ****** start sorting ******//
    var raw_data = [];
    for(var enterprise_idx = 0; enterprise_idx < enterprise_array.length; ++enterprise_idx){
        total_num += enterprise_array[enterprise_idx][type_idx];
        raw_data.push( [enterprise_idx, enterprise_array[enterprise_idx][type_idx]] );
    }
    sorted_data = sorting(raw_data, true);
    // ****** end of sorting ******//

    for(var sort_idx = 0; sort_idx < sorted_data.length; ++sort_idx){
        var ratio = sorted_data[sort_idx][1]/total_num * 100;
        var enterprise_idx = sorted_data[sort_idx][0];
        enterprise_str += '<tr class="row"><td class="cell">' + (sort_idx+1) + '</td>\
        <td class="cell">' + enterprise_array[enterprise_idx][0] + '</td><td class="cell">';
        var counted_word = 0;
        for(var i = 0; i < enterprise_array[enterprise_idx][1].length; ++i){
            shop_idx = enterprise_array[enterprise_idx][1][i];
            enterprise_str += '<a href="javascript: show_einvoice(' + shop_idx + ');">';
            enterprise_str += (shop_data[shop_idx][4]=='')? '總公司':shop_data[shop_idx][4];
            enterprise_str += '</a> ';
            counted_word += shop_data[shop_idx][4].length;
            if( counted_word>=20){
                enterprise_str += '<br />';
                counted_word = 0;
            }
        }
        enterprise_str += '</td><td class="cell">' + enterprise_array[enterprise_idx][type_idx] + '</td><td class="cell">' + ratio.toFixed(2) + '</td></tr>';
    }
    document.getElementById('query_statistics').innerHTML = enterprise_str;
}
function calculate_enterprise_statistics(){
    if( enterprise_array.length!=0 ) return; // already establish the enterprise array
    for(var shop_idx = 0; shop_idx < shop_data.length; ++shop_idx){
        in_array_flag = false;
        for(var enterprise_idx = 0; enterprise_idx < enterprise_array.length; ++enterprise_idx){
            if(shop_data[shop_idx][3] == enterprise_array[enterprise_idx][0]){
                enterprise_array[enterprise_idx][1].push(shop_idx);
                enterprise_array[enterprise_idx][2] += shop_data[shop_idx][6];
                enterprise_array[enterprise_idx][3] += shop_data[shop_idx][7];
                in_array_flag = true;
                break;
            }
        }
        if(!in_array_flag){
                enterprise_array.push( [shop_data[shop_idx][3], [shop_idx], shop_data[shop_idx][6], shop_data[shop_idx][7]]);
                //                       enterprise name   ,  shop_idx array,   total freq.       ,     total amount
        }
    }
}