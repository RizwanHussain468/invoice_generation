//Add new row
const tBody = document.getElementById("table-body");

// addNewRow =()=> {
//     const row = document.createElement("tr");
//     row.className = "single-row";
//     row.innerHTML = `<td style="text-align: right;"><span class="material-icons" action="delete">delete_outline</span></td>
//                      <td><input type="number" placeholder="0" name="amount" class="amount" id="amount" disabled style="font-size: large;" ></td>
//                     <td><input type="number" placeholder="0" name="price" class="price" id="price" onkeyup="getInput()" style="font-size: large;"></td>
//                     <td><div class="input-group mb-3">
//   <select class="custom-select" id="product" style="font-size: large;">
//      <option selected>تفصیل ...</option>
//                                 <option value="1">سریا 1/4 DF </option>
//                                 <option value="2">سریا 3/8 DF</option>
//                                 <option value="3">سریا 1/2 DF</option>
//                                 <option value="4">سریا 5/8 DF</option>
//                                 <option value="5">سریا 3/4 DF</option>
//                                 <option value="6">سریا 1/4 پلین گول</option>
//                                 <option value="7">سریا 3/8 پلین گول</option>
//                                 <option value="8">سریا 1/2 پلین گول</option>
//                                 <option value="9">سریا 1/4 چورس</option>
//                                 <option value="10">سریا 3/8 چورس</option>
//                                 <option value="11">سریا 1/2 چورس</option>
//                                 <option value="12">اینگل / پٹی</option>
//                                 <option value="13">چوکاٹھ جستی 16 گیج</option>
//                                 <option value="14">چوکاٹھ جستی 18 گیج</option>
//                                 <option value="15">کالی چادر پلین</option>
//                                 <option value="13">چادر گولہ ڈبی</option>
//                                 <option value="14">چادر لاہوری</option>
//   </select>
// </div></td>
//                     <td><input type="number" placeholder="0" name="unit" class="unit" id="unit" onkeyup="getInput()" style="font-size: large;">
//                      <select class="custom-select" id="type" style="font-size: large;">
//                         <option value="1"></option>
//                         <option value="2">kg</option>
//                         <option value="3">ft</option>
//                     </select>
//                     </td>`
    
//     tBody.insertBefore(row, tBody.lastElementChild.previousSibling);
// }

// document.getElementById("add-row").addEventListener("click", (e)=> {
//     e.preventDefault();
//     addNewR  ow();
// });

document.addEventListener('DOMContentLoaded', function () {
    // Set the initial value of total_amount input field
    var previousDebitAmount = parseFloat("{{ previous_debit_amount }}") || 0;
    document.getElementById('total_amount').value = previousDebitAmount;

    // Add event listeners to update total_amount dynamically
    document.getElementById('unit_price').addEventListener('keyup', updateTotalAmount);
    document.getElementById('quantity').addEventListener('keyup', updateTotalAmount);
    document.getElementById('loading_amount').addEventListener('keyup', updateTotalAmount);
    document.getElementById('debit_amount').addEventListener('keyup', updateTotalAmount);

    function updateTotalAmount() {
        // Calculate total amount based on selected product prices and user input
        var unitPrice = parseFloat(document.getElementById('unit_price').value) || 0;
        var quantity = parseFloat(document.getElementById('quantity').value) || 0;
        var loadingAmount = parseFloat(document.getElementById('loading_amount').value) || 0;
        var debitAmount = parseFloat(document.getElementById('debit_amount').value) || 0;

        var totalAmount = unitPrice * quantity + loadingAmount - debitAmount + previousDebitAmount;

        // Update the total_amount input field
        document.getElementById('total_amount').value = totalAmount.toFixed(2);
    }
});

document.getElementById('downloadPDF').addEventListener('click', function () {
    const element = document.getElementById('pdfContent');

    // Options for PDF generation
    const options = {
        margin: 2,
        filename: 'document.pdf',
        image: { type: 'jpeg', quality: 1.0 },
        html2canvas: {scale:3, logging: true, useCORS: true }, // Adjusted options for html2canvas
        jsPDF: { quantity: 'mm', format: 'a4', orientation: 'portrait' }
    };

    html2pdf(element, options);

});

document.getElementById('add-row').addEventListener('click', function (e) {
    e.preventDefault();
    cloneRow();
});

function cloneRow() {
    // Get the reference to the table body
    var tableBody = document.getElementById('table-body');

    // Get the reference to the original row
    var originalRow = document.getElementById('single-row');

    // Clone the original row
    var newRow = originalRow.cloneNode(true);

    // Generate unique IDs for the new elements
    var newId = 'row-' + new Date().getTime();
    newRow.id = newId;
    newRow.querySelector('.unit_price').id = 'unit_price-' + newId;
    newRow.querySelector('.quantity').id = 'quantity-' + newId;
    newRow.querySelector('#product').id = 'product-' + newId;

    // Reset the values in the cloned row (optional)
    newRow.querySelector('.unit_price').value = '';
    newRow.querySelector('.quantity').value = '';
    newRow.querySelector('#product').selectedIndex = 0;

    // Append the new row to the table
    tableBody.appendChild(newRow);

    // Reattach the event handlers
    newRow.querySelector('.unit_price').addEventListener('input', getInput);
    newRow.querySelector('.quantity').addEventListener('input', getInput);
}

//GET INPUTS, MULTIPLY AND GET THE ITEM PRICE
getInput =()=> {
    var rows = document.querySelectorAll("tr.single-row");
    rows.forEach((currentRow) => {
        var quantity = currentRow.querySelector("#quantity").value;
        var unit_price = currentRow.querySelector("#unit_price").value;
        unit_price
        price = quantity * unit_price;
        currentRow.querySelector("#price").value = price;
        overallSum();
        
    })
};




//Get the overall sum/Total
overallSum =()=> {
    var arr = document.getElementsByName("price");
    var total_amount = 0;
    for(var i = 0; i < arr.length; i++) {
        if(arr[i].value) {
            total_amount += +arr[i].value;
        }
        document.getElementById("total_amount").value = total_amount;
    }

    var loading_amount = parseFloat(document.getElementsByName("loading_amount")[0].value) || 0;
    total_amount = total_amount + loading_amount;
    document.getElementById("total_amount").value = total_amount;

    var debit_amount = parseFloat(document.getElementsByName("debit_amount")[0].value) || 0;
    total_amount -= debit_amount;
    document.getElementById("total_amount").value = total_amount;
}

//Delete row from the table
// tBody.addEventListener("click", (e)=>{
//     let el = e.target;
//     const deleteROW = e.target.attributes.action?.value;
//     if(deleteROW == "delete") {
//         delRow(el);
//         overallSum();
//     }
// })

function addScript(url) {
    var script = document.createElement('script');
    script.type = 'application/javascript';
    script.src = url;
    document.head.appendChild(script);
}
addScript('https://cdnjs.cloudflare.com/ajax/libs/html2pdf.js/0.10.1/html2pdf.bundle.min.js');



// //Target row and remove from DOM;
// delRow =(el)=> {
//     el.parentNode.parentNode.parentNode.removeChild(el.parentNode.parentNode);
// }
