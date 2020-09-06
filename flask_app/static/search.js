
const loading = document.getElementById('loading')
const mainDiv = document.getElementById('main-div')
loading.style.display = 'none'
var currentLoadRequest = null;
var currentWaitRequest = null;

var waiting_for_update = false;
var successfullyLoaded = false


$(document).ready(function () {
    $('body').bootstrapMaterialDesign()
})

function wait_for_update() {
    /**
     * Creates a GET requests to route '/updated' and waits for response
     * upon which calls load_data()
     */
    console.log('waiting ....');
    if (!waiting_for_update) {
        waiting_for_update = true;
        currentWaitRequest = $.ajax({
            url: '/updated',
            beforeSend: function () {
                if (currentWaitRequest != null) {
                    currentWaitRequest.abort();
                }
            },
            success: function () {
                successfullyLoaded = true;
                load_data();
            },
            complete: function () {
                if (!successfullyLoaded) {
                    waiting_for_update = false;
                    wait_for_update();
                }
            },

        });
    }
}

function load_data() {
    /**
     * Creates a GET request to route '/data' and receives latest results
     * if the request is sucessful the window is assigned location '/dashboard'
     */
    console.log('loading ....');
    var url = '/data'
    currentLoadRequest = $.ajax({
        url: url,
        beforeSend: function () {
            if (currentLoadRequest != null) {
                currentLoadRequest.abort();
            }
        },
        success: function (data) {
            window.location.assign('/dashboard')
        },
        error: function () {
            console.error('error loading data');
        }
    });
    return true;
}

document.addEventListener('DOMContentLoaded', () => {

    getFormFields()
    submitForm()

    const navLinks = document.querySelectorAll('.nav-link')

    navLinks.forEach(node => {
        $('.active #keyword-form').replaceWith($('.active #keyword-form').clone());
        node.addEventListener('mouseout', () => {
            $('.active #query-form').replaceWith($('.active #query-form').clone());
            getFormFields()
            submitForm()
        })
    })
})



function submitForm() {
    /**
     * Creates a POST request to route '/' if the form passes validation then displays the loading screen
     */
    document.getElementsByClassName('active')[1].childNodes.forEach(node => {
        if (node.nodeName === 'FORM') {

            node.addEventListener('submit', (event) => {
                event.preventDefault()

                let form = getFormValues()
                if (form) {
                    if (form.location) {
                        let boundingBox = []
                        let promises = []
                        if (typeof form.location === 'object') {
                            for (let i = 0; i < form.location.length; i++) {
                                promises.push(validateLocation(form.location[i]))
                            }
                        } else {
                            promises.push(validateLocation(form.location))
                        }

                        Promise.all(promises)
                            .then(result => {
                                for (let i = 0; i < result.length; i++) {
                                    const r = result[i];
                                    r.forEach(coordinate => {
                                        boundingBox.push(coordinate)
                                    })
                                }
                                console.log(boundingBox);
                                form.location = boundingBox

                                loading.style.display = ''
                                mainDiv.style.display = 'none'
                                var minutes = 60 - 2, display = document.querySelector('#refresh-display');
                                startTimer(minutes, display);

                                console.log(form);
                                let jsonForm = JSON.stringify(form)

                                $.ajax({
                                    type: "POST",
                                    url: '/',
                                    data: jsonForm,
                                    contentType: "application/json; charset=utf-8",
                                    success: function (response) {
                                        console.log(response)
                                    }
                                });
                                console.log('form submitted');

                                wait_for_update();

                            })
                            .catch(err => {
                                alert(form.location + ' is not valid, please choose another location!')
                                console.log('One of the locations was invalid... ', err)
                            })
                    } else {

                        loading.style.display = ''
                        mainDiv.style.display = 'none'
                        if (form.windowSize) {
                            var seconds = (form.windowSize * 60) - 2, display = document.querySelector('#refresh-display');
                            startTimer(seconds, display);
                        } else {
                            var seconds = 60 - 2, display = document.querySelector('#refresh-display');
                            startTimer(seconds, display);
                        }

                        let jsonForm = JSON.stringify(form)

                        $.ajax({
                            type: "POST",
                            url: '/',
                            data: jsonForm,
                            contentType: "application/json; charset=utf-8",
                            success: function (response) {
                                console.log(response)
                            }
                        });
                        console.log('form submitted');

                        wait_for_update();

                    }
                }
            })
        }
    });
}



