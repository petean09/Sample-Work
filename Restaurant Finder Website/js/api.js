/* jshint esversion: 6 */
/* jshint node: true */
"use strict";


async function getData(url, key="") {
    let myHeaders = new Headers();
    myHeaders.append("Authorization", key);
    return fetch(`https://cors-anywhere.herokuapp.com/${url}`, {
        headers: myHeaders 
    })
        .then(response => response.json())
        .catch(error => console.log(error));
}

function buildRestaurantDictionary(restaurantInfoById, restaurantReviewsbyId){
    let restaurants = []
    for (let idx = 0; idx < restaurantInfoById.length; idx++){
        let dict = {}
        dict['name'] = restaurantInfoById[idx].name;
        dict['image'] = restaurantInfoById[idx].image_url;
        dict['phone'] = restaurantInfoById[idx].display_phone;
        dict['review_count'] = restaurantInfoById[idx].review_count;
        dict['rating'] = restaurantInfoById[idx].rating;
        dict['latitude'] = restaurantInfoById[idx].coordinates.latitude;
        dict['longitude'] = restaurantInfoById[idx].coordinates.longitude;
        dict['price'] = restaurantInfoById[idx].price;
        if ('hours' in restaurantInfoById[idx]){
            let allHours = restaurantInfoById[idx].hours[0].open;
            let dayDictionary = {0:'Monday', 1:'Tuesday', 2:'Wednesday', 3:'Thursday', 4:'Friday', 5:'Saturday', 6:'Sunday'};
            let hoursList =[];
            for(let item of allHours){
                let startHours = parseInt(item['start'].slice(0,2));
                let sPM = false;
                if(startHours > 12){
                    startHours -= 12;
                    sPM = true;
                }
                let startTime = startHours.toString() + ":" + item['start'].slice(2,);
                if (sPM){
                    startTime += "PM";
                }else{
                    startTime += "AM";
                }
                let endHours = parseInt(item['end'].slice(0,2));
                let ePM = false;
                if(endHours > 12){
                    endHours -= 12;
                    ePM = true;
                }else if (endHours == 0){
                    endHours = 12;
                }
                let endTime = endHours.toString() + ":" + item['end'].slice(2,);
                if (ePM){
                    endTime += "PM";
                }else{
                    endTime += "AM";
                }
                let hours = startTime + "-" + endTime;
                hoursList.push(dayDictionary[item['day']]+": "+ hours);
            }
            dict['hours'] = hoursList;
        }else {
            dict['hours'] = 'Not Available';
        }
        dict['address'] = restaurantInfoById[idx].location.display_address;
        
        let all = restaurantInfoById[idx].categories[0].title;
        let num = 0;
        while(num + 1 < restaurantInfoById[idx].categories.length){
            all += ", " + restaurantInfoById[idx].categories[num+1].title;
            num+=1;
        }
        dict['cuisines'] = all;

        let reviews = [];
        let currAllReviews = restaurantReviewsbyId[idx];
        for (let idx = 0; idx < currAllReviews.reviews.length; idx++){
            let reviewdict = {}
            reviewdict["userName"] = currAllReviews.reviews[idx].user.name;
            reviewdict["userImage"] = currAllReviews.reviews[idx].user.image_url;
            reviewdict["rating"] = currAllReviews.reviews[idx].rating;
            reviewdict["time"] = currAllReviews.reviews[idx].time_created;
            reviewdict['review'] = currAllReviews.reviews[idx].text;
            reviewdict['reviewURL'] = currAllReviews.reviews[idx].url;
            reviews.push(reviewdict);
        }
        dict['reviews'] = reviews;
        restaurants.push(dict);
    }
    return restaurants;
}

async function getAllInfo(name) {
    let yelpKey = 'Bearer _56-0naRyZhDKMFZwJBMCyjnZlVtf7s7_jMU2uiInJH0ZMmQm965Eo8LP8oC2aC-PHTm2gkwVP8uZanmDIpKUOtjBLkiZzLriIPyakMUxA9c-6Qc5dPTNsGNEo6_W3Yx';
    let allResInfo = [];
    let allRevInfo = [];
    
    let [allInformation]= await Promise.all([
        getData(`https://api.yelp.com/v3/businesses/search?limit=5&term=restaurants&location=${name}&sort_by=rating`, yelpKey)
    ]);
    console.log(allInformation)

    let ids = []
    for(let idx = 0; idx < allInformation.businesses.length; idx ++){
        let id = allInformation.businesses[idx].id;
        ids.push(id);
    }

    let infoURLS = [];
    let reviewsURLS =[];
    for (let idx = 0; idx < ids.length; idx++){
        let id = ids[idx];
        infoURLS.push(`https://api.yelp.com/v3/businesses/${id}`);
        reviewsURLS.push(`https://api.yelp.com/v3/businesses/${id}/reviews`);
    }

    const infoPromises = infoURLS.map(async url => {
        const response = await getData(url, yelpKey);
        return response;
    })

    for (const infoPromise of infoPromises) {
        allResInfo.push(await infoPromise);
    }

    const reviewPromises = reviewsURLS.map(async url => {
        const response = await getData(url, yelpKey);
        return response;
    })

    for (const reviewPromise of reviewPromises) {
        allRevInfo.push(await reviewPromise);
    }

    populate(allResInfo,allRevInfo, allInformation);
}

