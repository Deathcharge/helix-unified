// Helix Collective Metrics Visualization
class MetricsVisualizer {
    constructor() {
        this.charts = {};
        this.init();
    }

    init() {
        this.initializeCharts();
        this.startMetricsUpdates();
    }

    initializeCharts() {
        this.initializeLatencyChart();
        this.initializeLoadChart();
        this.initializeMemoryChart();
        this.initializeDensityChart();
    }

    initializeLatencyChart() {
        const ctx = document.getElementById('latency-chart');
        if (!ctx) return;

        this.charts.latency = new Chart(ctx, {
            type: 'line',
            data: {
                labels: this.generateTimeLabels(20),
                datasets: [{
                    label: 'Network Latency (ms)',
                    data: this.generateRandomData(20, 10, 50),
                    borderColor: '#00ffcc',
                    backgroundColor: 'rgba(0, 255, 204, 0.1)',
                    borderWidth: 2,
                    tension: 0.4,
                    fill: true
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    }
                },
                scales: {
                    x: {
                        display: true,
                        grid: {
                            color: 'rgba(255, 255, 255, 0.1)'
                        },
                        ticks: {
                            color: '#b8b8d0'
                        }
                    },
                    y: {
                        display: true,
                        grid: {
                            color: 'rgba(255, 255, 255, 0.1)'
                        },
                        ticks: {
                            color: '#b8b8d0'
                        }
                    }
                }
            }
        });
    }

