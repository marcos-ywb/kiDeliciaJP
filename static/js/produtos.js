function deleteProduct() {
    const deleteBtn = document.getElementById('delete-details-modal-btn');
    const productId = deleteBtn.getAttribute('data-id');

    if (confirm('Tem certeza de que deseja excluir o produto?')) {
        if (productId) {
            fetch(`/tryDisableProduto/${productId}`, {
                method: 'PATCH'
            })
                .then(response => {
                    if (response.ok) {
                        document.getElementById('details-modal').classList.remove('is-active');
                        location.reload();
                    } else {
                        console.error('Erro ao excluir o produto');
                    }
                })
                .catch(error => console.error('Erro:', error));
        }

        else {
            console.error('ID do produto não encontrado');
        }
    }

}

function enableProduct() {
    const enableBtn = document.getElementById('activate-product-btn');
    const produtoId = enableBtn.getAttribute('data-disabled-product-id');

    if (confirm('Tem certeza que deseja ativar este produto?')) {
        fetch(`/tryEnableProduto/${produtoId}`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
            },
        })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    document.getElementById('disabled-products-modal').classList.remove('is-active');
                    location.reload();
                } else {
                    alert(data.message);
                }
            })
            .catch(error => {
                console.error('Erro ao ativar o produto:', error);
                alert('Erro ao ativar o produto.');
            });
    }
}

//Desnecessario (por enquanto!!!)
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}




document.addEventListener('DOMContentLoaded', () => {


    const filterInput = document.getElementById('filter-name-input');
    const tableRows = document.querySelectorAll('.product-row');

    filterInput.addEventListener('input', function () {
        const filterValue = filterInput.value.toLowerCase();

        let hasVisibleRows = false;

        tableRows.forEach(row => {
            const productName = row.getAttribute('data-nome').toLowerCase();

            if (productName.includes(filterValue)) {
                row.style.display = '';
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
                    <strong>Nenhum produto encontrado!</strong>
                `;
                document.querySelector('.table-container').appendChild(message);
            }
        } else {
            if (noResultsMessage) {
                noResultsMessage.remove();
            }
        }
    });


    const addProductBtn = document.getElementById('add-product-btn');
    const addProductModal = document.getElementById('add-product-modal');
    const closeAddProductModalBtn = document.getElementById('close-add-product-modal-btn');
    const cancelAddProductModalBtn = document.getElementById('cancel-modal-btn');
    const saveAddProductModalBtn = document.getElementById('save-modal-btn');
    const productForm = document.getElementById('new-product-form');

    addProductBtn.addEventListener('click', () => {
        addProductModal.classList.add('is-active');
    });

    closeAddProductModalBtn.addEventListener('click', () => {
        addProductModal.classList.remove('is-active');
    });

    cancelAddProductModalBtn.addEventListener('click', () => {
        addProductModal.classList.remove('is-active');
    });

    addProductModal.querySelector('.modal-background').addEventListener('click', () => {
        addProductModal.classList.remove('is-active');
    });

    saveAddProductModalBtn.addEventListener('click', () => {
        productForm.submit();
    });



    const productRows = document.querySelectorAll('.product-row');
    const detailsModal = document.getElementById('details-modal');
    const cancelDetailsModalBtn = document.getElementById('cancel-details-modal-btn');
    const closeDetailsModalBtn = document.getElementById('close-details-modal-btn');
    const deleteDetailsModalBtn = document.getElementById('delete-details-modal-btn');


    productRows.forEach(row => {
        row.addEventListener('click', () => {
            const id = row.getAttribute('data-id');
            const nome = row.getAttribute('data-nome');
            const preco = row.getAttribute('data-preco');
            const estoque = row.getAttribute('data-estoque');

            document.getElementById('modal-produto-nome').textContent = nome;
            document.getElementById('modal-produto-preco').textContent = preco;
            document.getElementById('modal-produto-estoque').textContent = estoque;

            deleteDetailsModalBtn.setAttribute('data-id', id);

            detailsModal.classList.add('is-active');
        });
    });

    cancelDetailsModalBtn.addEventListener('click', () => {
        detailsModal.classList.remove('is-active');
    });

    detailsModal.querySelector('.modal-background').addEventListener('click', () => {
        detailsModal.classList.remove('is-active');
    });

    closeDetailsModalBtn.addEventListener('click', () => {
        detailsModal.classList.remove('is-active');
    });











    const disabledProductsBtn = document.getElementById('disabled-products-btn');
    const disabledProductsModal = document.getElementById('disabled-products-modal');
    const closeDisabledProductsModalBtn = document.getElementById('close-disabled-products-modal-btn');
    const cancelDisabledProductsModalBtn = document.getElementById('cancel-disabled-products-btn');










    if (disabledProductsBtn) {
        disabledProductsBtn.addEventListener('click', () => {
            disabledProductsModal.classList.add('is-active');
        });
    }

    closeDisabledProductsModalBtn.addEventListener('click', () => {
        disabledProductsModal.classList.remove('is-active');
    });

    cancelDisabledProductsModalBtn.addEventListener('click', () => {
        disabledProductsModal.classList.remove('is-active');
    });

    disabledProductsModal.querySelector('.modal-background').addEventListener('click', () => {
        disabledProductsModal.classList.remove('is-active');
    });












});