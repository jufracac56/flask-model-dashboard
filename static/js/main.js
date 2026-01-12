 // Datos para colores de cada métrica
        var mlColors = {
            accuracy: '#4CAF50',    // Verde para Accuracy
            f1score: '#2196F3',     // Azul para F1 Score  
            precision: '#FF9800',   // Naranja para Precision
            recall: '#9C27B0'       // Púrpura para Recall
        };

        // Variables globales para almacenar las instancias de los gráficos
        var radarChartInstance = null;
        var barChartInstance = null;
        var confusionMatrixInstance = null;
        var classMetricsInstance = null;
        var gaugeInstances = {};

        // Función para crear el gráfico radar con datos de la API
        function createRadarChartFromAPI(apiData) {
            var ctx = document.getElementById('radarChart').getContext('2d');
            
            if (radarChartInstance) {
                radarChartInstance.destroy();
            }

            radarChartInstance = new Chart(ctx, {
                type: 'radar',
                data: {
                    labels: apiData.labels,
                    datasets: [{
                        label: 'Model Performance',
                        data: apiData.data,
                        borderColor: 'rgba(54, 162, 235, 1)',
                        backgroundColor: 'rgba(54, 162, 235, 0.2)',
                        pointBackgroundColor: 'rgba(54, 162, 235, 1)',
                        pointBorderColor: '#fff',
                        pointHoverBackgroundColor: '#fff',
                        pointHoverBorderColor: 'rgba(54, 162, 235, 1)',
                        borderWidth: 2,
                        pointRadius: 5
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: true,
                    aspectRatio: 1.1,
                    plugins: {
                        legend: {
                            display: false
                        },
                        datalabels: {
                            display: true,
                            color: '#333',
                            font: {
                                weight: 'bold'
                            },
                            formatter: (value) => {
                                return (value * 100).toFixed(1) + '%';
                            }
                        }
                    },
                    scales: {
                        r: {
                            min: 0,
                            max: 1,
                            ticks: {
                                stepSize: 0.2,
                                callback: function(value) {
                                    return (value * 100) + '%';
                                }
                            },
                            grid: {
                                color: 'rgba(0,0,0,0.1)'
                            }
                        }
                    }
                },
                plugins: [ChartDataLabels]
            });
        }

        // Función para crear el gráfico de barras con datos de la API
        function createBarChartFromAPI(apiData) {
            var ctx = document.getElementById('barChart').getContext('2d');
            
            if (barChartInstance) {
                barChartInstance.destroy();
            }

            barChartInstance = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: apiData.labels,
                    datasets: [{
                        label: 'Score',
                        data: apiData.data,
                        backgroundColor: [
                            mlColors.accuracy,
                            mlColors.f1score,
                            mlColors.precision,
                            mlColors.recall
                        ],
                        borderColor: [
                            mlColors.accuracy,
                            mlColors.f1score,
                            mlColors.precision,
                            mlColors.recall
                        ],
                        borderWidth: 2
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: true,
                    aspectRatio: 1.3,
                    plugins: {
                        legend: {
                            display: false
                        },
                        datalabels: {
                            anchor: 'end',
                            align: 'top',
                            color: 'black',
                            font: {
                                weight: 'bold'
                            },
                            formatter: (value) => {
                                return (value * 100).toFixed(1) + '%';
                            }
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            max: 1,
                            ticks: {
                                callback: function(value) {
                                    return (value * 100) + '%';
                                }
                            }
                        }
                    }
                },
                plugins: [ChartDataLabels]
            });
        }

        // Función para crear gráficos gauge con datos de la API
        function createGaugeChartFromAPI(canvasId, value, color, label) {
            var ctx = document.getElementById(canvasId).getContext('2d');
            
            if (gaugeInstances[canvasId]) {
                gaugeInstances[canvasId].destroy();
            }

            var percentage = value * 100;
            
            gaugeInstances[canvasId] = new Chart(ctx, {
                type: 'doughnut',
                data: {
                    datasets: [{
                        data: [percentage, 100 - percentage],
                        backgroundColor: [color, '#e0e0e0'],
                        borderWidth: 0,
                        circumference: 180,
                        rotation: 270
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: true,
                    aspectRatio: 2,
                    plugins: {
                        legend: {
                            display: false
                        },
                        tooltip: {
                            enabled: false
                        },
                        datalabels: {
                            display: true,
                            color: '#333',
                            font: {
                                size: 16,
                                weight: 'bold'
                            },
                            formatter: function(value, context) {
                                if (context.dataIndex === 0) {
                                    return percentage.toFixed(1) + '%';
                                }
                                return '';
                            }
                        }
                    },
                    cutout: '70%'
                },
                plugins: [ChartDataLabels, {
                    beforeDraw: function(chart) {
                        var ctx = chart.ctx;
                        var centerX = chart.chartArea.left + (chart.chartArea.right - chart.chartArea.left) / 2;
                        var centerY = chart.chartArea.bottom - 20;
                        
                        ctx.fillStyle = getQualityColor(value);
                        ctx.font = 'bold 12px Arial';
                        ctx.textAlign = 'center';
                        ctx.fillText(getQualityLabel(value), centerX, centerY);
                    }
                }]
            });
        }

        // Función para crear la matriz de confusión como tabla
        function createConfusionMatrixTable(confusionMatrix) {
            const table = document.getElementById('confusionTable');
            const cells = table.querySelectorAll('.confusion-cell');
            
            let cellIndex = 0;
            for (let i = 0; i < confusionMatrix.length; i++) {
                for (let j = 0; j < confusionMatrix[i].length; j++) {
                    const value = confusionMatrix[i][j];
                    const cell = cells[cellIndex];
                    
                    cell.textContent = value;
                    cell.setAttribute('data-value', value);
                    
                    // Aplicar colores basados en el valor
                    if (value >= 8) {
                        cell.classList.add('high-value');
                    } else if (value >= 4) {
                        cell.classList.add('medium-value');
                    } else {
                        cell.classList.add('low-value');
                    }
                    
                    cellIndex++;
                }
            }
        }

        // Función para crear tarjetas de métricas por clase
        function createClassMetricsCards(classificationReport) {
            const container = document.getElementById('classCardsContainer');
            container.innerHTML = ''; // Limpiar contenido anterior
            
            const classes = [
                { key: 'Iris-setosa', name: 'Setosa', class: 'setosa', emoji: '🌸' },
                { key: 'Iris-versicolor', name: 'Versicolor', class: 'versicolor', emoji: '🌺' },
                { key: 'Iris-virginica', name: 'Virginica', class: 'virginica', emoji: '🌻' }
            ];
            
            classes.forEach(cls => {
                if (classificationReport[cls.key]) {
                    const metrics = classificationReport[cls.key];
                    
                    const card = document.createElement('div');
                    card.className = `class-card ${cls.class}`;
                    
                    card.innerHTML = `
                        <div class="class-card-title">${cls.emoji} ${cls.name}</div>
                        <div class="class-metrics-grid">
                            <div class="metric-item">
                                <div class="metric-label">Precision</div>
                                <div class="metric-value">${(metrics.precision * 100).toFixed(1)}%</div>
                            </div>
                            <div class="metric-item">
                                <div class="metric-label">Recall</div>
                                <div class="metric-value">${(metrics.recall * 100).toFixed(1)}%</div>
                            </div>
                            <div class="metric-item">
                                <div class="metric-label">F1-Score</div>
                                <div class="metric-value">${(metrics['f1-score'] * 100).toFixed(1)}%</div>
                            </div>
                            <div class="support-item">
                                <div class="metric-label">Support</div>
                                <div class="metric-value">${metrics.support} samples</div>
                            </div>
                        </div>
                    `;
                    
                    container.appendChild(card);
                }
            });
        }

        // Función auxiliar para determinar el color según la calidad
        function getQualityColor(value) {
            if (value >= 0.9) return '#4CAF50';
            if (value >= 0.8) return '#8BC34A';
            if (value >= 0.7) return '#FFC107';
            if (value >= 0.6) return '#FF9800';
            return '#F44336';
        }

        // Función auxiliar para determinar la etiqueta de calidad
        function getQualityLabel(value) {
            if (value >= 0.9) return 'Excelente';
            if (value >= 0.8) return 'Bueno';
            if (value >= 0.7) return 'Regular';
            if (value >= 0.6) return 'Bajo';
            return 'Malo';
        }

        // Función principal para cargar todos los gráficos con datos de la API
        function loadDashboardFromAPI(apiData) {
            // Crear estructura de datos para compatibilidad con gráficos existentes
            var basicMetrics = {
                labels: ['Accuracy', 'F1 Score', 'Precision', 'Recall'],
                data: [apiData.accuracy, apiData.f1_score, apiData.precision, apiData.recall]
            };

            // Cargar gráficos existentes
            createRadarChartFromAPI(basicMetrics);
            createBarChartFromAPI(basicMetrics);
            createGaugeChartFromAPI('accuracyGauge', apiData.accuracy, mlColors.accuracy, 'Accuracy');
            createGaugeChartFromAPI('f1Gauge', apiData.f1_score, mlColors.f1score, 'F1 Score');
            createGaugeChartFromAPI('precisionGauge', apiData.precision, mlColors.precision, 'Precision');
            createGaugeChartFromAPI('recallGauge', apiData.recall, mlColors.recall, 'Recall');

            // Cargar nuevos elementos de classification report
            if (apiData.confusion_matrix) {
                createConfusionMatrixTable(apiData.confusion_matrix);
            }
            if (apiData.classification_report) {
                createClassMetricsCards(apiData.classification_report);
            }
        }

        // Llamar a la API '/metrics' para obtener las métricas y mostrarlas en todos los gráficos
        fetch('/metrics')  
            .then(response => response.json())  // Convertir la respuesta en formato JSON
            .then(data => {
                // Cargar todos los gráficos con los datos de la API
                loadDashboardFromAPI(data);
                
                // Configurar actualizaciones automáticas cada 10 segundos
                setInterval(() => {
                    fetch('/metrics')
                        .then(response => response.json())
                        .then(newData => {
                            loadDashboardFromAPI(newData);
                        });
                }, 10000); // Actualizar cada 10 segundos
            });