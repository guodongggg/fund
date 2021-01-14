function redorgreen(){
    var num = document.getElementsByClassName('num');
    var list = Array.from(num);
    list.map(function(item){
        value = item.textContent.replace('%','');
        if (value > 0){
            item.style.color = 'red';
        }
        else {
            item.style.color = 'green';
        }
    })}
redorgreen();