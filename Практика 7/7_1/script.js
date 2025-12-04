// Основные переменные
let originalImageData = null;
let receivedImageData = null;
let simulationId = null;
let statsData = [];

// Элементы DOM
const originalCanvas = document.getElementById('originalCanvas');
const receivedCanvas = document.getElementById('receivedCanvas');
const origCtx = originalCanvas.getContext('2d');
const recvCtx = receivedCanvas.getContext('2d');
const simulateBtn = document.getElementById('simulateBtn');
const resetBtn = document.getElementById('resetBtn');

// Инициализация
init();

function init() {
    // Загружаем тестовое изображение
    const img = new Image();
    img.crossOrigin = "Anonymous";
    img.src = 'https://upload.wikimedia.org/wikipedia/commons/thumb/6/6a/JavaScript-logo.png/240px-JavaScript-logo.png'; // Замените на свое изображение
    img.onload = function() {
        // Устанавливаем размеры canvas
        originalCanvas.width = receivedCanvas.width = img.width;
        originalCanvas.height = receivedCanvas.height = img.height;
        
        // Рисуем исходное изображение
        origCtx.drawImage(img, 0, 0);
        originalImageData = origCtx.getImageData(0, 0, img.width, img.height);
        
        // Копируем исходное изображение в полученное (пока без искажений)
        recvCtx.drawImage(img, 0, 0);
        receivedImageData = recvCtx.getImageData(0, 0, img.width, img.height);
        
        // Инициализируем график
        initChart();
    };

    // Обработчики событий для ползунков
    document.getElementById('networkSpeed').addEventListener('input', function(e) {
        document.getElementById('speedValue').textContent = e.target.value;
    });
    document.getElementById('packetLoss').addEventListener('input', function(e) {
        document.getElementById('lossValue').textContent = e.target.value;
    });
    document.getElementById('bitError').addEventListener('input', function(e) {
        document.getElementById('errorValue').textContent = e.target.value;
    });
    document.getElementById('packetSize').addEventListener('input', function(e) {
        document.getElementById('sizeValue').textContent = e.target.value;
    });

    // Обработчики кнопок
    simulateBtn.addEventListener('click', startSimulation);
    resetBtn.addEventListener('click', resetImage);
}

// Основная функция симуляции
function startSimulation() {
    if (simulationId) {
        clearTimeout(simulationId);
    }

    // Сбрасываем статистику
    statsData = [];
    updateChart();

    // Получаем параметры из UI
    const networkSpeed = parseInt(document.getElementById('networkSpeed').value);
    const packetLoss = parseInt(document.getElementById('packetLoss').value) / 100;
    const bitError = parseInt(document.getElementById('bitError').value) / 100;
    const packetSize = parseInt(document.getElementById('packetSize').value);

    // Создаем копию исходного изображения для искажений
    recvCtx.putImageData(originalImageData, 0, 0);
    receivedImageData = recvCtx.getImageData(0, 0, originalCanvas.width, originalCanvas.height);

    // Разбиваем изображение на пакеты
    const packets = createPacketsFromImageData(originalImageData, packetSize);
    let packetsToSend = [...packets];
    let receivedPackets = 0;
    let corruptedPackets = 0;
    let lostPackets = 0;

    function simulateStep() {
        let sentThisTick = 0;

        // Передаем пакеты в соответствии со скоростью сети
        while (sentThisTick < networkSpeed && packetsToSend.length > 0) {
            const packet = packetsToSend.shift();
            
            // Симулируем потерю пакета
            if (Math.random() < packetLoss) {
                lostPackets++;
                // Пакет потерян, не добавляем его в полученные данные
            } else {
                // Симулируем битовые ошибки
                const corruptedPacket = corruptPacket(packet, bitError);
                if (corruptedPacket.corrupted) {
                    corruptedPackets++;
                }
                
                // Восстанавливаем пакет в изображении
                applyPacketToImageData(receivedImageData, corruptedPacket.data, packet.index);
                receivedPackets++;
            }
            
            sentThisTick++;
        }

        // Обновляем статистику
        const totalPackets = packets.length;
        const progress = (totalPackets - packetsToSend.length) / totalPackets * 100;
        
        statsData.push({
            progress: progress,
            received: receivedPackets,
            corrupted: corruptedPackets,
            lost: lostPackets,
            efficiency: (receivedPackets / (receivedPackets + lostPackets)) * 100 || 0
        });

        // Обновляем UI
        recvCtx.putImageData(receivedImageData, 0, 0);
        updateChart();

        // Продолжаем симуляцию, если есть пакеты для отправки
        if (packetsToSend.length > 0) {
            simulationId = setTimeout(simulateStep, 100);
        } else {
            // Симуляция завершена
            console.log("Симуляция завершена");
            console.log(`Статистика: Получено: ${receivedPackets}, Искажено: ${corruptedPackets}, Потеряно: ${lostPackets}`);
        }
    }

    // Запускаем симуляцию
    simulateStep();
}

