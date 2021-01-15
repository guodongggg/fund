function redorgreen(){
    var num = document.getElementsByClassName('num');
    var list = Array.from(num);
    list.map(function(item){
        value = item.textContent.replace('%','');
        if (value){
            if (value > 0){
                item.style.color = 'red';
            }
            else {
                item.style.color = 'green';
            }
        }
        else{
            item.innerText = '无估值';
            item.style.color = '#666';
        }
    })}
redorgreen();