from flask import Flask, render_template, request, jsonify
import json
from datetime import datetime
from simulation import F1Car2026, simulate_race

app = Flask(__name__)

# Store race results in memory
race_results = {}

class F1Car2026:
    """F1 2026 Car Simulation Class"""
    
    # 2026 F1 Regulation Constants
    BATTERY_CAPACITY = 14  # kWh
    FUEL_CAPACITY = 50  # kg
    ENERGY_RECOVERY_BRAKING = 0.65  # 65%
    OVERTAKE_MODE_ENERGY = 50  # kJ
    MAX_OVERTAKE_USES = 6
    ICE_FUEL_CONSUMPTION = 0.14  # kg/km
    
    def __init__(self, driver_name, team, qualifying_position=1):
        """Initialize F1 car with 2026 specifications"""
        self.driver_name = driver_name
        self.team = team
        self.qualifying_position = qualifying_position
        
        # Energy systems
        self.battery_soc = 100.0  # State of Charge (0-100%)
        self.fuel_remaining = self.FUEL_CAPACITY
        self.tire_degradation = 0.0
        self.power_output = 600  # kW
        
        # Race tracking
        self.lap_number = 0
        self.overtake_uses_remaining = self.MAX_OVERTAKE_USES
        self.overtake_active = False
        self.overtake_timer = 0.0
        self.pit_stops = 0
        
        # Event logging
        self.events = []
        self.race_data = {
            'laps': [],
            'batteries': [100.0],
            'fuels': [self.FUEL_CAPACITY],
            'tires': [0.0],
            'powers': [600],
            'pit_stops': []
        }
    
    def brake_event(self, speed_reduction):
        """
        Simulate braking and energy recovery
        Args: speed_reduction (float) - speed reduced in km/h
        Returns: energy_recovered (float) - energy recovered in kJ
        """
        # Kinetic energy calculation: E = 0.5 * m * v^2
        # Simplified for racing car: base energy per km/h reduction
        energy_recoverable = (speed_reduction / 100) * 200
        
        # Apply recovery efficiency (65%)
        energy_recovered = energy_recoverable * self.ENERGY_RECOVERY_BRAKING
        
        # Convert kJ to battery percentage (14 kWh = 50400 kJ)
        battery_gain = (energy_recovered / 3600) * 1000 * 0.15
        
        # Add to battery (max 100%)
        self.battery_soc = min(100, self.battery_soc + battery_gain)
        
        return energy_recovered
    
    def deploy_energy(self, deployment_percentage):
        """
        Deploy battery energy for power boost
        Args: deployment_percentage (float) - % of battery to deploy (0-100)
        Returns: power_delivered (float) - power in kW
        """
        # Calculate available energy
        available_energy = (self.battery_soc / 100) * self.BATTERY_CAPACITY
        
        # Calculate energy to deploy
        energy_to_deploy = (deployment_percentage / 100) * available_energy
        
        # Convert to power (kW)
        power_delivered = (energy_to_deploy * 3600 / 5) / 1000
        
        # Reduce battery
        self.battery_soc -= (energy_to_deploy / self.BATTERY_CAPACITY) * 100
        self.battery_soc = max(0, self.battery_soc)
        
        return power_delivered
    
    def activate_overtake_mode(self):
        """
        Activate overtake mode (if available)
        Returns: bool - Success or failure
        """
        # Check if uses remaining
        if self.overtake_uses_remaining <= 0:
            self.events.append(f"LAP {self.lap_number}: ❌ No overtake uses remaining!")
            return False
        
        # Check if enough energy
        energy_available = (self.battery_soc / 100) * self.BATTERY_CAPACITY
        energy_needed = self.OVERTAKE_MODE_ENERGY / 3600
        
        if energy_available < energy_needed:
            self.events.append(f"LAP {self.lap_number}: ❌ Not enough battery for overtake!")
            return False
        
        # Activate overtake
        self.overtake_active = True
        self.overtake_timer = 20.0  # 20 seconds
        self.overtake_uses_remaining -= 1
        
        # Consume energy
        self.battery_soc -= (energy_needed / self.BATTERY_CAPACITY) * 100
        
        self.events.append(f"LAP {self.lap_number}: 🚀 OVERTAKE ACTIVATED! ({self.overtake_uses_remaining} uses left)")
        return True
    
    def simulate_lap(self, track_conditions='normal'):
        """
        Simulate one complete racing lap
        Args: track_conditions (str) - 'normal', 'wet', 'hot'
        Returns: dict - lap data
        """
        self.lap_number += 1
        
        # BRAKING ZONES (3 per lap)
        braking_values = [80, 90, 100]  # speed reductions
        total_energy_recovered = 0
        
        for brake_val in braking_values:
            recovered = self.brake_event(brake_val)
            total_energy_recovered += recovered
        
        # ACCELERATION & ENERGY DEPLOYMENT
        if not self.overtake_active:
            deployment = 60  # Deploy 60% normally
        else:
            deployment = 80  # Deploy 80% in overtake
            self.overtake_timer -= 20  # Overtake lasts 20 seconds
            if self.overtake_timer <= 0:
                self.overtake_active = False
        
        power = self.deploy_energy(deployment)
        
        # FUEL CONSUMPTION
        fuel_consumed = self.ICE_FUEL_CONSUMPTION
        
        # Tire wear modifier (worse tires = more fuel)
        tire_wear_factor = 1 + (self.tire_degradation / 100) * 1
        fuel_consumed *= tire_wear_factor
        
        # Overtake penalty (+30% fuel)
        if self.overtake_active:
            fuel_consumed *= 1.3
        
        self.fuel_remaining -= fuel_consumed
        self.fuel_remaining = max(0, self.fuel_remaining)
        
        # TIRE DEGRADATION
        self.tire_degradation += 1.5
        self.tire_degradation = min(100, self.tire_degradation)
        
        # PIT STOP CHECK
        pit_stop_happened = False
        if self.lap_number in [5, 12]:
            pit_stop_happened = self.pit_stop()
        
        # STORE DATA
        self.race_data['laps'].append(self.lap_number)
        self.race_data['batteries'].append(round(self.battery_soc, 1))
        self.race_data['fuels'].append(round(self.fuel_remaining, 2))
        self.race_data['tires'].append(round(self.tire_degradation, 1))
        self.race_data['powers'].append(round(power, 0))
        
        # LOG EVENT
        if not pit_stop_happened:
            self.events.append(
                f"LAP {self.lap_number}: Battery {self.battery_soc:.1f}% | "
                f"Fuel {self.fuel_remaining:.2f}kg | "
                f"Tires {self.tire_degradation:.1f}% | "
                f"Power {power:.0f}kW"
            )
        
        return {
            'lap': self.lap_number,
            'battery': self.battery_soc,
            'fuel': self.fuel_remaining,
            'tires': self.tire_degradation,
            'power': power,
            'pit_stop': pit_stop_happened
        }
    
    def pit_stop(self):
        """
        Execute pit stop: refuel, recharge battery, replace tires
        Returns: bool - pit stop executed
        """
        self.pit_stops += 1
        
        # Add fuel
        self.fuel_remaining = min(self.FUEL_CAPACITY, self.fuel_remaining + 15)
        
        # Recharge battery
        self.battery_soc = min(100, self.battery_soc + 5)
        
        # Replace tires
        self.tire_degradation = 0
        
        self.events.append(
            f"LAP {self.lap_number}: 🏁 PIT STOP #{self.pit_stops} | "
            f"Fuel +15kg | Battery +5% | Tires RESET"
        )
        
        self.race_data['pit_stops'].append({
            'lap': self.lap_number,
            'fuel_added': 15,
            'battery_added': 5,
            'duration': 21.0
        })
        
        return True
    
    def get_performance_score(self):
        """Calculate performance score (0-100)"""
        battery_score = (100 - abs(50 - self.battery_soc)) / 2
        fuel_score = (self.fuel_remaining / self.FUEL_CAPACITY) * 25
        tire_score = (100 - self.tire_degradation) / 4
        overall = (battery_score + fuel_score + tire_score) / 3
        return round(overall, 1)


