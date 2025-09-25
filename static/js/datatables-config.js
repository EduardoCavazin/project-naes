/**
 * Configuração do DataTables
 * Assistente Financeiro - NAES
 */

$(document).ready(function() {
    console.log('DataTables carregado e configurado!');

    // ====== CONFIGURAÇÃO PADRÃO DATATABLES ======

    // Configuração global em português brasileiro
    $.extend(true, $.fn.dataTable.defaults, {
        language: {
            "sEmptyTable": "Nenhum dado disponível na tabela",
            "sInfo": "Mostrando de _START_ até _END_ de _TOTAL_ registros",
            "sInfoEmpty": "Mostrando 0 até 0 de 0 registros",
            "sInfoFiltered": "(filtrado de _MAX_ registros no total)",
            "sInfoPostFix": "",
            "sInfoThousands": ".",
            "sLengthMenu": "Mostrar _MENU_ registros por página",
            "sLoadingRecords": "Carregando...",
            "sProcessing": "Processando...",
            "sSearch": "🔍 Buscar:",
            "sSearchPlaceholder": "Digite aqui para buscar...",
            "sZeroRecords": "Nenhum registro encontrado",
            "oPaginate": {
                "sNext": "Próximo",
                "sPrevious": "Anterior",
                "sFirst": "Primeiro",
                "sLast": "Último"
            },
            "oAria": {
                "sSortAscending": ": ativar para classificar a coluna em ordem crescente",
                "sSortDescending": ": ativar para classificar a coluna em ordem decrescente"
            },
            "buttons": {
                "copy": "Copiar",
                "excel": "📊 Excel",
                "pdf": "📄 PDF",
                "csv": "📋 CSV",
                "print": "🖨️ Imprimir",
                "colvis": "🔧 Colunas"
            }
        },
        responsive: true,
        pageLength: 25,
        lengthMenu: [[10, 25, 50, 100, -1], [10, 25, 50, 100, "Todos"]],
        order: [[0, 'desc']], // Ordenar pela primeira coluna (mais recente)
        autoWidth: false,
        processing: true,
        stateSave: true, // Salvar estado da tabela (ordenação, paginação)
        dom: "<'row'<'col-md-6'><'col-md-6'f>>" +
             "tr" +
             "<'d-none'lip>", // Esconder elementos padrão, vamos posicionar manualmente
        buttons: [
            {
                extend: 'excel',
                className: 'btn btn-success btn-sm me-1',
                text: '📊 Excel',
                title: 'Assistente Financeiro - Relatório'
            },
            {
                extend: 'pdf',
                className: 'btn btn-danger btn-sm me-1',
                text: '📄 PDF',
                title: 'Assistente Financeiro - Relatório',
                orientation: 'landscape',
                pageSize: 'A4'
            },
            {
                extend: 'csv',
                className: 'btn btn-info btn-sm me-1',
                text: '📋 CSV'
            },
            {
                extend: 'print',
                className: 'btn btn-secondary btn-sm',
                text: '🖨️ Imprimir'
            }
        ]
    });

    // ====== APLICAR DATATABLES NAS TABELAS ======

    // Tabela de DESPESAS
    if ($('#expenses-table').length) {
        $('#expenses-table').DataTable({
            columnDefs: [
                {
                    targets: [2], // Coluna de valor (R$)
                    render: function(data, type, row) {
                        if (type === 'display' || type === 'type') {
                            return 'R$ ' + parseFloat(data).toLocaleString('pt-BR', {
                                minimumFractionDigits: 2,
                                maximumFractionDigits: 2
                            });
                        }
                        return data;
                    }
                },
                {
                    targets: [3], // Coluna de data
                    render: function(data, type, row) {
                        if (type === 'display' || type === 'type') {
                            // Converter para formato brasileiro se necessário
                            return data;
                        }
                        return data;
                    }
                },
                {
                    targets: [-1], // Última coluna (ações)
                    orderable: false,
                    searchable: false,
                    width: "120px"
                }
            ],
            buttons: [
                {
                    extend: 'excel',
                    className: 'btn btn-success btn-sm me-1',
                    text: '📊 Despesas Excel',
                    title: 'Minhas Despesas - ' + new Date().toLocaleDateString('pt-BR')
                },
                {
                    extend: 'pdf',
                    className: 'btn btn-danger btn-sm me-1',
                    text: '📄 Despesas PDF',
                    title: 'Relatório de Despesas',
                    orientation: 'landscape'
                },
                {
                    extend: 'csv',
                    className: 'btn btn-info btn-sm',
                    text: '📋 CSV'
                }
            ]
        });
    }

    // Tabela de CHEQUES
    if ($('#cheques-table').length) {
        $('#cheques-table').DataTable({
            columnDefs: [
                {
                    targets: [1], // Coluna de valor (R$)
                    render: function(data, type, row) {
                        if (type === 'display' || type === 'type') {
                            return 'R$ ' + parseFloat(data).toLocaleString('pt-BR', {
                                minimumFractionDigits: 2,
                                maximumFractionDigits: 2
                            });
                        }
                        return data;
                    }
                },
                {
                    targets: [6], // Coluna de status
                    render: function(data, type, row) {
                        if (type === 'display' || type === 'type') {
                            // Manter os badges do Bootstrap
                            return data;
                        }
                        return data;
                    }
                },
                {
                    targets: [-1], // Última coluna (ações)
                    orderable: false,
                    searchable: false,
                    width: "120px"
                }
            ],
            buttons: [
                {
                    extend: 'excel',
                    className: 'btn btn-success btn-sm me-1',
                    text: '📊 Cheques Excel',
                    title: 'Meus Cheques - ' + new Date().toLocaleDateString('pt-BR')
                },
                {
                    extend: 'pdf',
                    className: 'btn btn-danger btn-sm me-1',
                    text: '📄 Cheques PDF',
                    title: 'Relatório de Cheques',
                    orientation: 'landscape'
                },
                {
                    extend: 'csv',
                    className: 'btn btn-info btn-sm',
                    text: '📋 CSV'
                }
            ]
        });
    }

    // ====== INTEGRAÇÃO COM LAYOUT CUSTOMIZADO ======

    // Mover botões de export para o container personalizado
    setTimeout(function() {
        $('.dt-buttons').detach().appendTo('#export-buttons-container');

        // Mover campo de busca para o header da tabela
        var searchInput = $('div.dataTables_filter input').detach();
        searchInput.addClass('form-control form-control-sm');
        searchInput.attr('placeholder', 'Busca rápida na tabela...');
        searchInput.css('max-width', '250px');
        $('#table-controls').append('<div class="input-group input-group-sm"><span class="input-group-text bg-light"><i class="fas fa-search text-muted"></i></span></div>');
        $('#table-controls .input-group').append(searchInput);

        // Mover informações para o footer
        $('div.dataTables_info').detach().appendTo('#table-info-container');

        // Mover paginação para o footer
        $('div.dataTables_paginate').detach().appendTo('#table-pagination-container');

        // Mover length para o header (se necessário)
        var lengthSelect = $('div.dataTables_length select').detach();
        lengthSelect.addClass('form-select form-select-sm me-2');
        $('#table-controls').prepend('<div class="d-flex align-items-center me-3"><small class="text-muted me-2">Mostrar:</small></div>');
        $('#table-controls .d-flex').append(lengthSelect);

        // Limpar containers vazios
        $('.dataTables_filter, .dataTables_length, .dataTables_info, .dataTables_paginate').parent().remove();
    }, 100);

    // ====== MELHORIAS VISUAIS ======

    // Estilizar botões de paginação
    $(document).on('draw.dt', function() {
        $('.paginate_button').addClass('btn btn-sm btn-outline-primary me-1');
        $('.paginate_button.current').addClass('btn-primary').removeClass('btn-outline-primary');
        $('.paginate_button.disabled').addClass('btn-secondary').removeClass('btn-primary btn-outline-primary');

        // Ícones nos botões prev/next
        $('.paginate_button.previous:not(.disabled)').html('<i class="fas fa-chevron-left me-1"></i>Anterior');
        $('.paginate_button.next:not(.disabled)').html('Próximo<i class="fas fa-chevron-right ms-1"></i>');

        // Atualizar contador de registros
        var info = $('.dataTables_info').text();
        if (info) {
            var matches = info.match(/(\d+)/g);
            if (matches && matches.length >= 3) {
                $('#records-count').text(matches[2]).addClass('animate__animated animate__pulse');
                setTimeout(() => $('#records-count').removeClass('animate__animated animate__pulse'), 500);
            }
        }
    });

    // Customizar aparência da busca
    $(document).on('keyup', '#table-controls input', function() {
        var $this = $(this);
        if ($this.val()) {
            $this.parent().addClass('border-primary');
            $this.prev('.input-group-text').html('<i class="fas fa-times text-danger" style="cursor: pointer;" onclick="$(this).closest(\'.input-group\').find(\'input\').val(\'\').trigger(\'keyup\')"></i>');
        } else {
            $this.parent().removeClass('border-primary');
            $this.prev('.input-group-text').html('<i class="fas fa-search text-muted"></i>');
        }
    });

    // ====== RESPONSIVIDADE MÓVEL ======

    // Ajustar layout em dispositivos móveis
    if ($(window).width() < 768) {
        $('.dataTables_filter').addClass('mb-3');
        $('.dataTables_length').addClass('mb-3');

        // Mover botões de export para baixo em mobile
        $('.dt-buttons').addClass('mb-3 d-flex flex-wrap gap-2');
    }

    // ====== LOADING E FEEDBACK ======

    // Mostrar loading durante processamento
    $(document).on('processing.dt', function(e, settings, processing) {
        if (processing) {
            $('body').addClass('loading');
        } else {
            $('body').removeClass('loading');
        }
    });

    // Feedback para exportações
    $(document).on('buttons-action', function(e, buttonApi, dataTable, node) {
        var action = buttonApi.text();

        // Toast notification (se tiver)
        if (typeof showToast === 'function') {
            showToast(`${action} gerado com sucesso!`, 'success');
        } else {
            console.log(`${action} exportado com sucesso!`);
        }
    });

    // ====== INTEGRAÇÃO FILTROS DJANGO + DATATABLES ======

    // Preservar estado do DataTables ao usar filtros Django
    $('form[method="get"]').on('submit', function(e) {
        var table = $('#expenses-table, #cheques-table').DataTable();

        if (table) {
            // Salvar estado atual do DataTables
            var state = table.state();
            if (state) {
                // Adicionar parâmetros do DataTables ao formulário Django
                var form = $(this);

                // Preservar busca do DataTables
                if (state.search && state.search.search) {
                    form.append('<input type="hidden" name="dt_search" value="' + state.search.search + '">');
                }

                // Preservar ordenação
                if (state.order && state.order.length > 0) {
                    form.append('<input type="hidden" name="dt_order_col" value="' + state.order[0][0] + '">');
                    form.append('<input type="hidden" name="dt_order_dir" value="' + state.order[0][1] + '">');
                }

                // Preservar paginação
                if (state.start) {
                    form.append('<input type="hidden" name="dt_start" value="' + state.start + '">');
                }
                if (state.length) {
                    form.append('<input type="hidden" name="dt_length" value="' + state.length + '">');
                }
            }
        }
    });

    // Restaurar estado do DataTables após filtros Django
    $(document).ready(function() {
        var urlParams = new URLSearchParams(window.location.search);

        // Verificar se temos parâmetros do DataTables para restaurar
        setTimeout(function() {
            var table = $('#expenses-table, #cheques-table').DataTable();

            if (table) {
                // Restaurar busca
                var dtSearch = urlParams.get('dt_search');
                if (dtSearch) {
                    table.search(dtSearch).draw();
                    $('#table-controls input').val(dtSearch);
                }

                // Restaurar ordenação
                var orderCol = urlParams.get('dt_order_col');
                var orderDir = urlParams.get('dt_order_dir');
                if (orderCol && orderDir) {
                    table.order([orderCol, orderDir]).draw();
                }

                // Restaurar página
                var start = urlParams.get('dt_start');
                if (start) {
                    table.page(Math.floor(start / table.page.len())).draw();
                }

                // Restaurar tamanho da página
                var length = urlParams.get('dt_length');
                if (length) {
                    table.page.len(length).draw();
                }
            }
        }, 200);
    });

    // Adicionar loading visual durante filtros Django
    $(document).on('submit', 'form[method="get"]', function() {
        var submitBtn = $(this).find('button[type="submit"]');
        var originalText = submitBtn.html();

        submitBtn.prop('disabled', true).html('<i class="fas fa-spinner fa-spin me-2"></i>Filtrando...');

        // Adicionar overlay de loading na tabela
        $('.table-responsive').append('<div id="table-loading-overlay" style="position: absolute; top: 0; left: 0; right: 0; bottom: 0; background: rgba(255,255,255,0.8); z-index: 1000; display: flex; align-items: center; justify-content: center;"><div class="text-center"><i class="fas fa-spinner fa-spin fa-2x text-primary mb-2"></i><br><span class="text-muted">Aplicando filtros...</span></div></div>');

        // Remover loading se a página não carregar (fallback)
        setTimeout(function() {
            submitBtn.prop('disabled', false).html(originalText);
            $('#table-loading-overlay').remove();
        }, 10000);
    });

    // Melhorar feedback visual para filtros ativos
    function updateActiveFiltersDisplay() {
        var urlParams = new URLSearchParams(window.location.search);
        var hasFilters = false;

        // Contar filtros Django ativos
        urlParams.forEach(function(value, key) {
            if (value && key !== 'page' && !key.startsWith('dt_')) {
                hasFilters = true;
            }
        });

        // Adicionar indicador visual
        if (hasFilters) {
            $('#filterToggle').removeClass('btn-outline-primary btn-outline-info')
                              .addClass('btn-primary')
                              .find('i').removeClass('fa-chevron-down')
                              .addClass('fa-filter');

            // Badge com número de filtros
            var filterCount = $('.badge.bg-primary, .badge.bg-info').length;
            if (filterCount > 0 && !$('#filter-count-badge').length) {
                $('#filterToggle').append('<span id="filter-count-badge" class="badge bg-warning text-dark ms-1">' + filterCount + '</span>');
            }
        }
    }

    // Atualizar indicadores na inicialização
    updateActiveFiltersDisplay();

    // Log de debug
    console.log('DataTables aplicado em:', {
        'Despesas': $('#expenses-table').length > 0,
        'Cheques': $('#cheques-table').length > 0,
        'Largura da tela': $(window).width()
    });
});

// ====== FUNÇÕES AUXILIARES ======

/**
 * Função para mostrar toast (opcional)
 */
function showToast(message, type = 'info') {
    // Implementação básica de toast
    var alertClass = 'alert-' + (type === 'success' ? 'success' : 'info');
    var toast = `
        <div class="alert ${alertClass} alert-dismissible fade show position-fixed"
             style="top: 20px; right: 20px; z-index: 9999;" role="alert">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;

    $('body').append(toast);

    // Remove após 3 segundos
    setTimeout(function() {
        $('.alert').fadeOut(500, function() {
            $(this).remove();
        });
    }, 3000);
}

/**
 * Recarregar DataTable (útil após operações AJAX)
 */
function reloadDataTable(tableId) {
    if ($.fn.DataTable.isDataTable('#' + tableId)) {
        $('#' + tableId).DataTable().ajax.reload();
    }
}

/**
 * Destruir e recriar DataTable (útil para atualizações dinâmicas)
 */
function refreshDataTable(tableId) {
    if ($.fn.DataTable.isDataTable('#' + tableId)) {
        $('#' + tableId).DataTable().destroy();
        $('#' + tableId).DataTable();
    }
}