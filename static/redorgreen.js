function redorgreen(){
    var num = $('.num');
    num.map(function(){
        var value = this.textContent.replace('%','');;
        if (value){
            if (value > 0){
                this.style.color = 'red';
            }
            else if (value < 0){
                this.style.color = 'green';
            }
            else{
                this.textContent = '无估值';
                this.style.color = '#666';
            }
        }
        else{
            this.textContent = '无估值';
            this.style.color = '#666';
        }
    })
}
//    var num = document.getElementsByClassName('num');
//    var list = Array.from(num);
//    list.map(function(item){
//        value = item.textContent.replace('%','');
//        if (value){
//            if (value > 0){
//                item.style.color = 'red';
//            }
//            else {
//                item.style.color = 'green';
//            }
//        }
//        else{
//            item.innerText = '无估值';
//            item.style.color = '#666';
//        }
//    })}
redorgreen();