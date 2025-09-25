/**
 * Script principal para o dashboard financeiro
 * Responsável por inicializar os gráficos e integrar os dados do backend
 */

// Array com nomes dos meses em português
const MONTH_LABELS = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez'];

// Inicializar os gráficos quando o DOM estiver pronto
document.addEventListener('DOMContentLoaded', function() {
    console.log('Dashboard JS: DOM loaded');
    
    // Verificar se os dados dos gráficos estão disponíveis
    if (!window.chartData) {
        console.error('Dashboard JS: Chart data not found in window.chartData');
        return;
    }
    
    console.log('Dashboard JS: Chart data:', window.chartData);
    console.log('Dashboard JS: Chart data TYPE:', typeof window.chartData);
    console.log('Dashboard JS: Category labels TYPE:', typeof window.chartData.categoryLabels);
    console.log('Dashboard JS: Category data TYPE:', typeof window.chartData.categoryData);
    
    // Inicializa o gráfico de despesas mensais
    if (document.getElementById('myAreaChart')) {
        try {
            const monthlyData = window.chartData.monthlyExpenses;
            console.log('Dashboard JS: Monthly data:', monthlyData);
            
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
            const categoryLabels = window.chartData.categoryLabels;
            const categoryData = window.chartData.categoryData;
            
            console.log('Dashboard JS: Category labels:', categoryLabels);
            console.log('Dashboard JS: Category data:', categoryData);
            console.log('Dashboard JS: Category labels length:', categoryLabels?.length);
            console.log('Dashboard JS: Category data length:', categoryData?.length);
            
            // Verificar se os dados existem e são arrays
            if (!Array.isArray(categoryLabels) || !Array.isArray(categoryData)) {
                console.error('Dashboard JS: Category data is not array format');
                console.error('Dashboard JS: categoryLabels is array:', Array.isArray(categoryLabels));
                console.error('Dashboard JS: categoryData is array:', Array.isArray(categoryData));
                return;
            }
            
            if (categoryLabels.length === 0 || categoryData.length === 0) {
                console.error('Dashboard JS: Empty category data');
                return;
            }
            
            initPieChart('myPieChart', categoryLabels, categoryData);
            console.log('Dashboard JS: Pie chart initialized');
        } catch (error) {
            console.error('Dashboard JS: Error initializing pie chart:', error);
            console.error('Dashboard JS: Full error:', error.stack);
        }
    } else {
        console.log('Dashboard JS: myPieChart element not found');
    }
});