function getFormFields() {

    /**
     * Initializes query form variables from the currently active tab
     */

    const keywordQueryField = $(".active #keyword-query-field")[0]
    const languageQueryField = $(".active #language-query-field")[0]
    const locationQueryField = $(".active #location-query-field")[0]
    const keywordField = $(".active #keyword-field")[0]
    const keywordCheckbox = $(".active #keyword-checkbox")[0]
    const locationField = $(".active #location-field")[0]
    const locationCheckbox = $(".active #location-checkbox")[0]
    const languageField = $(".active #language-field")[0]
    const languageCheckbox = $(".active #language-checkbox")[0]
    $('.active #add-keyword-button').replaceWith($('.active #add-keyword-button').clone());
    const keywordFieldAdder = $(".active #add-keyword-button")[0]
    $('.active #add-language-button').replaceWith($('.active #add-language-button').clone());
    const languageFieldAdder = $(".active #add-language-button")[0]
    $('.active #add-location-button').replaceWith($('.active #add-location-button').clone());
    const locationFieldAdder = $(".active #add-location-button")[0]

    const actionSwtichKeyword = $(".active #actions-switch-keyword")[0]
    const actionSwtichLocation = $(".active #actions-switch-location")[0]
    const actionSwtichLanguage = $(".active #actions-switch-language")[0]
    const actionSwtichAdvanced = $(".active #actions-switch-advanced")[0]
    $('.active #togglable').replaceWith($('.active #togglable').clone());
    const actionScaleOptions = $(".active #togglable")[0]


    if (actionSwtichKeyword) {
        actionSwtichKeyword.addEventListener('change', () => {
            checkOptions(actionSwtichKeyword)
        })
    }

    if (actionSwtichLocation) {
        actionSwtichLocation.addEventListener('change', () => {
            checkOptions(actionSwtichLocation)
        })
    }

    if (actionSwtichLanguage) {
        actionSwtichLanguage.addEventListener('change', () => {
            checkOptions(actionSwtichLanguage)
        })
    }

    if (actionSwtichAdvanced) {
        actionSwtichAdvanced.addEventListener('change', () => {
            checkOptions(actionSwtichAdvanced)
        })
    }


    if (keywordFieldAdder) {
        keywordFieldAdder.addEventListener('click', () => {
            addInput('Keyword', keywordQueryField, 'keyword-field')
        })
    }


    if (languageFieldAdder) {
        languageFieldAdder.addEventListener('click', () => {
            addInput('Language', languageQueryField, 'language-field')
        })
    }

    if (locationFieldAdder) {
        locationFieldAdder.addEventListener('click', () => {
            addInput('Location', locationQueryField, 'location-field')
        })
    }

    if (keywordCheckbox &&
        locationCheckbox &&
        languageCheckbox) {
        keywordCheckbox.addEventListener("change", () => {
            toggleInput({ target: keywordCheckbox }, keywordField, keywordFieldAdder, $("#keyword-required-indicator")[0]);
        })

        locationCheckbox.addEventListener("change", () => {
            toggleInput({ target: locationCheckbox }, locationField, locationFieldAdder, $("#location-required-indicator")[0])
        })

        languageCheckbox.addEventListener("change", () => {
            toggleInput({ target: languageCheckbox }, languageField, languageFieldAdder, $("#language-required-indicator")[0])
        })
    }

    function checkOptions(checkbox) {
        let button = $('.active #radio1')
        let area = $('.active .form-control.pad')

        if (checkbox.checked) {
            actionScaleOptions.style.display = 'block'
            button.attr("required", true)
            if (area.length) {
                for (let i = 0; i < area.length; i++) {
                    const element = area[i];
                    element.required = true
                }
            }
        } else {
            actionScaleOptions.style.display = 'none'
            button.attr("required", false)
            if (area.length) {
                for (let i = 0; i < area.length; i++) {
                    const element = area[i];
                    element.required = false
                }
            }
        }
    }

}

function toggleInput(e, field, button, requiredIndicator) {
    field.disabled = !e.target.checked
    button.disabled = !e.target.checked
    if (requiredIndicator.style.display === 'none') {
        requiredIndicator.style.display = ''
    } else {
        requiredIndicator.style.display = 'none'
    }
}

function addInput(placeholder, parent, id) {
    if (placeholder === "Language") {
        let node = $('.active #language-field').clone()
        node[0].required = false
        parent.appendChild(node[0])
    } else if (placeholder === "Location") {
        let node = $('.active #location-field').clone()
        node[0].required = false
        parent.appendChild(node[0])
    } else {
        let node = document.createElement('input')
        node.setAttribute('type', 'text')
        node.setAttribute('class', 'form-control')
        node.setAttribute('id', id)
        node.setAttribute('placeholder', placeholder)
        parent.appendChild(node)
    }

}

function validate(form) {

    /**
     * Checks if the query form is filled correctly and input is valid
     */
    let valid = true

    if (!form.keyword && !form.location) {
        valid = false
        $(".active #keyword-field").addClass("is-invalid")
        $(".active #location-field").addClass("is-invalid")
        document.getElementById('has-spaces').style.display = 'none'
        alert("Both location and keyword fields cannot be empty. You must fill either the keyword field or the location field.")
    }


    let keywords = $(".active #keyword-field")
    for (let i = 0; i < $(".active #keyword-field").length; i++) {
        if ($(".active #keyword-field")[i].value.length != $(".active #keyword-field")[i].value.replace(" ", "").length) {
            valid = false
            $(".active #keyword-field").addClass("is-invalid")
            document.getElementById('keyword-invalid').style.display = 'none'
        }
    }
    return valid
}

