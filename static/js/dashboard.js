/**
 * Script principal para o dashboard financeiro
 * Responsável por inicializar os gráficos e integrar os dados do backend
 */

// Array com nomes dos meses em português
const MONTH_LABELS = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez'];

// Inicializar os gráficos quando o DOM estiver pronto
document.addEventListener('DOMContentLoaded', function() {
    console.log('Dashboard JS: DOM loaded');
    
    const chartContainer = document.getElementById('chart-container');
    if (!chartContainer) {
        console.log('Dashboard JS: chart-container not found');
        return;
    }
    
    // Inicializa o gráfico de despesas mensais
    if (document.getElementById('myAreaChart')) {
        try {
            // Os dados mensais vêm da página através do data-attribute
            const monthlyDataRaw = chartContainer.getAttribute('data-monthly-data');
            console.log('Dashboard JS: Monthly data raw:', monthlyDataRaw);
            
            const monthlyData = JSON.parse(monthlyDataRaw);
            console.log('Dashboard JS: Monthly data parsed:', monthlyData);
            
            initAreaChart('myAreaChart', MONTH_LABELS, monthlyData);
            console.log('Dashboard JS: Area chart initialized');
        } catch (error) {
            console.error('Dashboard JS: Error initializing area chart:', error);
        }
    } else {
        console.log('Dashboard JS: myAreaChart element not found');
    }
    
    // Inicializa o gráfico de distribuição por categoria
    if (document.getElementById('myPieChart')) {
        try {
            // Os dados de categorias vêm da página através dos data-attributes
            const categoryLabelsRaw = chartContainer.getAttribute('data-category-labels');
            const categoryDataRaw = chartContainer.getAttribute('data-category-data');
            
            console.log('Dashboard JS: Category labels raw:', categoryLabelsRaw);
            console.log('Dashboard JS: Category data raw:', categoryDataRaw);
            
            const categoryLabels = JSON.parse(categoryLabelsRaw);
            const categoryData = JSON.parse(categoryDataRaw);
            
            console.log('Dashboard JS: Category labels parsed:', categoryLabels);
            console.log('Dashboard JS: Category data parsed:', categoryData);
            
            initPieChart('myPieChart', categoryLabels, categoryData);
            console.log('Dashboard JS: Pie chart initialized');
        } catch (error) {
            console.error('Dashboard JS: Error initializing pie chart:', error);
        }
    } else {
        console.log('Dashboard JS: myPieChart element not found');
    }
});