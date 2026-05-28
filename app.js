// F1 2026 Simulator - Frontend JavaScript
// This file handles all frontend logic and API calls

let charts = {};
let currentRaceData = null;

// F1 Car Class (Frontend Simulation as backup)
class F1Car {
    constructor(name, team) {
        this.name = name;
        this.team = team;
        this.battery = 100;
        this.fuel = 50;
        this.tires = 0;
        this.power = 600;
        this.lapNumber = 0;
        this.overtakeUses = 6;
        this.events = [];
        this.pitStops = 0;
        
        this.raceData = {
            batteries: [100],
            fuels: [50],
            tires: [0],
            powers: [600],
            laps: [0]
        };
    }

    simulateLap() {
        this.lapNumber++;
        
        // Braking energy recovery
        const brakingZones = [80, 90, 100];
        for (let brake of brakingZones) {
            const energyRecovered = (brake / 100) * 200 * 0.65;
            this.battery = Math.min(100, this.battery + (energyRecovered / 3600) * 0.15);
        }

        // Energy deployment
        const deployment = this.battery * (Math.random() * 0.2 + 0.5);
        this.power = 600 + (deployment / 10);

        // Fuel consumption
        let fuelConsumed = 0.14;
        fuelConsumed *= (1 + this.tires * 0.01);
        this.fuel = Math.max(0, this.fuel - fuelConsumed);

        // Battery discharge
        const batteryLoss = 0.8 + Math.random() * 0.4;
        this.battery = Math.max(0, this.battery - batteryLoss);

        // Tire degradation
        this.tires = Math.min(100, this.tires + 1.5);

        // Pit stop check
        if (this.lapNumber === 5 || this.lapNumber === 12) {
            this.pitStop();
        }

        // Store data
        this.raceData.batteries.push(parseFloat(this.battery.toFixed(1)));
        this.raceData.fuels.push(parseFloat(this.fuel.toFixed(2)));
        this.raceData.tires.push(parseFloat(this.tires.toFixed(1)));
        this.raceData.powers.push(parseFloat(this.power.toFixed(0)));
        this.raceData.laps.push(this.lapNumber);

        return {
            lap: this.lapNumber,
            battery: this.battery,
            fuel: this.fuel,
            tires: this.tires,
            power: this.power
        };
    }

    pitStop() {
        this.pitStops++;
        this.battery = Math.min(100, this.battery + 5);
        this.fuel = Math.min(50, this.fuel + 15);
        this.tires = 0;
        this.events.push(
            `LAP ${this.lapNumber}: 🏁 PIT STOP #${this.pitStops} | ` +
            `Fuel +15kg | Battery +5% | Tires RESET`
        );
    }
}

// Main simulation function
async function runSimulation() {
    console.log('🏁 Starting F1 2026 Simulation...');
    
    // Get input values
    const driver1Name = document.getElementById('driver1').value;
    const team1 = document.getElementById('team1').value;
    const driver2Name = document.getElementById('driver2').value;
    const team2 = document.getElementById('team2').value;
    const numLaps = parseInt(document.getElementById('laps').value);
    const conditions = document.getElementById('conditions').value;

    // Create cars
    const driver1 = new F1Car(driver1Name, team1);
    const driver2 = new F1Car(driver2Name, team2);

    // Clear race log
    const raceLog = document.getElementById('raceLog');
    raceLog.innerHTML = `
        <strong>${driver1Name} (${team1}) vs ${driver2Name} (${team2})</strong><br>
        <strong>Track Conditions: ${conditions.toUpperCase()}</strong><br><br>
    `;

    // Run simulation
    for (let lap = 0; lap < numLaps; lap++) {
        const d1Data = driver1.simulateLap();
        const d2Data = driver2.simulateLap();

        // Add to race log
        const entry1 = document.createElement('div');
        entry1.className = 'lap-entry';
        if (driver1.lapNumber === 5 || driver1.lapNumber === 12) {
            entry1.classList.add('pit-stop');
        }
        entry1.innerHTML = `
            <strong>${driver1Name}:</strong> 
            LAP ${d1Data.lap} | Battery ${d1Data.battery.toFixed(1)}% | 
            Fuel ${d1Data.fuel.toFixed(2)}kg | Tires ${d1Data.tires.toFixed(1)}%
        `;
        raceLog.appendChild(entry1);

        const entry2 = document.createElement('div');
        entry2.className = 'lap-entry';
        if (driver2.lapNumber === 5 || driver2.lapNumber === 12) {
            entry2.classList.add('pit-stop');
        }
        entry2.innerHTML = `
            <strong>${driver2Name}:</strong> 
            LAP ${d2Data.lap} | Battery ${d2Data.battery.toFixed(1)}% | 
            Fuel ${d2Data.fuel.toFixed(2)}kg | Tires ${d2Data.tires.toFixed(1)}%
        `;
        raceLog.appendChild(entry2);
    }

    // Update dashboard
    updateDashboard(driver1, driver2);

    // Update charts
    updateCharts(driver1, driver2, driver1Name, driver2Name);

    // Scroll to bottom
    raceLog.scrollTop = raceLog.scrollHeight;

    console.log('✅ Simulation complete!');
}

