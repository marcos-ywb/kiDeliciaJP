
const form = document.getElementById('new-venda-form');
form.addEventListener('submit', function (event) {
    const inputsPreco = document.querySelectorAll('input[name="preco[]"]');
    inputsPreco.forEach(input => {
        console.log("Preço enviado:", input.value);
    });
});


function formatarMoeda(valor) {
    return new Intl.NumberFormat('pt-BR', {
        style: 'currency',
        currency: 'BRL',
    }).format(valor);
}



document.addEventListener('DOMContentLoaded', () => {

    const produtosDataElement = document.getElementById("produtos-data");
    const produtosDisponiveis = JSON.parse(produtosDataElement.dataset.produtos);
    console.log("Produtos disponíveis:", produtosDisponiveis);

    const addProductBtn = document.getElementById("add-product");
    const produtosLista = document.getElementById("produtos-lista");
    const totalVendaInput = document.querySelector('input[name="total-venda"]');

    addProductBtn.addEventListener("click", function () {
        const produtoFieldGroup = document.createElement("div");
        produtoFieldGroup.className = "field is-grouped product-group";

        let optionsHTML = `<option value="" disabled selected>Selecione um produto...</option>`;
        produtosDisponiveis.forEach(produto => {
            const produtoId = produto[0];
            const produtoNome = produto[1];
            const produtoPreco = produto[2];
            const produtoEstoque = produto[3];


            if (produtoEstoque > 0) {
                optionsHTML += `
                <option value="${produtoId}" data-preco="${produtoPreco}">
                    ${produtoNome} (Em estoque: ${produtoEstoque})
                </option>`;
            }
            else {
                optionsHTML += `
                <option value="${produtoId}" data-preco="${produtoPreco}" disabled>
                    ${produtoNome} 
                    <span class="has-text-danger">(Fora de estoque)</span>
                </option>`;
            }


        });

        produtoFieldGroup.innerHTML = `

            <div class="field is-fullwidth">
                <div class="columns is-2 are-medium">

                    <!--Selecionar produtos-->
                    <div class="column">
                        <div class="control">
                            <div class="select is-medium is-fullwidth">
                                <select name="produto[]" required>
                                    ${optionsHTML}
                                </select>
                            </div>
                        </div>
                    </div>

                    <!--Quantidade de cada produto-->
                    <div class="column">
                        <div class="control">
                            <input class="input is-medium is-fullwidth" type="number" name="quantidade[]" placeholder="Quantidade" min="1" required>
                        </div>
                    </div>

                    <input type="hidden" name="preco[]" value="">

                    <!--Remover produto-->
                    <div class="column">
                        <button class="button is-medium is-fullwidth is-danger is-outlined remove-product" type="button">Remover</button>
                    </div>


                </div>
            </div>


        `;

        produtosLista.appendChild(produtoFieldGroup);

        atualizarTotal();

        addProductBtn.scrollIntoView({ behavior: "smooth" });
    });

    produtosLista.addEventListener("change", function (event) {
        if (event.target.name === "produto[]") {
            const produtoSelect = event.target;
            const precoUnitario = produtoSelect.selectedOptions[0]?.getAttribute("data-preco") || 0;

            console.log('Produto selecionado:', produtoSelect.value);
            console.log('Preço unitário capturado:', precoUnitario);

            const hiddenInput = produtoSelect.closest('.product-group').querySelector('input[name="preco[]"]');
            if (hiddenInput) {
                hiddenInput.value = precoUnitario;
                console.log('Campo oculto atualizado:', hiddenInput.value);
            }
        }

        if (event.target.name === "quantidade[]") {
            atualizarTotal();
        }
    });











    produtosLista.addEventListener("click", function (event) {
        if (event.target.classList.contains("remove-product")) {
            const productGroup = event.target.closest(".product-group");
            produtosLista.removeChild(productGroup);

            atualizarTotal();
        }
    });

    produtosLista.addEventListener("change", function (event) {
        if (event.target.name === "produto[]" || event.target.name === "quantidade[]") {
            atualizarTotal();
        }
    });

    function atualizarTotal() {
        let total = 0;

        document.querySelectorAll(".product-group").forEach(function (group) {
            const produtoSelect = group.querySelector('select[name="produto[]"]');
            const quantidadeInput = group.querySelector('input[name="quantidade[]"]');

            if (produtoSelect && quantidadeInput) {
                const preco = parseFloat(produtoSelect.selectedOptions[0]?.getAttribute("data-preco")) || 0;
                const quantidade = parseInt(quantidadeInput.value) || 0;
                total += preco * quantidade;
            }
        });

        totalVendaInput.value = formatarMoeda(total);
    }

    function formatarMoeda(valor) {
        return new Intl.NumberFormat('pt-BR', {
            style: 'currency',
            currency: 'BRL',
        }).format(valor);
    }


    const filterInput = document.getElementById('filter-name-input');
    const tableContainer = document.querySelector('.table-container');
    const tableRows = document.querySelectorAll('.venda-row');

    filterInput.addEventListener('input', function () {
        const filterValue = filterInput.value.toLowerCase();

        let hasVisibleRows = false;

        tableRows.forEach(row => {
            const vendaId = row.getAttribute('data-id').toLowerCase();
            const vendaFuncionario = row.getAttribute('data-funcionario').toLowerCase();
            const vendaData = row.getAttribute('data-date').toLowerCase();

            const isVisible =
                vendaId.includes(filterValue) ||
                vendaFuncionario.includes(filterValue) ||
                vendaData.includes(filterValue);

            if (isVisible) {
                row.style.display = 'table-row';
                hasVisibleRows = true;
            } else {
                row.style.display = 'none';
            }
        });

        const noResultsMessage = document.querySelector('.notification.is-warning');
        if (!hasVisibleRows) {
            if (!noResultsMessage) {
                const message = document.createElement('div');
                message.className = 'notification is-warning has-text-centered';
                message.innerHTML = `
                <div class="icon">
                    <i class="fa-solid fa-circle-info"></i>
                </div>
                <strong>Nenhuma venda encontrada!</strong>
            `;
                tableContainer.parentNode.insertBefore(message, tableContainer);
            }
            tableContainer.style.display = 'none';
        } else {
            if (noResultsMessage) {
                noResultsMessage.remove();
            }
            tableContainer.style.display = '';
        }
    });


    const vendaRow = document.querySelectorAll('.venda-row');
    const detailsVendaModal = document.getElementById('details-venda-modal');
    const cancelDetailsVendaModalBtn = document.getElementById('cancel-details-modal-btn');
    const closeDetailsVendaModalBtn = document.getElementById('close-details-modal-btn');

    const formatDate = (isoDate) => {
        const date = new Date(isoDate);
        const day = String(date.getDate()).padStart(2, '0');
        const month = String(date.getMonth() + 1).padStart(2, '0');
        const year = date.getFullYear();
        const hours = String(date.getHours()).padStart(2, '0');
        const minutes = String(date.getMinutes()).padStart(2, '0');
        return `${day}/${month}/${year} - ${hours}:${minutes}`
    };


    vendaRow.forEach(row => {
        row.addEventListener('click', () => {
            const vendaId = row.getAttribute('data-id');
            const funcionarioId = row.getAttribute('data-funcionario');
            const data = row.getAttribute('data-date');
            const nomeFuncionario = row.getAttribute('data-funcionario-name');
            const produtosJSON = row.getAttribute('data-produtos-quantidade');

            console.log(produtosJSON);

            const produtos = JSON.parse(produtosJSON);

            console.log('Venda ID:', vendaId);
            console.log('Funcionario ID:', funcionarioId);
            console.log('Nome do funcionário:', nomeFuncionario);
            console.log('Produtos:', produtos);
            console.log('Data:', data);

            document.getElementById('modal-venda-id').textContent = `#${vendaId}`;
            document.getElementById('modal-venda-data').textContent = formatDate(data);
            document.getElementById('modal-funcionario-nome').textContent = nomeFuncionario;

            let produtosLista = '';
            let precoTotal = 0;
            produtos.forEach(produto => {
                produtosLista += `${produto.produto} <b>(${produto.quantidade}x)</b> - [ R$ ${formatarMoeda(produto.preco_unitario.toFixed(2))}]<br>`;
                precoTotal += produto.preco_unitario * produto.quantidade;
            });

            document.getElementById('modal-produtos-lista').innerHTML = produtosLista;
            document.getElementById('modal-preco-total').textContent = formatarMoeda(precoTotal.toFixed(2));

            detailsVendaModal.classList.add('is-active');
        });
    });


    cancelDetailsVendaModalBtn.addEventListener('click', () => {
        detailsVendaModal.classList.remove('is-active');
    });

    detailsVendaModal.querySelector('.modal-background').addEventListener('click', () => {
        detailsVendaModal.classList.remove('is-active');
    });

    closeDetailsVendaModalBtn.addEventListener('click', () => {
        detailsVendaModal.classList.remove('is-active');
    });

    const addVendaBtn = document.getElementById('add-venda-btn');
    const addVendaModal = document.getElementById('add-venda-modal');
    const closeAddVendaModalBtn = document.getElementById('close-add-venda-modal-btn');
    const cancelAddVendaModalBtn = document.getElementById('cancel-add-venda-modal-btn');
    const saveAddVendaModalBtn = document.getElementById('save-venda-modal-btn');
    const vendasForm = document.getElementById('new-venda-form');
    const cancelVendaModalBtn = document.getElementById("cancel-venda-modal-btn");


    addVendaBtn.addEventListener('click', () => {
        addVendaModal.classList.add('is-active');
    });

    closeAddVendaModalBtn.addEventListener('click', () => {
        addVendaModal.classList.remove('is-active');
    });

    addVendaModal.querySelector('.modal-background').addEventListener('click', () => {
        addVendaModal.classList.remove('is-active');
    });

    cancelAddVendaModalBtn.addEventListener('click', () => {
        addVendaModal.classList.remove('is-active');
    });


    saveAddVendaModalBtn.addEventListener('click', () => {
        vendasForm.submit();
    });

    cancelVendaModalBtn.addEventListener("click", function () {
        addVendaModal.classList.remove('is-active');
    });



});





