$(function () {

    // ****************************************
    //  U T I L I T Y   F U N C T I O N S
    // ****************************************

    // Updates the form with data from the response
    function update_form_data(res) {
        $("#product_id").val(res.id);
        $("#product_name").val(res.name);
        $("#product_category").val(res.category);
        if (res.available == true) {
            $("#product_available").val("true");
        } else {
            $("#product_available").val("false");
        }
        $("#product_like").val(res.like);
        $("#product_color").val(res.color);
        $("#product_size").val(res.size);
        $("#product_create_date").val(res.create_date);
        $("#product_last_modify_date").val(res.last_modify_date);
    }

    /// Clears all form fields
    function clear_form_data() {
        $("#product_name").val("");
        $("#product_category").val("");
        $("#product_available").val("");
        $("#product_like").val("");
        $("#product_color").val("");
        $("#product_size").val("");
        $("#product_create_date").val("");
        $("#product_last_modify_date").val("");
    }

    // Updates the flash message area
    function flash_message(message) {
        $("#flash_message").empty();
        $("#flash_message").append(message);
    }

    // ****************************************
    // Create a Product
    // ****************************************

    $("#create-btn").click(function () {

        let name = $("#product_name").val();
        let category = $("#product_category").val();
        let available = $("#product_available").val() == "true";
        let like = $("#product_like").val();
        let color = $("#product_color").val();
        let size = $("#product_size").val();
        let create_date = $("#product_create_date").val();
        let last_modify_date = $("#product_last_modify_date").val();

        let data = {
            "name": name,
            "category": category,
            "available": available,
            "like": like,
            "color": color,
            "size": size,
            "create_date": create_date,
            "last_modify_date": last_modify_date
        };

        $("#flash_message").empty();
        
        let ajax = $.ajax({
            type: "POST",
            url: "/products",
            contentType: "application/json",
            data: JSON.stringify(data),
        });

        ajax.done(function(res){
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });
    });


    // ****************************************
    // Update a Product
    // ****************************************

    $("#update-btn").click(function () {

        let product_id = $("#product_id").val();
        let name = $("#product_name").val();
        let category = $("#product_category").val();
        let available = $("#product_available").val() == "true";
        let like = $("#product_like").val();
        let color = $("#product_color").val();
        let size = $("#product_size").val();
        let create_date = $("#product_create_date").val();
        let last_modify_date = $("#product_last_modify_date").val();

        let data = {
            "name": name,
            "category": category,
            "available": available,
            "like": like,
            "color": color,
            "size": size,
            "create_date": create_date,
            "last_modify_date": last_modify_date
        };

        $("#flash_message").empty();

        let ajax = $.ajax({
                type: "PUT",
                url: `/products/${product_id}`,
                contentType: "application/json",
                data: JSON.stringify(data)
            })

        ajax.done(function(res){
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Retrieve a Product
    // ****************************************

    $("#retrieve-btn").click(function () {

        let product_id = $("#product_id").val();

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "GET",
            url: `/products/${product_id}`,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            clear_form_data()
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Like a Product
    // ****************************************

    $("#like-btn").click(function () {

        let product_id = $("#product_id").val();

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "PUT",
            url: `/products/like/${product_id}`,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            update_form_data(res)
            flash_message("The product has been liked!")
        });

        ajax.fail(function(res){
            clear_form_data()
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Delete a Product
    // ****************************************

    $("#delete-btn").click(function () {

        let product_id = $("#product_id").val();

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "DELETE",
            url: `/products/${product_id}`,
            contentType: "application/json",
            data: '',
        })

        ajax.done(function(res){
            clear_form_data()
            flash_message("Product has been Deleted!")
        });

        ajax.fail(function(res){
            flash_message("Server error!")
        });
    });

    // ****************************************
    // Clear the form
    // ****************************************

    $("#clear-btn").click(function () {
        $("#product_id").val("");
        $("#flash_message").empty();
        clear_form_data()
    });

    // ****************************************
    // Search for a Product
    // ****************************************

    $("#search-btn").click(function () {

        let name = $("#product_name").val();
        let category = $("#product_category").val();
        let available = $("#product_available").val() == "true";

        let queryString = ""

        if (name) {
            queryString += 'name=' + name
        }
        if (category) {
            if (queryString.length > 0) {
                queryString += '&category=' + category
            } else {
                queryString += 'category=' + category
            }
        }
        if (available) {
            if (queryString.length > 0) {
                queryString += '&available=' + available
            } else {
                queryString += 'available=' + available
            }
        }

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "GET",
            url: `/products?${queryString}`,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            $("#search_results").empty();
            let table = '<table class="table table-striped" cellpadding="10">'
            table += '<thead><tr>'
            table += '<th class="col-md-2">ID</th>'
            table += '<th class="col-md-2">Name</th>'
            table += '<th class="col-md-2">Category</th>'
            table += '<th class="col-md-2">Available</th>'
            table += '<th class="col-md-2">Like</th>'
            table += '<th class="col-md-2">Color</th>'
            table += '<th class="col-md-2">Size</th>'
            table += '<th class="col-md-2">Create Date</th>'
            table += '<th class="col-md-2">Last Modify Date</th>'
            table += '</tr></thead><tbody>'
            let firstProduct = "";
            for(let i = 0; i < res.length; i++) {
                let product = res[i];
                table +=  `<tr id="row_${i}"><td>${product.id}</td><td>${product.name}</td><td>${product.category}</td><td>${product.available}</td><td>${product.like}</td><td>${product.color}</td><td>${product.size}</td><td>${product.create_date}</td><td>${product.last_modify_date}</td></tr>`;
                if (i == 0) {
                    firstProduct = product;
                }
            }
            table += '</tbody></table>';
            $("#search_results").append(table);

            // copy the first result to the form
            if (firstProduct != "") {
                update_form_data(firstProduct)
            }

            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

})
