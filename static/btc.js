function btc(){
    var btc = document.getElementById('btc')
    value = hq_str_btc_btcbtcusd.split(',')[8]; // hq_str_btc_btcbtcusd通过https://www.usd-cny.com/btc/b.js在线获取
    btc.textContent = "BTC: "+parseInt(value);
}
btc();