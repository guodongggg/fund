$(document).ready(function(){
    console.log('加载提交方法...')
    $(".delete").click(function(){
        var delete_btn = $(this)
        var code = delete_btn.parent().siblings(".code").text();
        console.log('delete code：',code);
        $.ajax({
            url: "/api/fund/delete",
            type: "get",
            data: {'code':code},
            dataType: "json",
            success: function(data){
                delete_btn.parent().parent().remove();
                console.log('data：',data['data']);
                updateMoney(data);
            }
        })
    });

    $(".update").click(function(){
        var update_btn = $(this);
        var code = update_btn.parent().siblings(".code").text();
        console.log('update code：',code);
        var money = update_btn.siblings(".value").val();
        if (money != "" && money > 0){
            $.ajax({
                url: "/api/fund/update",
                type: "get",
                data: {
                'code':code,
                'money': money
                },
                dataType: "json",
                success: function(data){
                    update_btn.siblings(".value").val("")
                    console.log('data：',data['data']);
                    updateMoney(data);
                }
            })
        }else{
            alert("更新持仓为空！")
        }
    })

    $("#create_btn").click(function(){
        var create_btn = $(this);
        var code = $("#create_code").val();
        var money = $("#create_money").val();
        console.log('create code：',code);
        console.log('create money：',money);
        if (money != "" && money >0 && code != ""){
            $.ajax({
                url: "/api/fund/create",
                type: "get",
                data: {
                'code':code,
                'money': money
                },
                dataType: "json",
                success: function(data){
                    create_btn.siblings().val("")
                    console.log('data：',data['data']);
                    updateMoney(data);
                    setTimeout(function flash(){window.location.reload();},1000);
                }
            })
        }else{
            alert("新增持仓为空！")
        }
    })

    function updateMoney(data){
        if (data['result']){
            var codelist = Object.keys(data['data'])
            console.log(codelist)
            codelist.forEach(function(i){
                var money = data['data'][i]['percent'] * 100
                var count = data['data'][i]['count']
                $(`#${i}`).find(".value").attr("placeholder", `${money}% ￥${count}`);
                console.log(i,' finish')
            })
        }else{
            alert('执行异常，请检查！')
        }
    }

    console.log('完毕.')

})
