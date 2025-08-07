/**
 * Script principal para o dashboard financeiro
 * Responsável por inicializar os gráficos e integrar os dados do backend
 */

// Array com nomes dos meses em português
const MONTH_LABELS = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez'];

// Inicializar os gráficos quando o DOM estiver pronto
document.addEventListener('DOMContentLoaded', function() {
    // Inicializa o gráfico de despesas mensais
    if (document.getElementById('myAreaChart')) {
        // Os dados mensais vêm da página através do data-attribute
        const monthlyData = JSON.parse(
            document.getElementById('chart-container').getAttribute('data-monthly-data')
        );
        
        initAreaChart('myAreaChart', MONTH_LABELS, monthlyData);
    }
    
    // Inicializa o gráfico de distribuição por categoria
    if (document.getElementById('myPieChart')) {
        // Os dados de categorias vêm da página através dos data-attributes
        const categoryLabels = JSON.parse(
            document.getElementById('chart-container').getAttribute('data-category-labels')
        );
        
        const categoryData = JSON.parse(
            document.getElementById('chart-container').getAttribute('data-category-data')
        );
        
        initPieChart('myPieChart', categoryLabels, categoryData);
    }
});