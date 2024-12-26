create table Customers(
	Customer_ID int primary key,
	First_Name varchar(10) not null,
	Last_Name varchar(10) not null,
	Email varchar (30) unique,
	Phone varchar(15) unique,
	Address varchar(50),
	Date_Joined date default GETDATE(),
);
create table Orders(
	Order_ID int primary key,
	Customer_ID int foreign key references Customers(Customer_ID),
	Order_Date date default GETDATE(),
	Total_Amount decimal(12,2) not null, /*المبلغ الاجمالي للطلب*/
	Shipping_Address varchar(50) not null, /*عنوان الشحن*/ 
	Order_Status varchar(50) check (Order_Status in ('Pending', 'Shipped','Delivered')) not null
);
create table Payments(
	Payment_ID int primary key,
	Order_ID int foreign key references Orders(Order_ID),
	Payment_Status varchar(50) check (Payment_Status in ('Pending', 'Paid')) not null,
	Payment_Method varchar(50) check (Payment_Method in ('Credit Card', 'PayPal','Cash')) not null,
	Payment_Amount decimal(12,2) not null,
	Payment_Date date default GETDATE()
);
create table Order_Details(
	Order_Detail_ID int primary key,
	Order_ID int foreign key references Orders(Order_ID),
	Quantity int not null ,
	Price decimal(12,2) not null, /*السعر الخاص بالمنتج في هذا الطلب*/
);
create table Categories(
	Category_ID int primary key,
	Category_Name varchar(20) not null,
	Category_Description varchar(50),
);
create table Products(
	Product_ID int primary key,
	Category_ID int foreign key references Categories(Category_ID),
	Name varchar(30) not null,
	Product_Price decimal(12,2) not null,
	Description varchar(50),
	Stock int not null ,
	Image_URL nvarchar(50)
);
create table Products_Order_Details(
	FK_Order_Detail_ID int not null,
	FK_Product_ID int not null,
	constraint FK_Product_ID foreign key(FK_Product_ID)references Products(Product_ID),
	constraint FK_Order_Detail_ID foreign key(FK_Order_Detail_ID)references Order_Details(Order_Detail_ID),
	
);




