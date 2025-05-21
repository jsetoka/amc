function createuser() {
  const nom = document.getElementById("nom").value;
  const email = document.getElementById("email").value;
  console.log("JOB ETOKAS");
  fetch("http://localhost:8000/momoapi/createuser/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ nom: nom, email: email }),
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error("Erreur HTTP : " + response.status);
      }
      return response.json();
    })
    .then((data) => {
      document.getElementById("reponse").innerText = data.message;
    })
    .catch((error) => {
      document.getElementById("reponse").innerText =
        "Erreur : " + error.message;
    });
}
