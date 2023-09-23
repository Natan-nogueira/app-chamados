$(document).ready(function() {
    $(".at_interacoes").click(function(){
        $(".descricao").slideUp();
        $(".interacoes").slideDown();
        $(".at_interacoes").addClass("active");
        $(".at_descricao").removeClass("active");
    })
    $(".at_descricao").click(function(){
        $(".interacoes").slideUp();
        $(".descricao").slideDown();
        $(".at_descricao").addClass("active");
        $(".at_interacoes").removeClass("active")
    })
})