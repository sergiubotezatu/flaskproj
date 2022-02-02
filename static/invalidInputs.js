function InvalidAlert() 
{
    document.getElementById("invalid").innerHTML = "";
    document.getElementById("auth").style.backgroundColor = "white";
    var input = document.getElementById("auth").value.slice(-1);
    const pattern = /[1-9a-z]/gi;
    if (!pattern.test(input) && input != "")
    {
       document.getElementById("invalid").innerHTML = "Letters & numbers only!";
       document.getElementById("auth").style.backgroundColor = "rgba(201, 37, 22, 0.7)";
    }    
}