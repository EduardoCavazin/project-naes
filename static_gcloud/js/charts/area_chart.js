/**
 * Inicializa um gráfico de área para exibir despesas mensais
 * @param {string} elementId - ID do elemento canvas onde o gráfico será renderizado
 * @param {Array} monthLabels - Array com os nomes dos meses
 * @param {Array} monthlyData - Array com os valores das despesas por mês
 * @returns {Chart} - Instância do gráfico criado
 */
function initAreaChart(elementId, monthLabels, monthlyData) {
    // Dados para o gráfico de área
    const chartData = {
        labels: monthLabels,
        datasets: [{
            label: 'Despesas Mensais',
            lineTension: 0.3,
            backgroundColor: 'rgba(78, 115, 223, 0.05)',
            borderColor: 'rgba(78, 115, 223, 1)',
            pointRadius: 3,
            pointBackgroundColor: 'rgba(78, 115, 223, 1)',
            pointBorderColor: 'rgba(78, 115, 223, 1)',
            pointHoverRadius: 5,
            pointHoverBackgroundColor: 'rgba(78, 115, 223, 1)',
            pointHoverBorderColor: 'rgba(78, 115, 223, 1)',
            pointHitRadius: 10,
            pointBorderWidth: 2,
            data: monthlyData,
        }],
    };

    // Configuração do gráfico de área
    const chartConfig = {
        type: 'line',
        data: chartData,
        options: {
            maintainAspectRatio: false,
            layout: {
                padding: {
                    left: 10,
                    right: 25,
                    top: 25,
                    bottom: 0
                }
            },
            scales: {
                x: {
                    grid: {
                        display: false,
                        drawBorder: false
                    }
                },
                y: {
                    ticks: {
                        maxTicksLimit: 5,
                        callback: function(value) {
                            return 'R$ ' + value.toLocaleString();
                        }
                    },
                    grid: {
                        color: 'rgb(234, 236, 244)',
                        drawBorder: false,
                        borderDash: [2],
                        zeroLineBorderDash: [2]
                    }
                },
            },
            plugins: {
                tooltip: {
                    backgroundColor: 'rgb(255, 255, 255)',
                    bodyColor: '#858796',
                    titleColor: '#6e707e',
                    titleFontSize: 14,
                    borderColor: '#dddfeb',
                    borderWidth: 1,
                    padding: 15,
                    displayColors: false,
                    callbacks: {
                        label: function(context) {
                            const value = context.parsed.y;
                            return 'R$ ' + value.toLocaleString();
                        }
                    }
                }
            }
        }
    };

    // Inicializar o gráfico de área
    return new Chart(
        document.getElementById(elementId),
        chartConfig
    );
}