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
                console.log('data：',data);
            }
        })
    });

    $(".update").click(function(){
        var update_btn = $(this);
        var code = update_btn.parent().siblings(".code").text();
        console.log('update code：',code);
        var money = update_btn.siblings(".value").val();
        if (money != ""){
            $.ajax({
                url: "/api/fund/update",
                type: "get",
                data: {
                'code':code,
                'money': money
                },
                dataType: "json",
                success: function(data){
                    console.log('data：',data);
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
        if (money != "" && code != ""){
            $.ajax({
                url: "/api/fund/create",
                type: "get",
                data: {
                'code':code,
                'money': money
                },
                dataType: "json",
                success: function(data){
                    console.log('data：',data);
                }
            })
        }else{
            alert("更新持仓为空！")
        }
    })

    console.log('完毕.')
})
