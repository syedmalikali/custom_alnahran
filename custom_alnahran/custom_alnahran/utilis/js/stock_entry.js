frappe.ui.form.on("Stock Entry Detail", {

    item_code: function (frm  , cdt , cdn){

        // frm.clear_table("custom_last_transfer_details_");

        // if (frm.doc.purpose == "Material Transfer"){
        //     let row = locals[cdt][cdn]

        //     if(row.item_code){

        //         if(row.s_warehouse && row.t_warehouse){
                    
        //             frappe.call({
        //                 method :"custom_alnahran.custom_alnahran.utilis.py.stock_entry.get_last_transfer_stock_details",  
        //                 args:{
        //                 "item_code":  row.item_code,
        //                 "s_warehouse": row.s_warehouse,
        //                 "t_warehouse": row.t_warehouse 
        //                 } ,
        //                 callback : function (r){
        //                     if(r.message){
        //                         if(r.message.length > 0){
        //                             r.message.forEach(function(data) {
        //                                 frm.add_child("custom_last_transfer_details_", {
        //                                     stock_entry_id: data.parent,
        //                                     qty: data.qty,
        //                                     basic_rate: data.basic_rate
        //                                 });
        //                             });
        //                             frm.refresh_field("custom_last_transfer_details_");
        //                         }
        //                         else{
        //                             frm.refresh_field("custom_last_transfer_details_");
        //                             frappe.show_alert({ message: "No history found to fetch last stock transfer details.", indicator: "blue" }); 
        //                         }
        //                     }
        //                     else{
        //                         frm.refresh_field("custom_last_transfer_details_");
        //                         frappe.show_alert({ message: "No history found to fetch last stock transfer details.", indicator: "blue" });
        //                     }
        //                 }
        //             })


        //         }
        //         else{
        //         frappe.show_alert({ message: "Source and Target Warehouse not selected to fetch last stock transfer details.", indicator: "orange" });
        //         }
        //     }
        // }

        frm.clear_table("custom_last_transfer_details_warehouse_wise");

        if (frm.doc.purpose == "Material Transfer"){
            let row = locals[cdt][cdn]

            if(row.item_code){

                if(row.s_warehouse){
                    
                    frappe.call({
                        method :"custom_alnahran.custom_alnahran.utilis.py.stock_entry.get_last_transfer_stock_details_warehoue_wise",  
                        args:{
                        "item_code":  row.item_code,
                        "s_warehouse": row.s_warehouse
                        } ,
                        callback : function (r){
                            if(r.message){
                                if(r.message.length > 0){
                                    r.message.forEach(function(data) {
                                        frm.add_child("custom_last_transfer_details_warehouse_wise", {
                                            stock_entry_id: data.parent,
                                            warehouse: data.warehouse,
                                            qty: data.qty,
                                            basic_rate: data.basic_rate
                                        });
                                    });
                                    frm.refresh_field("custom_last_transfer_details_warehouse_wise");
                                }
                                else{
                                    frm.refresh_field("custom_last_transfer_details_warehouse_wise");
                                    frappe.show_alert({ message: "No history found to fetch last stock transfer details.", indicator: "blue" }); 
                                }
                            }
                            else{
                                frm.refresh_field("custom_last_transfer_details_warehouse_wise");
                                frappe.show_alert({ message: "No history found to fetch last stock transfer details.", indicator: "blue" });
                            }
                        }
                    })


                }
                else{
                frappe.show_alert({ message: "Source Warehouse not selected to fetch last stock transfer details.", indicator: "orange" });
                }
            }
        }
    }
  })