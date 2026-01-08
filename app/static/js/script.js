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
    $('.peso2').mask('##0,0', {reverse: true});

    $('[data-medida]').on('click', function(e){
        e.preventDefault();
        alert(e.target.href)
    })
    $('.atualiza-peso').on('click', function(e){
        $('.modal-atualiza-peso').fadeIn()
    })
    $('.fechar-atualiza-peso').on('click', function(e){
        $('.modal-atualiza-peso').fadeOut()
    })
      $('.form-comparar').on('submit', function(e){
      e.preventDefault();
      const url = e.target.action;
      const data_antiga = $("#data_antiga").val()
      const data_atual = $("#data_atual").val()
      const params = url+'?data1='+data_antiga+'&data2='+data_atual
      
      $.ajax({
         url:params,
         method:'GET',
         success:function(data){
            $('#modal-medidas').fadeIn()
            $('#mostrar-resultado').load(params)
         }
      })
   })
   $('#close-medidas').on('click', function(){
    $('#modal-medidas').fadeOut();
   })
})