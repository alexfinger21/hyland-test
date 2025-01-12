import { main } from "./utility.js"


function getNextMedicationDay(startDate, interval) {
    const startDateObj = new Date(
        parseInt(startDate.substring(0, 4)), 
        parseInt(startDate.substring(4, 6)) - 1, // Month (0-indexed)
        parseInt(startDate.substring(6, 8))
    );

    // Get today's date (set time to midnight for comparison)
    const today = new Date();
    today.setHours(0, 0, 0, 0);

    // Calculate the next occurrence
    let nextDate = startDateObj;
    while (nextDate <= today) {
        nextDate.setDate(nextDate.getDate() + interval);
    }

    return nextDate.toLocaleDateString('en-US', { weekday: 'long' });
}


const createPrescription = (med, link) => {
    const element = document.createElement("template")
    element.innerHTML = `<button class="prescriptions-container">
                <div class="prescriptions-horizontal-container">
                    <div class="prescriptions-head-container">
                        <p class="prescriptions-header">${med.Name}: ${getNextMedicationDay(med.StartDate, med.Interval)}</p>
                        <p class="prescriptions-description">Click To Expand</p>
                    </div>
                    <div class="remove-button">
                        <img alt="remove prescription" src="media/remove.png"/>
                    </div>
                </div>
                <form class="prescriptions-form">
                    <div class="prescriptions-row">
                        <div>
                            <label for="endDate">End Date:</label><br>
                            <input type="date" id="fquantity" name="fquantity" value="${med.EndDate}"><br>
                        </div>
                        <div>
                            <label for="startDate">Start Date:</label><br>
                            <input type="date" id="fstartDate" name="fstartDate" value="${med.StartDate}"><br>
                        </div>
                    </div>
                    <div class="prescriptions-row">
                        <div>
                            <label for="strength">Strength:</label><br>
                            <input type="text" id="fstrength" name="strength" value="${med.Strength}"><br>
                        </div>
                        <div>
                            <label for="directions">Directions:</label><br>
                            <input type="text" id="fdirections" name="directions" value="${med.Directions}"><br>
                        </div>
                    </div>
                    <div class="prescriptions-row">
                        <div>
                            <label for="hour">Hour:</label><br>
                            <input type="text" id="fHour" name="fHour" value="${med.Hour}"><br>
                        </div>
                        <div>
                            <label for="interval">Interval:</label><br>
                            <input type="text" id="finterval" name="interval" value="${med.Interval}"><br>
                        </div>
                    </div>
                    <div class="prescriptions-row">
                        <div>
                            <label for="quantity">Quantity:</label><br>
                            <input type="text" id="fquantity" name="fquantity" value="${med.Quantity}"><br>
                        </div>
                        <div>
                            <label for="refills">Refills:</label><br>
                            <input type="text" id="frefills" name="refills" value="${med.Refills}"><br>
                        </div>
                    </div>
                    <p>${med.Warnings}</p>
                </form>
                <a class="prescriptions-action">Add to Google Calendar</a>
            </button>`

    const btn = element.content.firstChild
    const headContainer = btn.getElementsByClassName("prescriptions-head-container")[0]
    btn.addEventListener("click", () => {
        if(btn.classList.contains("expanded")) {
            btn.classList.remove("expanded")
            btn.style.maxHeight = headContainer.clientHeight + 10 + "px"
        }
        else {
            btn.classList.add("expanded")
            btn.style.maxHeight = "1000px"
        }
    })

    return btn
    
}

