let uploadedPath = null;

async function uploadVideo() {
    const file = document.getElementById("videoInput").files[0];
    const formData = new FormData();
    formData.append("video", file);

    const res = await fetch("/upload", {
        method: "POST",
        body: formData
    });

    const data = await res.json();
    uploadedPath = data.path;

    alert("Uploaded!");
}

async function postVideo() {
    const checkboxes = document.querySelectorAll("input[type=checkbox]:checked");
    const platforms = Array.from(checkboxes).map(cb => cb.value);

    const res = await fetch("/post", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            platforms: platforms,
            video_path: uploadedPath
        })
    });

    const data = await res.json();
    document.getElementById("result").innerText = JSON.stringify(data, null, 2);
}