function populate(resInfo, revInfo, allInfo){
    let restaurants = buildRestaurantDictionary(resInfo, revInfo);

    let cityLatitute = allInfo.region.center.latitude;
    let cityLongitude = allInfo.region.center.longitude;

    populateRestaurantInformation(restaurants);
    initMap(cityLatitute, cityLongitude, restaurants);
    weatherAlert(cityLatitute, cityLongitude);
}
 
function initMap(cityLat, cityLong, restaurants) {
    // creates the map and zooms in on the city coordinates
    var mapProp= {
        center:new google.maps.LatLng(cityLat,cityLong),
    };
    var map=new google.maps.Map(document.getElementById("googleMap"),mapProp);

    var bounds = new google.maps.LatLngBounds();

    for (let locationIdx in restaurants) {
        var newLat = (restaurants[locationIdx].latitude);
        var newLong = (restaurants[locationIdx].longitude);
    
        let newLocation = {lat: parseFloat(newLat), lng: parseFloat(newLong)}

        let restaurantName = restaurants[locationIdx].name;
        var infowindow = new google.maps.InfoWindow({
            content: restaurantName
        });

        var marker = new google.maps.Marker({
            position: newLocation,
            map: map,
            info: restaurantName
        });

        bounds.extend(marker.position);

        google.maps.event.addListener(marker, 'click', function() {
            infowindow.setContent( this.info );
            infowindow.open( map, this );
            map.setCenter(marker.getPosition());
        });

    }
    map.fitBounds(bounds);

}

function populateRestaurantInformation(res){
    let rDiv = document.querySelector("#restaurants");
    rDiv.classList.add("container2", 'mt-3');
    rDiv.innerHTML ="";
    
    for(let idx in res){
        idx = parseInt(idx);
        let resDiv = document.createElement("div");
        resDiv.classList.add('row2', 'border', 'border-dark', 'rounded');
    
        let numDiv = document.createElement('div');
        numDiv.classList.add('col', 'h2');
        numDiv.innerHTML = `#${idx + 1}`
        resDiv.appendChild(numDiv);
        

        let nameDiv = document.createElement('div')
        nameDiv.classList.add('col', 'h4')
        nameDiv.id = res[idx].name
        nameDiv.innerHTML = `<b>${res[idx].name}</b>`
        resDiv.appendChild(nameDiv);


        let addressDiv = document.createElement('div')
        addressDiv.classList.add('col')
        for(let addressIdx=0; addressIdx < res[idx].address.length; addressIdx++){
            addressDiv.innerHTML += res[idx].address[addressIdx] + "<br />";
        }
        resDiv.appendChild(addressDiv);

        let lineDiv = document.createElement('div');
        lineDiv.classList.add('col','line');
        resDiv.appendChild(lineDiv);

        let phoneDiv = document.createElement('div');
        phoneDiv.classList.add('col');
        phoneDiv.innerHTML = `<b>Phone:</b> `;
        if (res[idx].phone != "") {
            phoneDiv.innerHTML += res[idx].phone;
        }else {
            phoneDiv.innerHTML += "Not Available";
        }
        resDiv.appendChild(phoneDiv);

        let cuisineDiv = document.createElement('div');
        cuisineDiv.classList.add('col');
        cuisineDiv.innerHTML = `<b>Cuisine:</b> `;
        if (res[idx].cuisines != ""){
            cuisineDiv.innerHTML += res[idx].cuisines; 
        }else {
            cuisineDiv.innerHTML += "Not Available";
        }
        resDiv.appendChild(cuisineDiv);


        let priceDiv = document.createElement('div');
        priceDiv.classList.add('col');
        priceDiv.innerHTML = `<b>Price:</b> `;
        if (res[idx].price != ""){
            priceDiv.innerHTML += res[idx].price; 
        }else {
            priceDiv.innerHTML += "Not Available";
        }
        resDiv.appendChild(priceDiv);

        let ratingDiv = document.createElement('div');
        ratingDiv.classList.add('col'); 
        ratingDiv.innerHTML = `<b>Rating:</b> ${res[idx].rating}`;
        resDiv.appendChild(ratingDiv);

        let reviewCountDiv = document.createElement('div');
        reviewCountDiv.classList.add('col'); 
        reviewCountDiv.innerHTML = `<b>Number of Reviews:</b> ${res[idx].review_count}`;
        resDiv.appendChild(reviewCountDiv);
        
        let hoursDiv = document.createElement('div');
        hoursDiv.classList.add('col');
        hoursDiv.innerHTML += '<b>Hours:</b><br/>';
        if (res[idx].hours == "Not Available"){
            hoursDiv.innerHTML += `&nbsp;&nbsp;${res[idx].hours}`;
        }else {
            for (let day of res[idx].hours){
                hoursDiv.innerHTML += `&nbsp;&nbsp;${day}<br/>`;
            }
        }
        resDiv.appendChild(hoursDiv);
        resDiv.innerHTML += "<br>";

        let revButtonDiv = document.createElement('div');
        revButtonDiv.classList.add('col', 'text-center');
        let reviewButton = document.createElement('button');
        reviewButton.type="button";
        reviewButton.innerHTML = "Click for Reviews";
        reviewButton.classList.add('btn', 'btn-outline-primary');
        reviewButton.setAttribute('onclick', "getReviews("+JSON.stringify(res[idx])+"," + idx + ")");
        revButtonDiv.appendChild(reviewButton);
        resDiv.appendChild(revButtonDiv);
        
        resDiv.innerHTML += "<br>";

        rDiv.appendChild(resDiv);
    }
    let loadingAlert = document.getElementById('loading');
    loadingAlert.parentNode.removeChild(loadingAlert);
}

