// your_javascript.js

document.addEventListener("DOMContentLoaded", function () {
    const buyerModal = document.getElementById("buyerModal");
    const sellerModal = document.getElementById("sellerModal");

    const buyerButton = document.querySelector('[data-target="#buyerModal"]');
    const sellerButton = document.querySelector('[data-target="#sellerModal"]');

    buyerButton.addEventListener("click", function () {
        // Load content for the Buyer sign-up modal here
        buyerModal.innerHTML = `
            <div class="modal-dialog" role="document">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">Sign Up as a Buyer</h5>
                        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                            <span aria-hidden="true">&times;</span>
                        </button>
                    </div>
                    <div class="modal-body">
                        <!-- Add your Buyer sign-up form or content here -->
                        <!-- For example, you can include a form with fields for Buyer registration -->
                    </div>
                </div>
            </div>
        `;
    });

    sellerButton.addEventListener("click", function () {
        // Load content for the Seller sign-up modal here
        sellerModal.innerHTML = `
            <div class="modal-dialog" role="document">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">Sign Up as a Seller</h5>
                        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                            <span aria-hidden="true">&times;</span>
                        </button>
                    </div>
                    <div class="modal-body">
                        <!-- Add your Seller sign-up form or content here -->
                        <!-- For example, you can include a form with fields for Seller registration -->
                    </div>
                </div>
            </div>
        `;
    });
});
