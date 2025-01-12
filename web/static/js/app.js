import { main } from "./utility.js"

main(() => {
    const uploadBtn = document.getElementById("files")
    uploadBtn.addEventListener("change", async (e) => {
        const url = "http://localhost:8080/upload-photo"
        const formData = new FormData()
        formData.append("image", document.getElementById("files").files[0])
        console.log(document.getElementById("files").files[0])
        
        const addButton = document.getElementById("add-button")
        
        addButton.classList.add("expanded")
        addButton.innerText = "Done"
        
        let req = await fetch(url, {
          method: "POST",
          body: formData
        })

        req = await req.json()
        console.log("REQ:")
        console.log(req)
        
        if (!req?.length) {
            req = [req]
        }

        const prescriptionBg = document.getElementById("new-prescriptions-bg")
        prescriptionBg.classList.remove("hidden")
        const header = prescriptionBg.getElementsByClassName("prescriptions-head-container")[0]
        const formElements = Array.from(prescriptionBg.getElementsByClassName("prescriptions-form"))[0]
        let counter = 0

        
        const onButtonPress = (event) => {
            event.preventDefault()
            update()
        }

        const update = () => {
            const med = req[counter]
            header.innerHTML = "Add " + med.Name
            formElements[0].value = med.Name
            formElements[1].value = med.Strength
            formElements[2].value = med.StartDate.substr(0, 4) + '-' + med.StartDate.substr(4, 2) + '-' + med.StartDate.substr(6, 2)
            console.log(med.StartDate.substr(0, 4) + '-' + med.StartDate.substr(4, 2) + '-' + med.StartDate.substr(6, 2))
            formElements[3].value = med.Directions
            formElements[4].value = med.Hour
            formElements[5].value = med.Interval
            formElements[6].value = med.Quantity
            formElements[7].value = med.Refills
            formElements[8].value = med.EndDate.substr(0, 4) + '-' + med.EndDate.substr(4, 2) + '-' + med.EndDate.substr(6, 2)
            formElements[9].value = med.Warnings

            if (counter >= req.length - 1) {
                addButton.removeEventListener("click", onButtonPress)
                prescriptionBg.classList.add("hidden")
                addButton.classList.remove("expanded")
                addButton.innerText = "+"
                return
            }
            counter += 1
        }

        update()

        if(counter < req.length) {
            addButton.addEventListener("click", onButtonPress)
        }



        
    })

    const prescriptionButtons = document.getElementsByClassName("prescriptions-container")
    for (const btn of prescriptionButtons) {
        btn.addEventListener("click", () => {
            if(btn.classList.contains("expanded")) {
                btn.classList.remove("expanded")
            }
            else {
                btn.classList.add("expanded")
            }
        })
    }
})
