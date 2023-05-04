
registration.style.display = "none";
authentication.style.display = "none";
//resource.style.display = "none";

//console.log("App loaded!");
var current_id = 0

var addButton = document.querySelector("#vacation-place");

addButton.onclick = function () {
     
    var newPlaceInput1 = document.querySelector("#new-vacation-place1");
    var newPlaceInput2 = document.querySelector("#new-vacation-place2");
    var newPlaceInput3 = document.querySelector("#new-vacation-place3");
    var newPlaceInput4 = document.querySelector("#new-vacation-place4");
    var newPlaceInput5 = document.querySelector("#new-vacation-place5");
    var newPlaceInput6 = document.querySelector("#new-vacation-place6");
    createPlaceOnServer(newPlaceInput1.value, newPlaceInput2.value, newPlaceInput3.value, newPlaceInput4.value, newPlaceInput5.value, newPlaceInput6.value);
    
};


var changeButton = document.querySelector("#vacation-place1");

changeButton.onclick = function () {
    var newPlaceInput1 = document.querySelector("#new-vacation-place1");
    var newPlaceInput2 = document.querySelector("#new-vacation-place2");
    var newPlaceInput3 = document.querySelector("#new-vacation-place3");
    var newPlaceInput4 = document.querySelector("#new-vacation-place4");
    var newPlaceInput5 = document.querySelector("#new-vacation-place5");
    var newPlaceInput6 = document.querySelector("#new-vacation-place6");
    updatePlaceOnServer(newPlaceInput1.value, newPlaceInput2.value, newPlaceInput3.value, newPlaceInput4.value, newPlaceInput5.value, newPlaceInput6.value);
    addButton.style.display = "block";
    changeButton.style.display = "none";
};

function boxes(city, state, country, activity, language, climate ){
    document.getElementById("new-vacation-place1").value = city;
    document.getElementById("new-vacation-place2").value = state;
    document.getElementById("new-vacation-place3").value = country;
    document.getElementById("new-vacation-place4").value = activity;
    document.getElementById("new-vacation-place5").value = language;
    document.getElementById("new-vacation-place6").value = climate;
}




var registerButton = document.querySelector("#register-user");

registerButton.onclick = function () {
     
    var newName = document.querySelector("#new-name");
    var newLast = document.querySelector("#new-last");
    var newEmail = document.querySelector("#new-email");
    var newPassword = document.querySelector("#new-password");
    createUserOnServer(newName.value, newLast.value, newEmail.value, newPassword.value);
    
};



var authenticateButton = document.querySelector("#authenticate-user");

authenticateButton.onclick = function () {
    var Email = document.querySelector("#email");
    var Password = document.querySelector("#password");
    authenticateUserOnServer(Email.value, Password.value);
    
};
 
var upButton = document.querySelector("#sign-up");
upButton.onclick = function () {
    authentication.style.display = "none";
    registration.style.display = "block";
};

var inButton = document.querySelector("#sign-in");
inButton.onclick = function () {
    registration.style.display = "none";
    authentication.style.display = "block";
};


function createUserOnServer(userName, userLast, userEmail, userPassword){
    var data = "name=" + encodeURIComponent(userName) + "&last=" + encodeURIComponent(userLast) + "&email=" + encodeURIComponent(userEmail) + "&password=" + encodeURIComponent(userPassword);
    registration.style.display = "none";
    authentication.style.display = "block";

    fetch("https://my-vacaciones-app.herokuapp.com/users", {
        method: "POST",
        credentials: "include",
        body: data,
        headers: {
            //headers go here
            "Content-Type": "application/x-www-form-urlencoded"
        } 
    }).then(function (response){
        if(response.status == 201){
            
            alert("Success!")
        }else if (response.status == 422){
            alert("User already exists!")
        }
    });
}

/*added*/

function authenticateUserOnServer(userEmail, userPassword){
    var data = "email=" + encodeURIComponent(userEmail) + "&password=" + encodeURIComponent(userPassword);


    fetch("https://my-vacaciones-app.herokuapp.com/sessions", {
        method: "POST",
        credentials: "include",
        body: data,
        headers: {
            //headers go here
            "Content-Type": "application/x-www-form-urlencoded"
        } 
    }).then(function(response){
        if(response.status == 201){
            alert("Authentication from user " + userEmail + " was a success!")
            loadPlacesFromServer()
        }else if(response.status == 404){
            alert("User " + userEmail + "not in records")
        }else if(response.status == 422){
            alert("Wrong password")
        }
    });
}

function updatePlaceOnServer(placeCity, placeState, placeCountry, placeActivity, placeLanguage, placeClimate){
    var data = "city=" + encodeURIComponent(placeCity) + "&state=" + encodeURIComponent(placeState) + "&country=" + encodeURIComponent(placeCountry) + "&activity=" + encodeURIComponent(placeActivity) + "&language=" + encodeURIComponent(placeLanguage) + "&climate=" + encodeURIComponent(placeClimate);
    fetch("https://my-vacaciones-app.herokuapp.com/places/" + current_id, {
        method: "PUT",
        credentials: "include",
        body: data,
        headers: {
            //headers go here
            "Content-Type": "application/x-www-form-urlencoded"
        }
}).then(function (response){
    loadPlacesFromServer();
});
}




