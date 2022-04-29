function InvalidAuth() 
{
    document.getElementById("invalid").innerHTML = "";
    document.getElementById("auth").style.backgroundColor = "white";
    var input = document.getElementById("auth").value.slice(-1);
    const pattern = /[1-9a-z ]/gi;
    if (!pattern.test(input) && input != "")
    {
      document.getElementById("invalid").innerHTML = "Letters & numbers only!";
      document.getElementById("auth").style.backgroundColor = "rgba(201, 37, 22, 0.7)";
    }
}

function InvalidUserName() 
{
    document.getElementById("invalid").innerHTML = "";
    document.getElementById("toCheck").style.backgroundColor = "white";
    var input = document.getElementById("toCheck").value.slice(-1);
    const pattern = /[1-9a-z ]/gi;
    if (!pattern.test(input) && input != "")
    {
      document.getElementById("invalid").innerHTML = "Letters & numbers only!";
      document.getElementById("toCheck").style.backgroundColor = "rgba(201, 37, 22, 0.7)";
    }
}

function MessOn(id)
{
  document.getElementById(id).style.display = "block";
}

function MessOff(id)
{
    document.getElementById(id).style.display = "none";
}

function InvalidPass()
{
  var input = document.getElementById("pwd").value;
  const pattern = /[^A-Za-z0-9]/g;
  if (input.length < 7)
  {
    document.getElementById("wrongFormat").innerHTML = "Password must be at least 7 chars long";
    document.getElementById("pwd").style.backgroundColor = "red";  
  }
  else if(!pattern.test(input))  
  {
    document.getElementById("wrongFormat").innerHTML = "Password must contain at least 1 special character";
    document.getElementById("pwd").style.backgroundColor = "red";  
  } 
}

function RestoreAlerted()
{
    document.getElementById("wrongFormat").innerHTML = "";
    document.getElementById("pwd").style.backgroundColor = "white";
}

function DifferentPass()
{
   document.getElementById("sub").disabled = false;
   document.getElementById("diffPass").innerHTML = "";
   document.getElementById("pwd2").style.backgroundColor = "white";
   var password = document.getElementById("pwd").value;
   var input = document.getElementById("pwd2").value;
   var toCompare = password.slice(0, input.length);
   if (input != toCompare && input != "")
   {
       document.getElementById("sub").disabled = true;
       document.getElementById("diffPass").innerHTML = "Password format is different than the initial one.";
       document.getElementById("pwd2").style.backgroundColor = "red";
   }
}

function SwitchRole(id)
{
    var role = document.getElementById(id);
    document.getElementById("y").innerHTML = role.value;
    var title = "regular";
    if (role.value == "regular")
    {
        title = "admin";
    }
    if (role.value != "default")
    {
      role.value = title;
    }
}


function showOptions(){
  
  var display = "block";
  var direction = "up";
  var arrow = document.getElementById("arr");  
  if (document.getElementById("drop-log-sign").style.display == "block")
  {
      arrow.classList.remove(direction)    
      display = "none";
      direction = "down";
    }
   document.getElementById("drop-log-sign").style.display = display;
   arrow.classList.add(direction);
   }

function hideOptions()
{
  if (document.getElementById("drop-log-sign").style.display == "block"){
    document.getElementById("drop-log-sign").style.display = "none";
    }
}

function hideDrop(event)
{
   var target = event.target.id
   var arrow = document.getElementById("arr");
    if(target != "arr" && target != "show" && target != "drop-log-sign")
    {
      document.getElementById("drop-log-sign").style.display = "none";
      arrow.classList.remove("up");
      arrow.classList.add("down");
    }
}

function filterFunction()
{
  var input, filter, ul, li, a, i;
  input = document.getElementById("search");
  filter = input.value.toUpperCase();
  div = document.getElementById("found");
  a = div.getElementsByTagName("a");
  for (i = 0; i < a.length; i++) {
    txtValue = a[i].textContent || a[i].innerText;
    if (txtValue.toUpperCase().indexOf(filter) > -1) {
      a[i].style.display = "";
    }
    else 
    {
      a[i].style.display = "none";
    }
  }
}