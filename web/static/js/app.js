import { main } from "./utility.js"

main(() => {
    const uploadBtn = document.getElementById("files")
    uploadBtn.addEventListener("change", async (e) => {
        const url = "http://localhost:8080/upload-photo"
        const formData = new FormData()
        formData.append("image", document.getElementById("files").files[0])
        console.log(document.getElementById("files").files[0])

        let req = await fetch(url, {
          method: "POST",
          body: formData
        })

        req = await req.json()
        console.log(req)

        const prescriptionBg = Array.from(document.getElementById("new-prescription-bg").getElementsByClassName("prescriptions-form"))[0]
        prescriptionBg[0].value = req.Name
        prescriptionBg[1].value = req.Strength
        prescriptionBg[2].value = req.StartDate.substr(0, 4) + '-' + req.StartDate.substr(4, 2) + '-' + req.StartDate.substr(6, 2)
        console.log(req.StartDate.substr(0, 4) + '-' + req.StartDate.substr(4, 2) + '-' + req.StartDate.substr(6, 2))
        prescriptionBg[3].value = req.Directions
        prescriptionBg[4].value = req.Hour
        prescriptionBg[5].value = req.Interval
        prescriptionBg[6].value = req.Quantity
        prescriptionBg[7].value = req.Refills
        prescriptionBg[8].value = req.EndDate.substr(0, 4) + '-' + req.EndDate.substr(4, 2) + '-' + req.EndDate.substr(6, 2)
        prescriptionBg[9].value = req.Warnings
    })
})