function createPlaceOnServer(placeCity, placeState, placeCountry, placeActivity, placeLanguage, placeClimate){
    var data = "city=" + encodeURIComponent(placeCity) + "&state=" + encodeURIComponent(placeState) + "&country=" + encodeURIComponent(placeCountry) + "&activity=" + encodeURIComponent(placeActivity) + "&language=" + encodeURIComponent(placeLanguage) + "&climate=" + encodeURIComponent(placeClimate);


    fetch("https://my-vacaciones-app.herokuapp.com/places", {
        //request options go here
        //method, header(s), body
        method: "POST",
        credentials: "include",
        body: data,
        headers: {
            //headers go here
            "Content-Type": "application/x-www-form-urlencoded"
        } 
    }).then(function (response) {
        //response code goes here
        loadPlacesFromServer();
    });
}

/*
function createPlaceOnServer(placeName){
    var data = "city=" + encodeURIComponent(placeName);


    fetch("http://localhost:8080/places", {
        //request options go here
        //method, header(s), body
        method: "POST",
        body: data,
        headers: {
            //headers go here
            "Content-Type": "application/x-www-form-urlencoded"
        } 
    }).then(function (response) {
        //response code goes here
        loadPlacesFromServer();
    });
}
*/

function deletePlaceOnServer(placeId){
    fetch("https://my-vacaciones-app.herokuapp.com/places/" + placeId, {
        method: "DELETE",
        credentials: "include",
}).then(function (response){
    loadPlacesFromServer();
});
}

function loadPlacesFromServer(){
    fetch("https://my-vacaciones-app.herokuapp.com/places", {
        credentials: "include",
    }).then(function (response) {
        //added in class
        if (response.status == 401){
            resource.style.display = "none";
            inout.style.display = "block";
            return;
        }else if (response.status == 200) {
            inout.style.display = "none";
            resource.style.display = "block";
        }


    response.json().then(function (dataFromServer){
        vacationPlaces = dataFromServer;
        var vacationPlacesList = document.querySelector("#vacation-places-list");
        vacationPlacesList.innerHTML = "";

        //Python: for place in vacationPlaces
        vacationPlaces.forEach(function (place) {
            
            //code will execute one per item in the list
                       
            //inserts data into a new DOM element
            var vacationPlaceItem = document.createElement("li");
            //vacationPlaceItem.innerHTML = place["city"] + " " + place["state"];
            
           
            //vacationPlacesList.appendChild(vacationPlaceItem);
            var cityDiv = document.createElement("div");
            cityDiv.innerHTML = place.city;
            cityDiv.classList.add("place-city");
            vacationPlaceItem.appendChild(cityDiv);

            var stateDiv = document.createElement("div");
            stateDiv.innerHTML = place.state;
            stateDiv.classList.add("place-state");
            vacationPlaceItem.appendChild(stateDiv);

            var countryDiv = document.createElement("div");
            countryDiv.innerHTML = place.country;
            countryDiv.classList.add("place-country");
            vacationPlaceItem.appendChild(countryDiv);

            var activityDiv = document.createElement("div");
            activityDiv.innerHTML = place.activity;
            activityDiv.classList.add("place-activity");
            vacationPlaceItem.appendChild(activityDiv);

            var languageDiv = document.createElement("div");
            languageDiv.innerHTML = place.language;
            languageDiv.classList.add("place-state");
            vacationPlaceItem.appendChild(languageDiv);

            var climateDiv = document.createElement("div");
            climateDiv.innerHTML = place.climate;
            climateDiv.classList.add("place-climate");
            vacationPlaceItem.appendChild(climateDiv);
            
            var deleteButton = document.createElement("button");
            deleteButton.innerHTML = "Delete This Place";
            deleteButton.onclick = function () {
                console.log("please delete this", stateDiv);
                //call new function deleteRestaurantFromServer
                //pass place.id to this function for context
                if(confirm("Are you sure you want to delete this?")){
                    deletePlaceOnServer(place.id)
                }
                
            };

            changeButton.style.display = "none";

            var updateButton = document.createElement("button");
            updateButton.innerHTML = "Update This Place";
            updateButton.onclick = function () {
                console.log("please update this", stateDiv);
                //call new function deleteRestaurantFromServer
                //pass place.id to this function for context
                if(confirm("Are you sure you want to update this?")){
                    addButton.style.display = "none";
                    changeButton.style.display = "block";
                    boxes(place.city, place.state, place.country, place.activity, place.language, place.climate);
                    current_id = place.id
                }
                
            };
            vacationPlaceItem.appendChild(deleteButton);
            
            vacationPlaceItem.appendChild(updateButton);

            vacationPlacesList.appendChild(vacationPlaceItem);
        });

    });
});
}

loadPlacesFromServer();
