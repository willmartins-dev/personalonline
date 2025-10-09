
$(document).ready(function(){
   function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            let cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');
   //global loader
   $('#loader').hide();

   $('[data-id]').on('keyup', function(e){
      
         const buscar = $(this).val();
         var id_micro = e.target.dataset.id;
         var url_query = $(this).data('url');
         const url_busca_exercicio = url_query+'?buscar='+buscar+'&id_micro='+id_micro;
         
      if(buscar.length>2){
         
         $.ajax({
            url:url_busca_exercicio,
            type:'GET',
            data:{
               'buscar':buscar,
               'id_micro':id_micro,
            },
            dataType:'html',
            success:function(data){
               $('.resultado-busca').html(data)
               
               const queryString = url_busca_exercicio;
               const params = new URLSearchParams(queryString.split('?')[1])
               

               const addExercicio = document.querySelectorAll('[data-clickcheck]')
               addExercicio.forEach(item => {
                  item.addEventListener('click',function(e){
                     e.preventDefault();
                     $('#success-add').slideDown(300).delay(800);
                     $('#success-add').slideUp(300).delay(800);

                     const urlInserir = e.target.dataset.url2;
                     const urlImg = e.target.dataset.img;
                     const nome = e.target.dataset.nome;
                     const checkList = e.target.dataset.clickcheck;
                     const id_sessao = params.get('id_micro');
                    
                     $.post({
                        url:urlInserir,
                        headers:{
                           'X-CSRFToken':csrftoken,
                        },
                        data:{
                        'id_micro':id_sessao,
                        'url':urlImg,
                        'exercicio':nome,
                        },
                        success:function(data){
                           $('#'+checkList).removeClass('hidden');
                        },
                     })
                  })
               })

            }

         })
      }else{

      }
   })

   $('[data-modal-busca]').on('click', function(e){
      e.preventDefault()

      const inputBusca = document.getElementById('input-busca');
      inputBusca.dataset.id=$(this).data('modal-busca');
      
      $('#modal').removeClass('hidden')
   })

   $('.fechar').on('click',function(e){
      e.preventDefault()
      const inputBusca = document.getElementById('input-busca');
      inputBusca.dataset.id="";
      $('.resultado-busca').html('');

      $('#modal').addClass('hidden')
   })

})