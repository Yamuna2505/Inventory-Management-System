from tkinter import*
from PIL import Image,ImageTk
from tkinter import ttk,messagebox
import sqlite3
import os
import time
import random

class salesClass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1100x600+200+100")
        self.root.title("Inventory Management System ")
        self.root.config(bg="white")
        self.root.resizable(True,True)
        self.root.focus_force()

        self.blll_list=[]
        self.var_invoice=StringVar()
        self.var_cname=StringVar()
        self.var_contact=StringVar()

        self.cart_list = []

        # ---------------- title ---------------------
        Label(self.root,text="Sales Dashboard",font=("goudy old style",30),bg="#184a45",fg="white",bd=3,relief=RIDGE).pack(side=TOP,fill=X,padx=10,pady=10)

        # ---------------- Customer Entry ------------
        lbl_cname=Label(self.root,text="Customer Name",font=("times new roman",15),bg="white").place(x=20,y=80)
        txt_cname=Entry(self.root,textvariable=self.var_cname,font=("times new roman",15),bg="lightyellow").place(x=180,y=80,width=200)

        lbl_contact=Label(self.root,text="Contact No.",font=("times new roman",15),bg="white").place(x=400,y=80)
        txt_contact=Entry(self.root,textvariable=self.var_contact,font=("times new roman",15),bg="lightyellow").place(x=530,y=80,width=200)

        # --------------- Product Entry ----------------
        lbl_product=Label(self.root,text="Product",font=("times new roman",15),bg="white").place(x=20,y=130)
        self.var_product=StringVar()
        self.cmb_product=ttk.Combobox(self.root,textvariable=self.var_product,font=("times new roman",13),state='readonly')
        self.cmb_product['values']=("Paracetamol","Dettol","Vicks","Mask","Sanitizer")
        self.cmb_product.place(x=180,y=130,width=200)
        self.cmb_product.current(0)

        lbl_qty=Label(self.root,text="Quantity",font=("times new roman",15),bg="white").place(x=400,y=130)
        self.var_qty=IntVar(value=1)
        txt_qty=Entry(self.root,textvariable=self.var_qty,font=("times new roman",15),bg="lightyellow").place(x=530,y=130,width=100)

        btn_add=Button(self.root,text="Add to Bill",command=self.add_to_cart,font=("times new roman",15),bg="#4caf50",fg="white",cursor="hand2").place(x=650,y=130,width=150)

        # ---------------- Bill Area ------------------
        bill_Frame=Frame(self.root,bd=3,relief=RIDGE)
        bill_Frame.place(x=20,y=180,width=500,height=360)
        
        lbl_title2=Label(bill_Frame,text="Customer Bill Area",font=("goudy old style",20),bg="orange").pack(side=TOP,fill=X)
        
        scrolly2=Scrollbar(bill_Frame,orient=VERTICAL)
        self.bill_area=Text(bill_Frame,bg="lightyellow",yscrollcommand=scrolly2.set)
        scrolly2.pack(side=RIGHT,fill=Y)
        scrolly2.config(command=self.bill_area.yview)
        self.bill_area.pack(fill=BOTH,expand=1)

        # ---------------- Control Buttons --------------
        btn_generate=Button(self.root,text="Generate & Save Bill",command=self.generate_bill,font=("times new roman",15),bg="#607d8b",fg="white").place(x=540,y=180,width=250,height=40)

    def add_to_cart(self):
        pname = self.var_product.get()
        qty = self.var_qty.get()
        price_dict = {
            "Paracetamol": 15,
            "Dettol": 90,
            "Vicks": 25,
            "Mask": 10,
            "Sanitizer": 50
        }
        if pname in price_dict:
            price = price_dict[pname]
            self.cart_list.append((pname, qty, price))
            messagebox.showinfo("Success", f"{pname} added to cart!", parent=self.root)

    def generate_bill(self):
        if self.var_cname.get() == "" or self.var_contact.get() == "":
            messagebox.showerror("Error", "Customer details required", parent=self.root)
            return
        if len(self.cart_list) == 0:
            messagebox.showerror("Error", "Add at least one product to generate bill", parent=self.root)
            return

        self.var_invoice.set(str(time.strftime("%Y%m%d%H%M%S") + str(random.randint(100,999))))
        self.bill_area.delete('1.0', END)
        bill_text = f'''
        INVENTORY SYSTEM - BILL
        Invoice No.: {self.var_invoice.get()}
        Customer: {self.var_cname.get()}
        Contact: {self.var_contact.get()}
        --------------------------------------------
        Product        Qty      Price       Total
        --------------------------------------------\n'''
        total_bill = 0
        for item in self.cart_list:
            pname, qty, price = item
            total = qty * price
            total_bill += total
            bill_text += f"\t{pname:15}\t{qty:<8}\t{price:<10} \t {total}\n"
        bill_text += f"\n\t--------------------------------------------\n \tTotal Bill: ₹{total_bill}\n\n\t\t\tThank you!"

        self.bill_area.insert(END, bill_text)

        # save bill to folder
        with open(f"bill/{self.var_invoice.get()}.txt", "w") as f:
            f.write(bill_text)
        messagebox.showinfo("Success", f"Bill No. {self.var_invoice.get()} saved", parent=self.root)
        self.cart_list.clear()

if __name__=="__main__":
    root=Tk()
    obj=salesClass(root)
    root.mainloop()