// Вспомогательные функции

function createPacketsFromImageData(imageData, packetSize) {
    const packets = [];
    const data = imageData.data;
    const totalBytes = data.length;
    
    for (let i = 0; i < totalBytes; i += packetSize) {
        const packetData = new Uint8ClampedArray(data.slice(i, i + packetSize));
        packets.push({
            index: i,
            data: packetData,
            size: packetSize
        });
    }
    
    return packets;
}

function corruptPacket(packet, bitErrorRate) {
    let corrupted = false;
    const corruptedData = new Uint8ClampedArray(packet.data);
    
    for (let i = 0; i < corruptedData.length; i++) {
        // Для каждого байта проверяем каждый бит
        for (let bit = 0; bit < 8; bit++) {
            if (Math.random() < bitErrorRate) {
                corrupted = true;
                // Инвертируем бит
                corruptedData[i] ^= (1 << bit);
            }
        }
    }
    
    return {
        data: corruptedData,
        corrupted: corrupted
    };
}

function applyPacketToImageData(imageData, packetData, startIndex) {
    for (let i = 0; i < packetData.length && (startIndex + i) < imageData.data.length; i++) {
        imageData.data[startIndex + i] = packetData[i];
    }
}

function resetImage() {
    if (simulationId) {
        clearTimeout(simulationId);
        simulationId = null;
    }
    
    recvCtx.putImageData(originalImageData, 0, 0);
    receivedImageData = recvCtx.getImageData(0, 0, originalCanvas.width, originalCanvas.height);
    statsData = [];
    updateChart();
}

// График с использованием D3.js
function initChart() {
    const margin = {top: 20, right: 30, bottom: 40, left: 50};
    const width = document.getElementById('chart').clientWidth - margin.left - margin.right;
    const height = 400 - margin.top - margin.bottom;

    const svg = d3.select("#chart")
        .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", `translate(${margin.left},${margin.top})`);

    // Создаем шкалы
    const xScale = d3.scaleLinear().range([0, width]);
    const yScale = d3.scaleLinear().range([height, 0]);

    // Создаем оси
    const xAxis = d3.axisBottom(xScale);
    const yAxis = d3.axisLeft(yScale);

    // Добавляем оси
    svg.append("g")
        .attr("class", "x-axis")
        .attr("transform", `translate(0,${height})`);
    
    svg.append("g")
        .attr("class", "y-axis");

    // Создаем линии для графиков
    const efficiencyLine = d3.line()
        .x(d => xScale(d.progress))
        .y(d => yScale(d.efficiency));

    const packetsLine = d3.line()
        .x(d => xScale(d.progress))
        .y(d => yScale(d.received));

    // Добавляем пути для графиков
    svg.append("path")
        .attr("class", "efficiency-line")
        .style("stroke", "steelblue")
        .style("fill", "none");

    svg.append("path")
        .attr("class", "packets-line")
        .style("stroke", "green")
        .style("fill", "none");

    // Добавляем легенду
    const legend = svg.append("g")
        .attr("transform", `translate(${width - 150}, 20)`);

    legend.append("rect")
        .attr("x", 0)
        .attr("y", 0)
        .attr("width", 12)
        .attr("height", 12)
        .style("fill", "steelblue");

    legend.append("text")
        .attr("x", 20)
        .attr("y", 10)
        .text("Эффективность (%)")
        .style("font-size", "12px");

    legend.append("rect")
        .attr("x", 0)
        .attr("y", 20)
        .attr("width", 12)
        .attr("height", 12)
        .style("fill", "green");

    legend.append("text")
        .attr("x", 20)
        .attr("y", 30)
        .text("Полученные пакеты")
        .style("font-size", "12px");
}

function updateChart() {
    if (statsData.length === 0) return;

    const margin = {top: 20, right: 30, bottom: 40, left: 50};
    const width = document.getElementById('chart').clientWidth - margin.left - margin.right;
    const height = 400 - margin.top - margin.bottom;

    const svg = d3.select("#chart svg g");

    // Обновляем шкалы
    const xScale = d3.scaleLinear()
        .domain([0, 100])
        .range([0, width]);

    const yScale = d3.scaleLinear()
        .domain([0, d3.max(statsData, d => Math.max(d.efficiency, d.received))])
        .range([height, 0]);

    // Обновляем оси
    svg.select(".x-axis")
        .call(d3.axisBottom(xScale).tickFormat(d => d + "%"));

    svg.select(".y-axis")
        .call(d3.axisLeft(yScale));

    // Обновляем линии графиков
    const efficiencyLine = d3.line()
        .x(d => xScale(d.progress))
        .y(d => yScale(d.efficiency));

    const packetsLine = d3.line()
        .x(d => xScale(d.progress))
        .y(d => yScale(d.received));

    svg.select(".efficiency-line")
        .datum(statsData)
        .attr("d", efficiencyLine);

    svg.select(".packets-line")
        .datum(statsData)
        .attr("d", packetsLine);
}