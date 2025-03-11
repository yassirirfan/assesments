# 🚀 Odoo Webhook Exporter  

This Odoo module automatically **exports PoS order data** to a specified webhook **in JSON format** when an order is created.  

## 📦 Features  
✅ Sends **PoS order details** to a webhook URL automatically.  
✅ Includes **customer, payment, and product details** in the payload.  
✅ Uses **asynchronous threading** for **faster performance** (non-blocking).  
✅ Configurable webhook URL via **Odoo System Parameters**.  
✅ **Easy integration** with third-party APIs, analytics tools, or external systems.  

## 🔧 Installation  
1. Copy this module to your Odoo **addons** directory.  
2. Restart the Odoo server:  
   ```sh
   odoo --addons-path=addons -u webhook_exporter