function getReviews(resReviews,num){
    let reviews = document.querySelector("#reviews");
    reviews.innerHTML = "";
    reviews.classList.add('container', 'border', 'border-dark', 'rounded', 'mt-3', 'mb-3');
    let name = document.createElement('div');
    name.classList.add('row', 'col', 'mt-3', 'mb-3');
    name.innerHTML = `<h3><b>#${num+1}: ${resReviews.name}</b></h3>`;
    reviews.appendChild(name);

    for(let review of resReviews.reviews) {
        let reviewDiv = document.createElement('div');
        reviewDiv.classList.add('mb-2', 'row');

        let imageDiv = document.createElement('div');
        imageDiv.classList.add('col-sm-auto');
        if (review.userImage != null) {
            imageDiv.innerHTML = `<img src="${review.userImage}" alt="UserPicture" style="width:100px;height:100px;">`;
        }else {
            imageDiv.innerHTML = `<img src="../images/user_large_square.png" alt="UserPicture" style="width:100px;height:100px;">`;
        }
        reviewDiv.appendChild(imageDiv);
        
        let nameTimeDiv = document.createElement('div');
        nameTimeDiv.classList.add('col', 'col-sm-3', 'mr-2');
        let nameDiv = document.createElement('div');
        nameDiv.classList.add('row');
        nameDiv.innerHTML = `<h4><b>${review.userName}</b></h4>`;
        let timeDiv = document.createElement('div');
        timeDiv.classList.add('row');
        let date = review.time.slice(0,10).split('-');
        let time = review.time.slice(11).split(':');
        let monthDict = {1:'January', 2:'February', 3:'March', 4:"April", 5:"May", 6:"June", 7:"July", 8:"August", 9:"September", 10:"October", 11:"November", 12:'December'}

        timeDiv.innerHTML = `${monthDict[parseInt(date[1])]} ${parseInt(date[2])}, ${date[0]}<br>`;
        let hour = parseInt(time[0]);
        let timeOfDay = 'AM';
        if(hour > 12){
            hour = hour - 12;
            timeOfDay = 'PM';
        }else if (hour == 0){
            hour = 12;
        }
        let min = time[1];
        timeDiv.innerHTML += `${hour}:${min} ${timeOfDay}`;
        nameTimeDiv.appendChild(nameDiv);
        nameTimeDiv.appendChild(timeDiv);
        reviewDiv.appendChild(nameTimeDiv);

        let ratingReviewDiv = document.createElement('div');
        ratingReviewDiv.classList.add('col');
        let ratingDiv = document.createElement('div');
        ratingDiv.classList.add('row');
        ratingDiv.innerHTML = `<b>Rating: </b> ${review.rating}`;
        let reviewTextDiv = document.createElement('div');
        reviewTextDiv.classList.add('row');
        if (review.review.slice(-3)=="..."){
            reviewTextDiv.innerHTML = `<p><b>Comments:</b> ${review.review} <a href="${review.reviewURL}" target="_blank">Read More!</a></p>`;
        }else{
            reviewTextDiv.innerHTML = `<p><b>Comments:</b> ${review.review}</p>`;
        }
        

        ratingReviewDiv.appendChild(ratingDiv);
        ratingReviewDiv.appendChild(reviewTextDiv);
        reviewDiv.appendChild(ratingReviewDiv);
   
        reviews.appendChild(reviewDiv);
    }
    document.getElementById('bottom').scrollIntoView();
}

