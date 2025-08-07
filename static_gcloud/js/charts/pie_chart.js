/**
 * Inicializa um gráfico de pizza para exibir a distribuição de despesas por categoria
 * @param {string} elementId - ID do elemento canvas onde o gráfico será renderizado
 * @param {Array} categoryLabels - Array com os nomes das categorias
 * @param {Array} categoryData - Array com os valores das despesas por categoria
 * @returns {Chart} - Instância do gráfico criado
 */
function initPieChart(elementId, categoryLabels, categoryData) {
    // Cores para o gráfico de pizza - podemos ter várias categorias
    const backgroundColors = [
        '#4e73df', '#1cc88a', '#36b9cc', '#f6c23e', '#e74a3b', 
        '#5a5c69', '#8B4513', '#6A5ACD', '#FF6347', '#3CB371',
        '#4682B4', '#9370DB', '#20B2AA', '#B22222', '#4B0082'
    ];

    // Dados para o gráfico de pizza
    const chartData = {
        labels: categoryLabels,
        datasets: [{
            backgroundColor: backgroundColors.slice(0, categoryLabels.length),
            data: categoryData,
            borderWidth: 1
        }]
    };

    // Configuração do gráfico de pizza
    const chartConfig = {
        type: 'doughnut',
        data: chartData,
        options: {
            maintainAspectRatio: false,
            cutout: '60%',
            plugins: {
                tooltip: {
                    backgroundColor: 'rgb(255, 255, 255)',
                    bodyColor: '#858796',
                    borderColor: '#dddfeb',
                    borderWidth: 1,
                    padding: 15,
                    displayColors: false,
                    callbacks: {
                        label: function(context) {
                            const value = context.parsed;
                            const percent = Math.round((value / context.dataset.data.reduce((a, b) => a + b, 0)) * 100);
                            return context.label + ': ' + percent + '%';
                        }
                    }
                },
                legend: {
                    position: 'bottom',
                    labels: {
                        boxWidth: 20,
                        font: {
                            size: 11
                        }
                    }
                }
            }
        }
    };

    // Inicializar o gráfico de pizza
    return new Chart(
        document.getElementById(elementId),
        chartConfig
    );
}