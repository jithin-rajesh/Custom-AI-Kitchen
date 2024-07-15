const URL = "https://teachablemachine.withgoogle.com/models/8hJsh2CJ5/";
let model, webcam, labelContainer, maxPredictions;

async function init() {
    const modelURL = URL + "model.json";
    const metadataURL = URL + "metadata.json";
    model = await tmImage.load(modelURL, metadataURL);
    maxPredictions = model.getTotalClasses();

    const flip = true;
    webcam = new tmImage.Webcam(200, 200, flip);
    await webcam.setup();
    await webcam.play();
    window.requestAnimationFrame(loop);

    document.getElementById("webcam-container-ui").appendChild(webcam.canvas);
    labelContainer = document.getElementById("label-container-ui");
    for (let i = 0; i < maxPredictions; i++) {
        labelContainer.appendChild(document.createElement("div"));
    }
}

async function loop() {
    webcam.update();
    await predict();
    window.requestAnimationFrame(loop);
}

async function predict() {
    const prediction = await model.predict(webcam.canvas);
    labelContainer.innerHTML = '';
    for (let i = 0; i < maxPredictions; i++) {
        const probability = prediction[i].probability.toFixed(2);
        if (probability > 0.7) {
            const classPrediction = prediction[i].className + ": " + probability;
            const predictionElement = document.createElement("div");
            predictionElement.innerHTML = classPrediction;
            labelContainer.appendChild(predictionElement);
        }
    }
}
