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
  if (id == "pic-overlay")
  {
    document.getElementById("clicked").click();
  }
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
    if(target != "drop-log-sign" && target != "show" && target != "prfl" && target != "arr")
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

function changeFilterMessage()
{
  let newPlaceholder = "Search";
  var toChange = document.getElementsByName('lookup')[0];
  if (toChange.placeholder == newPlaceholder)
  {
    newPlaceholder = "Filter by users...";
}
  toChange.placeholder = newPlaceholder;
}

function restrictUnchecked()
{
    var form = document.querySelectorAll("[name ='usr_role']");
    var selected = null;
    var filtButton = document.getElementById("Filter");
    for (selection of form)
    {
      if (selection.checked)
      {
          filtButton.style.pointerEvents = "auto";
          filtButton.style.opacity = "1";
          selected = selection;
          break;
      }
    }
    if (selected == null)
    {
      filtButton.style.pointerEvents = "none";
      filtButton.style.opacity = "0.5";
      filtButton.title = "Select at least one option.";
    }
}

function saveChecked()
{
    saved = "values="
    var form = document.querySelectorAll("[name ='usr_role']");
    for (i = 0; i< form.length; i++)
    {
        if (form[i].checked == true)
        {
            saved += String(i);
        }
    }
    document.cookie = saved;
}

function hideGreeting()
{
  greet = document.getElementById("greeting").style.transitionDuration = "1s";
  document.getElementById("greeting").style.display = "none";
}

function displayPreview()
{
  var upload = document.getElementById("img");
  var file = upload.files[0];
  prev = document.querySelector(".img-prev");
  if (file)
  {
    const reader = new FileReader();
    prev.style.display = "block";
    reader.readAsDataURL(file);
    reader.addEventListener("load", function()
    {
        prev.setAttribute("src", this.result);
    });
  }
}

function generate_html(post)
{
  var modified = post.date_modified ? `updated: ${post.date_modified}` : "";
    return `<div class="read">
              <h2 style ="text-align: center">${post.title}</h2>
              <div class = "read-img" style = "pointer-events: auto;">
                <img src = '/${post.img_src}'>
                </div>
              <h4>Written by:${post.auth}</h4>
              <p>${post.content}</p>
              <p style ="float:right">created:${post.created}<br>${modified}</p>
            </div>`;
}

function get_404_html()
{
    return `<div style = "text-align:center;">
    <h2>404. NOT FOUND</h2>
    <h3>It seems that there is no post with the specified id.<h3>
    <h3>If you entered the URL manually, please check the spelling<h3>
    <h3>or go to front page and select from one of listed posts.</h3>
  </div>`;
}

function get_post(id)
{ 
  fetch(`/api/post/${id}/`)
    .then(res => res.json())
    .then(post => {
      document.getElementById("post").innerHTML = generate_html(post);
    })
    .catch(error => {
      error = get_404_html()
    document.getElementById("post").innerHTML = error});
}
