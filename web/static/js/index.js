import { main } from "./utility.js"

main(() => {
    console.log("hello world")
    /*
    const uploadBtn = document.getElementById("avatar")
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
    */
    const appBtn = document.getElementById("app-btn")
    appBtn.addEventListener("click", async (e) => {
        window.location.replace("/app")
    })
})
