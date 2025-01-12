import { main } from "./utility.js"

main(() => {
    const uploadBtn = document.getElementById("files")
    uploadBtn.addEventListener("click", async (e) => {
        const url = "http://localhost:8080/upload-photo"
        const formData = new FormData()
        formData.append("image", document.getElementById("avatar").files[0])
        console.log(document.getElementById("avatar").files[0])

        const req = await fetch(url, {
          method: "POST",
          body: formData
        })

        console.log(req)
    })
})
