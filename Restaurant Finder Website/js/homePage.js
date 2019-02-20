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