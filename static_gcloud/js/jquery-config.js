/**
 * Configuração do jQuery e Máscaras
 * Assistente Financeiro - NAES
 */

$(document).ready(function() {
    console.log('jQuery carregado e configurado!');

    // ====== MÁSCARAS AUTOMÁTICAS ======

    // Máscara de DATA (dd/mm/yyyy) - Formato brasileiro
    $('[data-mask="00/00/0000"]').mask('00/00/0000', {
        placeholder: 'dd/mm/aaaa',
        translation: {
            '0': {pattern: /[0-9]/}
        }
    });

    // Máscara de VALOR MONETÁRIO - Formato brasileiro (R$ 1.500,50)
    $('.money-field, input[type="text"][placeholder*="R$"]').mask('#.##0,00', {
        reverse: true,
        placeholder: 'R$ 0,00',
        translation: {
            '#': {pattern: /[0-9]/, optional: true}
        }
    });

    // Máscara de CPF (caso precise futuramente)
    $('[data-mask="000.000.000-00"]').mask('000.000.000-00', {
        placeholder: '___.___.___-__'
    });

    // Máscara de TELEFONE brasileiro
    $('[data-mask="phone"]').mask('(00) 00000-0000', {
        placeholder: '(__) _____-____',
        translation: {
            '0': {pattern: /[0-9]/}
        }
    });

    // Máscara de CEP
    $('[data-mask="00000-000"]').mask('00000-000', {
        placeholder: '_____-___'
    });

    // ====== MELHORIAS DE UX ======

    // Feedback visual para campos obrigatórios
    $('input[required], select[required], textarea[required]').each(function() {
        $(this).addClass('required-field');

        // Adicionar indicador visual
        if (!$(this).next('.required-indicator').length) {
            $(this).after('<small class="required-indicator text-danger">*</small>');
        }
    });

    // Validação em tempo real para campos de valor
    $('.money-field, input[placeholder*="R$"]').on('input', function() {
        var value = $(this).val().replace(/[^\d,]/g, '');
        var numericValue = parseFloat(value.replace(',', '.'));

        if (numericValue < 0) {
            $(this).addClass('is-invalid');
            if (!$(this).next('.invalid-feedback').length) {
                $(this).after('<div class="invalid-feedback">O valor deve ser positivo</div>');
            }
        } else {
            $(this).removeClass('is-invalid');
            $(this).next('.invalid-feedback').remove();
        }
    });

    // Validação para campos de data
    $('[data-mask="00/00/0000"]').on('blur', function() {
        var date = $(this).val();
        var isValid = isValidBrazilianDate(date);

        if (date && !isValid) {
            $(this).addClass('is-invalid');
            if (!$(this).next('.invalid-feedback').length) {
                $(this).after('<div class="invalid-feedback">Data inválida. Use dd/mm/aaaa</div>');
            }
        } else {
            $(this).removeClass('is-invalid');
            $(this).next('.invalid-feedback').remove();
        }
    });

    // ====== ANIMAÇÕES SUAVES ======

    // Efeito suave para botões
    $('.btn').hover(
        function() {
            $(this).addClass('shadow-lg');
        },
        function() {
            $(this).removeClass('shadow-lg');
        }
    );

    // Efeito fade para alerts/mensagens
    $('.alert').each(function() {
        $(this).hide().fadeIn(500);

        // Auto-hide alerts após 5 segundos
        setTimeout(() => {
            $(this).fadeOut(500);
        }, 5000);
    });

    // ====== FUNCIONALIDADES ESPECÍFICAS ======

    // Toggle de filtros (se existir)
    $('#filterToggle').on('click', function() {
        $('#filterCollapse').slideToggle(300);
        $(this).find('i').toggleClass('fa-chevron-down fa-chevron-up');
    });

    // Confirmação para exclusões
    $('a[href*="delete"], .delete-btn').on('click', function(e) {
        e.preventDefault();
        var href = $(this).attr('href');

        if (confirm('Tem certeza que deseja excluir este item? Esta ação não pode ser desfeita.')) {
            window.location.href = href;
        }
    });

    // ====== FORMATAÇÃO AUTOMÁTICA ======

    // Formatar valores monetários ao perder foco
    $('.money-field, input[placeholder*="R$"]').on('blur', function() {
        var value = $(this).val();
        if (value && !value.startsWith('R$')) {
            $(this).val('R$ ' + value);
        }
    });

    // Log para debug
    console.log('Máscaras aplicadas:', {
        'Data': $('[data-mask="00/00/0000"]').length,
        'Valor': $('.money-field, input[placeholder*="R$"]').length,
        'Campos obrigatórios': $('input[required]').length
    });
});

