window.onload = function () {

    var as = document.getElementsByClassName("content-header")[0].getElementsByTagName("a");
    console.log(as.length);
    var contents = document.getElementsByClassName("dom");
    console.log(contents.length);
    // 遍历
    for (var i=0; i < as.length; i++) {
        console.log("aaaaaaaaaaaaa");
        var a=as[i];
        console.log(a);
        a.id=i;
        // 监听鼠标的点击事件
        console.log(a);
        a.onclick=function () {
            for (var j=0;j<as.length;j++){
                //清除a的所有样式
                as[j].className='';
                contents[j].style.display='none';
            }

            // 设置当前a的class
            this.className="current";
            // 从contents数组中取出对应的标签
            contents[this.id].style.display="block"
        }
    }
};