    initializeLoadChart() {
        const ctx = document.getElementById('load-chart');
        if (!ctx) return;

        this.charts.load = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: ['CPU', 'Memory', 'Disk', 'Network', 'GPU'],
                datasets: [{
                    label: 'System Load (%)',
                    data: [65, 78, 45, 82, 34],
                    backgroundColor: [
                        'rgba(0, 255, 204, 0.8)',
                        'rgba(255, 0, 255, 0.8)',
                        'rgba(255, 170, 0, 0.8)',
                        'rgba(0, 255, 136, 0.8)',
                        'rgba(255, 68, 68, 0.8)'
                    ],
                    borderColor: [
                        '#00ffcc',
                        '#ff00ff',
                        '#ffaa00',
                        '#00ff88',
                        '#ff4444'
                    ],
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    }
                },
                scales: {
                    x: {
                        grid: {
                            color: 'rgba(255, 255, 255, 0.1)'
                        },
                        ticks: {
                            color: '#b8b8d0'
                        }
                    },
                    y: {
                        beginAtZero: true,
                        max: 100,
                        grid: {
                            color: 'rgba(255, 255, 255, 0.1)'
                        },
                        ticks: {
                            color: '#b8b8d0'
                        }
                    }
                }
            }
        });
    }

    initializeMemoryChart() {
        const ctx = document.getElementById('memory-chart');
        if (!ctx) return;

        this.charts.memory = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['Used', 'Cached', 'Buffered', 'Free'],
                datasets: [{
                    data: [65, 15, 8, 12],
                    backgroundColor: [
                        'rgba(255, 68, 68, 0.8)',
                        'rgba(255, 170, 0, 0.8)',
                        'rgba(0, 255, 204, 0.8)',
                        'rgba(0, 255, 136, 0.8)'
                    ],
                    borderColor: [
                        '#ff4444',
                        '#ffaa00',
                        '#00ffcc',
                        '#00ff88'
                    ],
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'right',
                        labels: {
                            color: '#b8b8d0'
                        }
                    }
                }
            }
        });
    }

    initializeDensityChart() {
        const ctx = document.getElementById('density-chart');
        if (!ctx) return;

        this.charts.density = new Chart(ctx, {
            type: 'radar',
            data: {
                labels: ['UCF', 'Resonance', 'Sync', 'Bandwidth', 'Latency', 'Throughput'],
                datasets: [{
                    label: 'Current',
                    data: [87, 92, 89, 78, 85, 91],
                    borderColor: '#00ffcc',
                    backgroundColor: 'rgba(0, 255, 204, 0.2)',
                    borderWidth: 2
                }, {
                    label: 'Target',
                    data: [90, 95, 92, 85, 90, 95],
                    borderColor: '#ff00ff',
                    backgroundColor: 'rgba(255, 0, 255, 0.1)',
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        labels: {
                            color: '#b8b8d0'
                        }
                    }
                },
                scales: {
                    r: {
                        beginAtZero: true,
                        max: 100,
                        grid: {
                            color: 'rgba(255, 255, 255, 0.1)'
                        },
                        ticks: {
                            color: '#b8b8d0'
                        },
                        pointLabels: {
                            color: '#b8b8d0'
                        }
                    }
                }
            }
        });
    }

    startMetricsUpdates() {
        // Update charts every 5 seconds
        setInterval(() => {
            this.updateLatencyChart();
            this.updateLoadChart();
            this.updateMemoryChart();
            this.updateDensityChart();
        }, 5000);
    }

    updateLatencyChart() {
        if (!this.charts.latency) return;

        const chart = this.charts.latency;
        const newData = Math.floor(Math.random() * 40 + 10);
        
        chart.data.labels.shift();
        chart.data.labels.push(this.getCurrentTimeString());
        
        chart.data.datasets[0].data.shift();
        chart.data.datasets[0].data.push(newData);
        
        chart.update('none'); // Update without animation for smooth real-time effect
    }

    updateLoadChart() {
        if (!this.charts.load) return;

        const chart = this.charts.load;
        chart.data.datasets[0].data = chart.data.datasets[0].data.map(value => {
            const change = (Math.random() - 0.5) * 10;
            return Math.max(10, Math.min(95, value + change));
        });
        
        chart.update();
    }

    updateMemoryChart() {
        if (!this.charts.memory) return;

        const chart = this.charts.memory;
        const used = Math.floor(Math.random() * 20 + 55);
        const cached = Math.floor(Math.random() * 10 + 10);
        const buffered = Math.floor(Math.random() * 8 + 5);
        const free = 100 - used - cached - buffered;
        
        chart.data.datasets[0].data = [used, cached, buffered, Math.max(0, free)];
        chart.update();
    }

    updateDensityChart() {
        if (!this.charts.density) return;

        const chart = this.charts.density;
        chart.data.datasets[0].data = chart.data.datasets[0].data.map(value => {
            const change = (Math.random() - 0.5) * 5;
            return Math.max(70, Math.min(98, value + change));
        });
        
        chart.update();
    }

    generateTimeLabels(count) {
        const labels = [];
        const now = new Date();
        
        for (let i = count - 1; i >= 0; i--) {
            const time = new Date(now - i * 5000); // 5 second intervals
            labels.push(this.formatTime(time));
        }
        
        return labels;
    }

    getCurrentTimeString() {
        return this.formatTime(new Date());
    }

    formatTime(date) {
        return date.toLocaleTimeString('en-US', {
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit'
        });
    }

    generateRandomData(count, min, max) {
        const data = [];
        for (let i = 0; i < count; i++) {
            data.push(Math.floor(Math.random() * (max - min + 1)) + min);
        }
        return data;
    }

    // Method to add custom metrics
    addCustomMetric(chartName, label, data) {
        if (!this.charts[chartName]) return;

        const chart = this.charts[chartName];
        chart.data.datasets.push({
            label: label,
            data: data,
            borderColor: this.getRandomColor(),
            backgroundColor: this.getRandomColor(0.2),
            borderWidth: 2
        });
        
        chart.update();
    }

    getRandomColor(alpha = 1) {
        const colors = [
            `rgba(0, 255, 204, ${alpha})`,
            `rgba(255, 0, 255, ${alpha})`,
            `rgba(255, 170, 0, ${alpha})`,
            `rgba(0, 255, 136, ${alpha})`,
            `rgba(255, 68, 68, ${alpha})`
        ];
        
        return colors[Math.floor(Math.random() * colors.length)];
    }

    // Method to export chart data
    exportChartData(chartName) {
        if (!this.charts[chartName]) return null;

        const chart = this.charts[chartName];
        return {
            labels: chart.data.labels,
            datasets: chart.data.datasets.map(dataset => ({
                label: dataset.label,
                data: dataset.data
            }))
        };
    }

    // Method to reset all charts
    resetAllCharts() {
        Object.keys(this.charts).forEach(chartName => {
            const chart = this.charts[chartName];
            chart.data.datasets.forEach(dataset => {
                dataset.data = dataset.data.map(() => Math.floor(Math.random() * 50 + 25));
            });
            chart.update();
        });
    }
}

// Initialize the metrics visualizer
const metricsVisualizer = new MetricsVisualizer();

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = MetricsVisualizer;
}