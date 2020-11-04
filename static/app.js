// Returns an array of cupcake objects
async function getCupcakes() {
    const resp = await axios.get("/api/cupcakes");
    return resp.data.cupcakes;
}

async function addCupcake() {
    let flavor = $("#flavor").val();
    let rating = $("#rating").val();
    let size = $("#size").val();
    let image = $("#image").val();

    const newCupcake = await axios.post('/api/cupcakes', {
        flavor,
        rating,
        size,
        image
    });

    cupcakeHTML = createHTML(newCupcake.data.cupcake);
    $("#cupcake-ul").append(cupcakeHTML);
}

async function deleteCupcake(evt) {
    console.log(evt);
    let $cupcake = $(evt.target).closest("div");
    let cupcakeId = $cupcake.attr("data-cupcake-id");

    await axios.delete(`api/cupcakes/${cupcakeId}`);
    $cupcake.remove();
}

async function init() {
    for (let cupcake of await getCupcakes()) {
        let html = createHTML(cupcake);
        $("#cupcake-ul").append(html);
    }
}

$("#cupcake-form").on("submit", async function (evt) {
    evt.preventDefault();
    await addCupcake();
});

$("#cupcake-ul").on("click", ".delete-button", async function (evt) {
    evt.preventDefault();
    await deleteCupcake(evt);
});

init();