async function validateLocation(location) {
    /**
     * If a location is provided as a query parameter, checks if it corresponds to an actual location on the map
     * by making a request to openstreetmap
     */
    const url = 'https://nominatim.openstreetmap.org/search?format=json&q='
    location.replace(" ", "+")
    let response = await fetch(url + location)
    let json = await response.json()
    return json[0].boundingbox
}


function getFormValues() {
    /**
     * Gets the query form values when the submit button i clicked
     */
    let form = {
        keyword: $(".active #keyword-field")[0] ? $(".active #keyword-field")[0].value : null,
        location: $(".active #location-field")[0] ? $(".active #location-field")[0].value : null,
        language: $(".active #language-checkbox")[0] ? $(".active #language-field")[0].value : null,
        numOfInfluencers: $(".active #top-k")[0].value,
        minFollowers: $(".active #min-followers")[0].value,
        maxFollowers: $(".active #max-followers")[0].value,
        windowSize: $(".active #window-size")[0] ? $(".active #window-size")[0].value : null,
        updateInterval: $(".active #update-interval")[0] ? $(".active #update-interval")[0].value : null,
        actionWeights: null,
        actionScale: null,
        verified: false
    }



    if ($(".active .action-switch")[0]) {
        if ($(".active .action-switch")[0].checked) {
            let actionScale = {
                tweet: $(".active input[name='tweetRadioOptions']:checked").val(),
                retweet: $(".active input[name='retweetRadioOptions']:checked").val(),
                quoteRetweet: $(".active input[name='qretweetRadioOptions']:checked").val(),
                reply: $(".active input[name='replyRadioOptions']:checked").val()
            }
            form['actionScale'] = actionScale
        }
    }

    if ($(".active .action-weight-switch")[0]) {
        if ($(".active .action-weight-switch")[0].checked) {
            let actionWeights = {
                tweet: $(".active #tweet-weight")[0] ? $(".active #tweet-weight")[0].value : "1",
                retweet: $(".active #retweet-weight")[0] ? $(".active #retweet-weight")[0].value : "1",
                quoteRetweet: $(".active #qretweet-weight")[0] ? $(".active #qretweet-weight")[0].value : "1",
                reply: $(".active #reply-weight")[0] ? $(".active #reply-weight")[0].value : "1"
            }
            form['actionWeights'] = actionWeights
        }
    }

    if ($(".active .verified-switch")[0].checked) {
        form['verified'] = true
    }

    if ($(".active #keyword-field").length > 1) {
        if ($(".active #keyword-checkbox")[0]) {
            if ($(".active #keyword-checkbox")[0].checked) {
                form['keyword'] = []
                for (let i = 0; i < $(".active #keyword-field").length; i++) {
                    const element = $(".active #keyword-field")[i];
                    form['keyword'].push(element.value)
                }
            } else {
                form['keyword'] = null
            }
        } else {
            form['keyword'] = []
            for (let i = 0; i < $(".active #keyword-field").length; i++) {
                const element = $(".active #keyword-field")[i];
                form['keyword'].push(element.value)
            }
        }
    }

    if ($(".active #location-field").length > 1) {
        if ($(".active #location-checkbox")[0]) {
            if ($(".active #location-checkbox")[0].checked) {
                form['location'] = []
                for (let i = 0; i < $(".active #location-field").length; i++) {
                    const element = $(".active #location-field")[i];
                    form['location'].push(element.value)
                }
            } else {
                form['location'] = null
            }
        } else {
            form['location'] = []
            for (let i = 0; i < $(".active #location-field").length; i++) {
                const element = $(".active #location-field")[i];
                form['location'].push(element.value)
            }
        }
    }

    if ($(".active #language-field").length > 1) {
        if ($(".active #language-checkbox")[0]) {
            if ($(".active #language-checkbox")[0].checked) {
                form['language'] = []
                for (let i = 0; i < $(".active #language-field").length; i++) {
                    const element = $(".active #language-field")[i];
                    form['language'].push(element.value)
                }
            } else {
                form['language'] = null
            }
        } else {
            form['language'] = []
            for (let i = 0; i < $(".active #language-field").length; i++) {
                const element = $(".active #language-field")[i];
                form['language'].push(element.value)
            }
        }
    }

    if (validate(form)) {
        return form
    }
}

function startTimer(duration, display) {
    var timer = duration, minutes, seconds;
    var x = setInterval(() => {
        minutes = parseInt(timer / 60, 10);
        seconds = parseInt(timer % 60, 10);

        minutes = minutes < 10 ? "0" + minutes : minutes;
        seconds = seconds < 10 ? "0" + seconds : seconds;


        display.textContent = minutes + ":" + seconds;

        if (--timer < 0) {
            timer = duration;
            clearInterval(x)
        }
    }, 1000);
}
