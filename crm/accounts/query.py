from models import  Customer, Order ,Product

# (1) returns all customers from customer table
customers = Customer.objects.all()
# (2) returns first customers from customer table
firstcustomer = Customer.objects.first()

# (3) returns last customers from customer table
lastcustomer = Customer.objects.first()

# (4) returns single customer by name from customer table
customerByname = Customer.objects.get(name='John')

# (5) returns single customer by name from customer table
customerById = Customer.objects.get(id=5)

#(6) Returns all orders related to customer
firstcustomer.order_set.all()

#(7) Returns orders customer name : ( Query parent models values)

order = Order.objects.all()
parentname = order.customer.name

#(8) Returns products from products table with value of 'out door' in category attribute

products = Product.objects.filter(category = 'Out Door')

#(9) Order/Sort objects using id

leastToGreatest = Product.objects.all.order_by('id')
greatestToleast = Product.objects.all.order_by('-id')

#(10) Returns products with Tag name 'Sports'

productFiltered = Product.objects.filter(tag_name ='Sports')