// Update dashboard metrics
function updateDashboard(driver1, driver2) {
    // Driver 1
    document.getElementById('driver1-battery').textContent = 
        `${driver1.battery.toFixed(1)}%`;
    document.getElementById('driver1-battery-bar').style.width = 
        `${driver1.battery}%`;

    document.getElementById('driver1-fuel').textContent = 
        `${driver1.fuel.toFixed(1)}kg`;
    document.getElementById('driver1-fuel-bar').style.width = 
        `${(driver1.fuel / 50) * 100}%`;

    document.getElementById('driver1-tires').textContent = 
        `${driver1.tires.toFixed(1)}%`;
    document.getElementById('driver1-tires-bar').style.width = 
        `${driver1.tires}%`;

    document.getElementById('driver1-overtake').textContent = 
        `${driver1.overtakeUses}/6`;
    document.getElementById('driver1-overtake-bar').style.width = 
        `${(driver1.overtakeUses / 6) * 100}%`;

    // Driver 2
    document.getElementById('driver2-battery').textContent = 
        `${driver2.battery.toFixed(1)}%`;
    document.getElementById('driver2-battery-bar').style.width = 
        `${driver2.battery}%`;

    document.getElementById('driver2-fuel').textContent = 
        `${driver2.fuel.toFixed(1)}kg`;
    document.getElementById('driver2-fuel-bar').style.width = 
        `${(driver2.fuel / 50) * 100}%`;

    document.getElementById('driver2-tires').textContent = 
        `${driver2.tires.toFixed(1)}%`;
    document.getElementById('driver2-tires-bar').style.width = 
        `${driver2.tires}%`;

    document.getElementById('driver2-overtake').textContent = 
        `${driver2.overtakeUses}/6`;
    document.getElementById('driver2-overtake-bar').style.width = 
        `${(driver2.overtakeUses / 6) * 100}%`;
}

// Update charts with Chart.js
function updateCharts(driver1, driver2, driver1Name, driver2Name) {
    // Battery Chart
    updateChart('batteryChart', 'Battery Status (%)', 
        driver1.raceData.laps,
        [
            {
                label: driver1Name,
                data: driver1.raceData.batteries,
                borderColor: '#ff0000',
                backgroundColor: 'rgba(255,0,0,0.1)'
            },
            {
                label: driver2Name,
                data: driver2.raceData.batteries,
                borderColor: '#0066cc',
                backgroundColor: 'rgba(0,102,204,0.1)'
            }
        ]
    );

    // Fuel Chart
    updateChart('fuelChart', 'Fuel Remaining (kg)',
        driver1.raceData.laps,
        [
            {
                label: driver1Name,
                data: driver1.raceData.fuels,
                borderColor: '#ff9800',
                backgroundColor: 'rgba(255,152,0,0.1)'
            },
            {
                label: driver2Name,
                data: driver2.raceData.fuels,
                borderColor: '#00cc00',
                backgroundColor: 'rgba(0,204,0,0.1)'
            }
        ]
    );

    // Tire Chart
    updateChart('tireChart', 'Tire Degradation (%)',
        driver1.raceData.laps,
        [
            {
                label: driver1Name,
                data: driver1.raceData.tires,
                borderColor: '#ff0000',
                backgroundColor: 'rgba(255,0,0,0.1)'
            },
            {
                label: driver2Name,
                data: driver2.raceData.tires,
                borderColor: '#0066cc',
                backgroundColor: 'rgba(0,102,204,0.1)'
            }
        ]
    );

    // Power Chart
    updateChart('powerChart', 'Power Output (kW)',
        driver1.raceData.laps,
        [
            {
                label: driver1Name,
                data: driver1.raceData.powers,
                borderColor: '#ff0000',
                backgroundColor: 'rgba(255,0,0,0.1)'
            },
            {
                label: driver2Name,
                data: driver2.raceData.powers,
                borderColor: '#0066cc',
                backgroundColor: 'rgba(0,102,204,0.1)'
            }
        ]
    );
}

// Helper function to create/update charts
function updateChart(canvasId, title, labels, datasets) {
    const ctx = document.getElementById(canvasId).getContext('2d');
    
    // Destroy old chart if exists
    if (charts[canvasId]) {
        charts[canvasId].destroy();
    }

    // Create new chart
    charts[canvasId] = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: datasets.map(ds => ({
                ...ds,
                tension: 0.3,
                borderWidth: 2,
                pointRadius: 3,
                fill: true
            }))
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: true,
                    position: 'top'
                },
                title: {
                    display: true,
                    text: title,
                    font: { size: 14 }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: title
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Lap Number'
                    }
                }
            }
        }
    });
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    console.log('🏁 F1 2026 Simulator Loaded!');
    // Run initial simulation
    runSimulation();
});

// Export data as JSON
function exportRaceData() {
    if (!currentRaceData) {
        alert('No race data available. Run a simulation first!');
        return;
    }

    const dataStr = JSON.stringify(currentRaceData, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `F1_2026_Race_${new Date().getTime()}.json`;
    link.click();
}