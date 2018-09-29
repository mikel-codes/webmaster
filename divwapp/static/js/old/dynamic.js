$(document).ready(function(){
  if(!$("input[type='text']#first").val() == "")
	$("input[type='text']#first").parents(".form-group").addClass("focused")
  if(!$("input[type='text']#second").val() == "")
	$("input[type='text']#second").parents(".form-group").addClass("focused")
  if(!$("input[type='text']#third").val() == "")
	$("input[type='text']#third").parents(".form-group").addClass("focused")

  $("input[type='text']").focus(function(){
	$(this).parents(".form-group").addClass("focused")
  })

  $("input[type='text']").blur(function(){
	var inputValue = $(this).val()
	if(inputValue == ""){
	  $(this).removeClass("filled")
	  $(this).parents(".form-group").removeClass("focused")
	}
	else{
	  $(this).addClass("filled")
	  $(this).parents(".form-group").addClass("focused")

	}
  })

  if($("input[type='text']").hasClass("filled") && $("input[type='text']").val() != ""){
	$(this).parents(".form-group").addClass("focused")
	}
  
});