// ====== FUNÇÕES AUXILIARES ======

/**
 * Valida data no formato brasileiro (dd/mm/yyyy)
 */
function isValidBrazilianDate(dateStr) {
    if (!dateStr || dateStr.length !== 10) return false;

    var parts = dateStr.split('/');
    if (parts.length !== 3) return false;

    var day = parseInt(parts[0], 10);
    var month = parseInt(parts[1], 10);
    var year = parseInt(parts[2], 10);

    if (year < 1900 || year > 2100) return false;
    if (month < 1 || month > 12) return false;
    if (day < 1 || day > 31) return false;

    // Validar dias do mês
    var daysInMonth = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];

    // Ano bissexto
    if (year % 4 === 0 && (year % 100 !== 0 || year % 400 === 0)) {
        daysInMonth[1] = 29;
    }

    return day <= daysInMonth[month - 1];
}

/**
 * Formatar valor para moeda brasileira
 */
function formatBrazilianCurrency(value) {
    return new Intl.NumberFormat('pt-BR', {
        style: 'currency',
        currency: 'BRL'
    }).format(value);
}

/**
 * Parsear valor monetário brasileiro para número
 */
function parseBrazilianCurrency(value) {
    if (!value) return 0;
    return parseFloat(value.replace(/[^\d,]/g, '').replace(',', '.')) || 0;
}

// ====== FUNCIONALIDADES DE FILTROS AVANÇADOS ======

/**
 * Controla filtros expansíveis globalmente
 */
function initAdvancedFilters() {
    // Controlar botões de filtros
    $('.filter-toggle').on('click', function() {
        var target = $(this).data('bs-target');
        var isExpanded = $(this).attr('aria-expanded') === 'true';
        
        if (isExpanded) {
            $(this).find('.filter-text').text('Mostrar Filtros');
            $(this).find('i').removeClass('fa-chevron-up').addClass('fa-chevron-down');
        } else {
            $(this).find('.filter-text').text('Ocultar Filtros');
            $(this).find('i').removeClass('fa-chevron-down').addClass('fa-chevron-up');
        }
    });

    // Auto-expandir filtros se há parâmetros GET
    if (window.location.search.includes('=') && !window.location.search.includes('page=')) {
        $('.filter-collapse').addClass('show');
        $('.filter-toggle .filter-text').text('Ocultar Filtros');
        $('.filter-toggle i').removeClass('fa-chevron-down').addClass('fa-chevron-up');
    }

    // Limpar filtro individual
    $('.filter-badge .remove-filter').on('click', function(e) {
        e.preventDefault();
        var url = $(this).attr('href');
        window.location.href = url;
    });

    // Contador de filtros ativos
    updateFilterCount();
}

/**
 * Conta e exibe número de filtros ativos
 */
function updateFilterCount() {
    var activeFilters = $('.filter-badge').length;
    var filterButton = $('.filter-toggle');
    
    if (activeFilters > 0) {
        if (!filterButton.find('.filter-count').length) {
            filterButton.append('<span class="filter-count badge bg-danger ms-1">' + activeFilters + '</span>');
        } else {
            filterButton.find('.filter-count').text(activeFilters);
        }
    } else {
        filterButton.find('.filter-count').remove();
    }
}

/**
 * Melhora UX dos filtros com loading states
 */
function enhanceFilterUX() {
    // Loading state ao submeter filtros
    $('form[method="get"]').on('submit', function() {
        var submitBtn = $(this).find('button[type="submit"]');
        var originalText = submitBtn.html();
        
        submitBtn.html('<i class="fas fa-spinner fa-spin me-2"></i>Filtrando...');
        submitBtn.prop('disabled', true);
        
        // Restaurar após um tempo (fallback)
        setTimeout(function() {
            submitBtn.html(originalText);
            submitBtn.prop('disabled', false);
        }, 3000);
    });

    // Feedback visual para campos de filtro
    $('.form-control, .form-select').on('input change', function() {
        var hasValue = $(this).val() && $(this).val().length > 0;
        
        if (hasValue) {
            $(this).addClass('has-value');
        } else {
            $(this).removeClass('has-value');
        }
    });

    // Inicializar estado dos campos
    $('.form-control, .form-select').each(function() {
        var hasValue = $(this).val() && $(this).val().length > 0;
        if (hasValue) {
            $(this).addClass('has-value');
        }
    });
}

// Inicializar quando documento estiver pronto
$(document).ready(function() {
    initAdvancedFilters();
    enhanceFilterUX();
});