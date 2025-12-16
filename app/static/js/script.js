$(document).ready(function(){
    $('#open-config').on('click', function(e){
        $('#configuracoes').fadeIn()
    })
    $('#close-config').on('click', function(e){
        $('#configuracoes').fadeOut()
    })

    //masks
    $('.celular').mask('(00)00000-0000');
    $('.peso').mask('##0.0', {reverse: true});

    $('[data-medida]').on('click', function(e){
        e.preventDefault();
        alert(e.target.href)
    })

})