async function weatherAlert(lat, lng) {
    let [weatherData]= await Promise.all([
        getData(`https://api.openweathermap.org/data/2.5/weather?lat=${lat}&lon=${lng}&units=imperial&APPID=c6232c094ccdcb5dd1e333b7f88b35e0`)
    ]);
    let alertDiv = document.getElementById('weatherAlert');
    alertDiv.innerHTML = "";
    alertDiv.classList.add('alert', 'alert-info', 'mb-0', 'mt-3');

    let temp = weatherData.main.temp;
    let cloudPercent = weatherData.clouds.all + '%';
    let name = weatherData.name;

    let weather = "The weather is currently: " + weatherData.weather[0].description;
    let idx = 0;
    let ids = [];
    ids.push(weatherData.weather[idx].id);
    while(idx + 1 < weatherData.weather.length){
        weather += ", " + weatherData.weather[idx+1].description;
        ids.push(weatherData.weather[idx+1].id);
        idx+=1;
    }

    let reminds = new Set()
    for (let id of ids){
        if(id >= 200 && id < 300){
            reminds.add("It's a thunderstorm, maybe stay inside?");
        }else if((id >= 300 && id < 400) || id == 701){
            reminds.add("Drizzle outside, bring a jacket.");
        }else if(id >= 500 && id < 600){
            reminds.add("Raining now. You may want an umbrella.");
        }else if(id >= 600 && id < 700){
            reminds.add("It's snowing! Bring those warm coats!");
        }else if(id == 741){
            reminds.add("Foggy, drive safe.");
        }else if(id == 762 || id == 781){
            reminds.add("Crazy stuff outside, may want to reschedule dinner...");
        }else if(id== 800) {
            reminds.add("Nothing happening, have a great meal!");
        }else if (id > 800){
            reminds.add("Might be a little cloudy");
        }
    }

    alertDiv.innerHTML = `The temperature in ${name} is ${temp}&#8457;.  The cloud cover is at ${cloudPercent}.  `;
    alertDiv.innerHTML += `${weather} <br/> Here are your reminders: <br/>`;
    for (let remind of reminds){
        alertDiv.innerHTML+= `&nbsp;&nbsp;&nbsp;&nbsp;&#8226;${remind}<br/>`;
    }
}


function loadInfo(cityName){
    let info = document.querySelector('#mainPage');
    let map = document.createElement('div');
    map.id="googleMap";
    map.style.height = "400px";
    map.style.margin= "20px";

    let restaurant = document.createElement('div');
    restaurant.id="restaurants";

    let reviews = document.createElement('div');
    reviews.id="reviews";

    info.appendChild(map);
    info.appendChild(restaurant);
    info.appendChild(reviews);

   getAllInfo(cityName);
}

function validateInput(input) {
    let isValid = false;
    if (isNaN(parseInt(input))){
        let stateCodeList = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA", 
                             "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", 
                             "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", 
                             "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", 
                             "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"];
        let stateNameList =  ["Alabama","Alaska","Arizona","Arkansas","California","Colorado",
                              "Connecticut","Delaware","Florida","Georgia","Hawaii","Idaho","Illinois",
                              "Indiana","Iowa","Kansas","Kentucky","Louisiana","Maine","Maryland",
                              "Massachusetts","Michigan","Minnesota","Mississippi","Missouri","Montana",
                              "Nebraska","Nevada","New Hampshire","New Jersey","New Mexico","New York",
                              "North Carolina","North Dakota","Ohio","Oklahoma","Oregon","Pennsylvania",
                              "Rhode Island","South Carolina","South Dakota","Tennessee","Texas","Utah",
                              "Vermont","Virginia","Washington","West Virginia","Wisconsin","Wyoming"];
        let inputList = input.split(",");
        if (inputList[1] == undefined){
            return isValid
        }
        let state = (inputList[1]).trim();
        if (stateCodeList.includes(state) | stateNameList.includes(state)){
            isValid = true;
            return isValid
        }
    }else {
        isValid = /^\d{5}(-\d{4})?$/.test(input);
        return isValid
    }
}

function clickedOn(){
    let cityName = document.querySelector('#locationInput').value;
    if (validateInput(cityName)){
        window.localStorage.setItem('cityName', JSON.stringify(cityName));
        window.location.href = "/static/results.html";
    }else{
        let alert = document.getElementById('alert');
        alert.innerHTML="";
        alert.classList.add("alert", "alert-danger");
        alert.innerHTML="Enter a City/State Pair or a 5-Digit Zip Code";
    }
}

$(document).ready(function () {
    let place = localStorage.getItem('cityName');
    loadInfo(place);
});