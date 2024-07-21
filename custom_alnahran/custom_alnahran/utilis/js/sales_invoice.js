frappe.ui.form.on("Sales Invoice Item" , {
  item_code: function (frm  , cdt , cdn){
    let row = locals[cdt][cdn]

    if(row.item_code){

      if(frm.doc.set_warehouse){
        frappe.call({
          method :"custom_alnahran.custom_alnahran.utilis.py.sales_invoice.get_last_purchaseand_stock_rate",  
          args:{
            "item_code":  row.item_code,
            "warehouse": frm.doc.set_warehouse      
          } ,
          callback : function (r){
            frappe.model.set_value(cdt, cdn, 'custom_last_purchase_rate', r.message[0])
            frappe.model.set_value(cdt, cdn, 'custom_last_stock_transfer_rate', r.message[1])
          }
        })
      }
      else{
        frappe.show_alert({ message: "Source Warehouse not selected to fetch last purchase and stock transfer rate.", indicator: "green" });
      }
    }
  }
})