main(() => {
    const uploadBtn = document.getElementById("files")
    const addButton = document.getElementById("add-button")
    const scroller = document.getElementById("scroller")

    const localS = JSON.parse(localStorage.getItem("previousPrescriptions"))

    if (localS) { 
        for (let i = 0; i<localS.length; ++i) {
            console.log(localS[i])
            const btn = createPrescription(localS[i])
            const nm = localS[i].Name
            btn.style.zIndex = i
            scroller.appendChild(btn)
            const rmd = btn.getElementsByClassName("prescriptions-horizontal-container")[0].getElementsByClassName("remove-button")[0]
            rmd.addEventListener("click", (e) => {
                btn.remove()
                const ls = JSON.parse(localStorage.getItem("previousPrescriptions")).filter(l => l.Name != nm)
                localStorage.setItem("previousPrescriptions", JSON.stringify(ls))
            })
        }
    }

    addButton.addEventListener("touchstart", ()=> {
        console.log('touch start')
        addButton.classList.add("pressed")
    })
    addButton.addEventListener("touchend", ()=> {
        console.log('touch end')
        addButton.classList.remove("pressed")
    })

    uploadBtn.addEventListener("change", async (e) => {
        const url = "/upload-photo"
        const formData = new FormData()
        formData.append("image", document.getElementById("files").files[0])
        console.log(document.getElementById("files").files[0])
        
        
        addButton.classList.add("expanded")
        addButton.innerText = "Done"
        
        let req = await fetch(url, {
          method: "POST",
          body: formData
        })

        req = await req.json()
        console.log("REQ:")
        console.log(req)

        if (req.error) {
            addButton.classList.remove("expanded")
            addButton.innerText = "+"

            console.log("err")
            return
        }
        
        if (!req?.length) {
            req = [req]
        }


        const prescriptionBg = document.getElementById("new-prescriptions-bg")
        const calendarLink = Array.from(prescriptionBg.getElementsByClassName("prescriptions-action"))[0]
        prescriptionBg.classList.remove("hidden")
        const scroller = document.getElementById("scroller")
        const header = prescriptionBg.getElementsByClassName("prescriptions-head-container")[0]
        const formElements = Array.from(prescriptionBg.getElementsByClassName("prescriptions-form"))[0]
        const warningText = prescriptionBg.getElementsByClassName("prescriptions-warnings")[0]
        const title = prescriptionBg.getElementsByClassName("prescriptions-head-container")[0].innerHTML.substring(4)
        let counter = 0 

        
        const onButtonPress = (event) => {
            event.preventDefault()
            update()
        }

        const  saveLocalStorage = async (elemVals, warningText, title, counter) => {
            let request;
            const rqBody = {
                "EndDate": elemVals[0].replace(/-/g, ''),
                "StartDate": elemVals[1].replace(/-/g, ''),
                "Strength": elemVals[2],
                "Directions": elemVals[3],
                "Hour": elemVals[4],
                "Interval": elemVals[5],
                "Quantity": elemVals[6],
                "Refills": elemVals[7],
                "Warnings": warningText,
                "Name": title,
            }

            if (elemVals[0] && elemVals[0].length != 0) {
                request = await fetch("/create-event", {
                    method: "POST",
                    body: JSON.stringify(rqBody)
                })
            }

            const calUrl =  await request.text()
            console.log("COUNTER", req, counter)
            const med = req[counter]  
            console.log(med)
            med.EndDate = med.EndDate.substr(0, 4) + '-' + med.EndDate.substr(4, 2) + '-' + med.EndDate.substr(6, 2)
            med.StartDate = med.StartDate.substr(0, 4) + '-' + med.StartDate.substr(4, 2) + '-' + med.StartDate.substr(6, 2)
            const btn = createPrescription(med)
            btn.style.zIndex = scroller.children.length+1
            scroller.appendChild(btn)
            const headContainer = btn.getElementsByClassName("prescriptions-head-container")[0]
            btn.style.maxHeight = headContainer.clientHeight + 10 + "px"


            const saveBody = {
                "EndDate": elemVals[0].replace(/-/g, ''),
                "StartDate": elemVals[1].replace(/-/g, ''),
                "Strength": elemVals[2],
                "Directions": elemVals[3],
                "Hour": elemVals[4],
                "Interval": elemVals[5],
                "Quantity": elemVals[6],
                "Refills": elemVals[7],
                "Warnings": warningText,
                "Name": title,
                "Link": calUrl
            }

            const prevStorage = JSON.parse(localStorage.getItem("previousPrescriptions")) ? JSON.parse(localStorage.getItem("previousPrescriptions")) : []
            prevStorage.push(saveBody)
            console.log(prevStorage)
            console.log(JSON.parse(JSON.stringify(prevStorage)))

            localStorage.setItem("previousPrescriptions", JSON.stringify(prevStorage))
        }

        const update = async () => {
            if (counter != 0) {
                const elemVals = Object.values(formElements).slice(0, 10).map(m => m.value)
                saveLocalStorage(elemVals, warningText.innerText, title, counter-1)
            }

            const med = req[counter]
            header.innerHTML = "Add " + med.Name
            formElements[0].value = med.EndDate.substr(0, 4) + '-' + med.EndDate.substr(4, 2) + '-' + med.EndDate.substr(6, 2)
            console.log("DATAE", med.EndDate.substr(0, 4) + '-' + med.EndDate.substr(4, 2) + '-' + med.EndDate.substr(6, 2))
            formElements[1].value = med.StartDate.substr(0, 4) + '-' + med.StartDate.substr(4, 2) + '-' + med.StartDate.substr(6, 2)
            formElements[2].value = med.Strength
            formElements[3].value = med.Directions
            formElements[4].value = med.Hour
            formElements[5].value = med.Interval
            formElements[6].value = med.Quantity
            formElements[7].value = med.Refills
            warningText.innerText = med.Warnings


            if (counter >= req.length - 1) {
                addButton.removeEventListener("click", onButtonPress)
                const lastClick = (e) => {
                    e.preventDefault()
                    console.log("ASDJKHASKDJASHKJDS")
                    const elemVals = Object.values(formElements).slice(0, 10).map(m => m.value)
                    saveLocalStorage(elemVals, warningText.innerText, title, counter-1)
                    prescriptionBg.classList.add("hidden")
                    addButton.classList.remove("expanded")
                    addButton.innerText = "+"
                    addButton.removeEventListener("click", lastClick)
                }

                addButton.addEventListener("click", lastClick)
            }
            counter += 1
        }

        update()

        if(counter < req.length) {
            addButton.addEventListener("click", onButtonPress)
        }
    })
})
