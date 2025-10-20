$(document).ready(function(){
    $('#open-config').on('click', function(e){
        $('#configuracoes').fadeIn()
    })
    $('#close-config').on('click', function(e){
        $('#configuracoes').fadeOut()
    })
})