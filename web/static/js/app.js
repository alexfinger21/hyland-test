import { main } from "./utility.js"

main(() => {
    const uploadBtn = document.getElementById("files")
    uploadBtn.addEventListener("click", async (e) => {
        const url = "http://localhost:8080/upload-photo"
        const formData = new FormData()
        formData.append("image", document.getElementById("files").files[0])
        console.log(document.getElementById("files").files[0])

        const req = await fetch(url, {
          method: "POST",
          body: formData
        })

        console.log(req)
        for (const x of req) {
            console.log(req)
        }
    })
})