@app.route('/')
def index():
    """Serve the main HTML page"""
    return render_template('index.html')


@app.route('/api/simulate', methods=['POST'])
def api_simulate():
    """
    API endpoint to run simulation
    POST data: {
        'driver1': str,
        'team1': str,
        'driver2': str,
        'team2': str,
        'laps': int,
        'conditions': str
    }
    """
    try:
        data = request.json
        
        # Extract parameters
        driver1_name = data.get('driver1', 'Max Verstappen')
        team1 = data.get('team1', 'Red Bull')
        driver2_name = data.get('driver2', 'Lewis Hamilton')
        team2 = data.get('team2', 'Ferrari')
        num_laps = int(data.get('laps', 20))
        conditions = data.get('conditions', 'normal')
        
        # Create cars
        driver1 = F1Car2026(driver1_name, team1, 1)
        driver2 = F1Car2026(driver2_name, team2, 2)
        
        # Run simulation
        for lap in range(num_laps):
            driver1.simulate_lap(conditions)
            driver2.simulate_lap(conditions)
        
        # Prepare response
        result = {
            'status': 'success',
            'timestamp': datetime.now().isoformat(),
            'drivers': [
                {
                    'name': driver1_name,
                    'team': team1,
                    'laps_completed': driver1.lap_number,
                    'final_battery': round(driver1.battery_soc, 1),
                    'final_fuel': round(driver1.fuel_remaining, 2),
                    'final_tires': round(driver1.tire_degradation, 1),
                    'pit_stops': driver1.pit_stops,
                    'performance_score': driver1.get_performance_score(),
                    'race_data': driver1.race_data,
                    'events': driver1.events
                },
                {
                    'name': driver2_name,
                    'team': team2,
                    'laps_completed': driver2.lap_number,
                    'final_battery': round(driver2.battery_soc, 1),
                    'final_fuel': round(driver2.fuel_remaining, 2),
                    'final_tires': round(driver2.tire_degradation, 1),
                    'pit_stops': driver2.pit_stops,
                    'performance_score': driver2.get_performance_score(),
                    'race_data': driver2.race_data,
                    'events': driver2.events
                }
            ]
        }
        
        # Store result
        race_id = f"race_{datetime.now().timestamp()}"
        race_results[race_id] = result
        result['race_id'] = race_id
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400


@app.route('/api/races', methods=['GET'])
def get_races():
    """Get all past race results"""
    return jsonify({
        'status': 'success',
        'races': list(race_results.keys()),
        'count': len(race_results)
    }), 200


@app.route('/api/race/<race_id>', methods=['GET'])
def get_race(race_id):
    """Get specific race result"""
    if race_id in race_results:
        return jsonify({
            'status': 'success',
            'data': race_results[race_id]
        }), 200
    else:
        return jsonify({
            'status': 'error',
            'message': 'Race not found'
        }), 404


@app.route('/api/specs', methods=['GET'])
def get_specs():
    """Get F1 2026 specifications"""
    return jsonify({
        'status': 'success',
        'specs': {
            'battery_capacity': '14 kWh',
            'fuel_capacity': '50 kg',
            'braking_recovery': '65%',
            'overtake_power_boost': '+50 kW',
            'overtake_duration': '20 seconds',
            'overtake_uses_per_race': '6',
            'fuel_consumption_base': '0.14 kg/km',
            'tire_degradation_per_lap': '1.5%',
            'race_distance': '56 laps (~305 km)',
            'pit_stop_duration': '21-22 seconds'
        }
    }), 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)