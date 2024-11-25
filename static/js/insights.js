if (!window.charts) {
    window.charts = {};
}

function adjustChartSize() {
    const chartContainers = document.querySelectorAll('.grafico');
    chartContainers.forEach((container) => {
        container.style.height = `${window.innerHeight}px`;
    });
}

document.addEventListener('DOMContentLoaded', adjustChartSize);
window.addEventListener('resize', adjustChartSize);

window.onload = function () {
    const selectInput = document.getElementById('categoria-filtro');
    selectInput.selectedIndex = 0;
};

document.getElementById('categoria-filtro').addEventListener('change', function () {
    const selectedCategory = this.value;

    //console.log('Categoria selecionada:', selectedCategory);

    document.querySelectorAll('.grafico').forEach(function (grafico) {
        grafico.style.display = 'none';
    });

    if (selectedCategory) {
        //console.log('Enviando requisição para /filterInsight com categoria:', selectedCategory);

        fetch('/filterInsight', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                'categoria-filtro': selectedCategory
            })
        })
            .then(response => {
                //console.log('Resposta:', response);
                return response.json();
            })
            .then(data => {
                //console.log('Dados recebidos:', data);
                if (data.erro) {
                    console.error('Erro na resposta:', data.erro);
                } else {
                    const chartSelected = document.getElementById(selectedCategory);
                    if (chartSelected) {
                        chartSelected.style.display = 'block';
                        //console.log('Exibindo gráfico para a categoria:', selectedCategory);
                        const chartType = getChartType(selectedCategory);
                        renderChart(selectedCategory, data, chartType);
                    } else {
                        console.warn(`Elemento com id "${selectedCategory}" não encontrado.`);
                    }
                }
            })
            .catch(error => {
                console.error('Erro ao buscar dados:', error);
            });
    } else {
        console.warn('Nenhuma categoria selecionada.');
    }
});

function renderChart(chartId, data, chartType = 'line') {
    //console.log('Renderizando gráfico com dados:', data);

    const ctx = document.getElementById(`${chartId}-chart`)?.getContext('2d');

    if (!ctx) {
        console.error(`Contexto do gráfico não encontrado para o id "${chartId}"`);
        return;
    }

    if (window.charts[`${chartId}Chart`]) {
        //console.log(`Destruindo gráfico existente para o id "${chartId}"`);
        window.charts[`${chartId}Chart`].destroy();
    }

    let labels = data.labels || [];
    let values = data.values || [];

    //console.log('Labels:', labels);
    //console.log('Values:', values);

    window.charts[`${chartId}Chart`] = new Chart(ctx, {
        type: chartType,
        data: {
            labels: labels,
            datasets: [{
                label: chartId,
                data: values,
                borderColor: getChartColor(chartId),
                backgroundColor: getChartBackgroundColor(chartId),
                fill: chartType === 'line' ? true : false,
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            indexAxis: chartId === 'produtos-mais-vendidos' ? 'y' : 'x'
        }
    });

}

function getChartType(chartId) {
    const chartTypes = {
        'vendas-mensais': 'line',
        'receita-mensal': 'bar',
        'vendas-diarias': 'line',
        'receita-diaria': 'bar',
        'vendas-produto': 'pie',
        'receita-produto': 'doughnut',
        'produtos-estoque': 'bar',
        'produtos-mais-vendidos': 'bar',
        'vendas-usuario': 'bar'
    };
    //console.log(`Tipo de gráfico para ${chartId}:`, chartTypes[chartId] || 'line');
    return chartTypes[chartId] || 'line';
}

function getChartColor(chartId) {
    const colors = {
        'vendas-mensais': '#00D1B2',
        'receita-mensal': '#FF3860',
        'vendas-diarias': '#FFDD57',
        'receita-diaria': '#7B2CBF',
        'vendas-produto': '#FFDD57',
        'receita-produto': '#7B2CBF',
        'produtos-estoque': '#4A90E2',
        'produtos-mais-vendidos': '#F5A623',
        'vendas-usuario': '#50E3C2'
    };
    //console.log(`Cor para o gráfico ${chartId}:`, colors[chartId] || '#000000');
    return colors[chartId] || '#000000';
}

function getChartBackgroundColor(chartId) {
    const backgroundColors = {
        'vendas-mensais': 'rgba(0, 209, 178, 0.2)',
        'receita-mensal': 'rgba(255, 56, 96, 0.2)',
        'vendas-diarias': 'rgba(255, 221, 87, 0.2)',
        'receita-diaria': 'rgba(123, 44, 191, 0.2)',
        'vendas-produto': 'rgba(255, 221, 87, 0.2)',
        'receita-produto': 'rgba(123, 44, 191, 0.2)',
        'produtos-estoque': 'rgba(74, 144, 226, 0.2)',
        'produtos-mais-vendidos': 'rgba(245, 166, 35, 0.2)',
        'vendas-usuario': 'rgba(80, 227, 194, 0.2)'
    };
    //console.log(`Cor de fundo para o gráfico ${chartId}:`, backgroundColors[chartId] || 'rgba(0, 0, 0, 0.2)');
    return backgroundColors[chartId] || 'rgba(0, 0, 0, 0.2)';
}
