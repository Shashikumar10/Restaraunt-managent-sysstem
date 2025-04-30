# Node class for linked list to store menu items
class MenuItemNode:
    def __init__(self, item_name, price):
        self.item_name = item_name
        self.price = price
        self.next = None

# Linked list class for the menu
class Menu:
    def __init__(self):
        self.head = None

    def add_item(self, item_name, price):
        new_item = MenuItemNode(item_name, price)
        if not self.head:
            self.head = new_item
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_item

    def display_menu(self):
        current = self.head
        menu_items = []
        index = 1
        while current:
            menu_items.append(f"{index}. {current.item_name}: ${current.price:.2f}")
            current = current.next
            index += 1
        return menu_items

    def get_item_by_number(self, number):
        current = self.head
        index = 1
        while current:
            if index == number:
                return current
            current = current.next
            index += 1
        return None

# Order class to manage individual orders
class Order:
    def __init__(self, order_id, customer_name, items):
        self.order_id = order_id
        self.customer_name = customer_name
        self.items = items  # List of item nodes
        self.status = "Pending"  # Default status
        self.total_price = sum(item.price for item in items)

# Queue class to manage customer orders
class OrderQueue:
    def __init__(self):
        self.queue = []

    def place_order(self, order):
        self.queue.append(order)

    def modify_order(self, order_id, new_items):
        for order in self.queue:
            if order.order_id == order_id:
                order.items = new_items
                order.total_price = sum(item.price for item in new_items)
                return f"Order {order_id} has been modified."
        return "Order not found."

    def cancel_order(self, order_id):
        for i, order in enumerate(self.queue):
            if order.order_id == order_id:
                self.queue.pop(i)
                return f"Order {order_id} has been canceled."
        return "Order not found."

    def display_orders(self):
        return [
            (order.order_id, order.customer_name, [item.item_name for item in order.items], order.status, order.total_price)
            for order in self.queue
        ]

    def track_order(self, order_id):
        for order in self.queue:
            if order.order_id == order_id:
                return (order.order_id, order.customer_name, [item.item_name for item in order.items], order.status, order.total_price)
        return "Order not found."

# Main system class to interact with the user
class RestaurantManagementSystem:
    def __init__(self):
        self.menu = Menu()
        self.order_queue = OrderQueue()
        self.next_order_id = 1

    def add_menu_item(self, item_name, price):
        self.menu.add_item(item_name, price)
        return f"Added {item_name} to the menu."

    def show_menu(self):
        return self.menu.display_menu()

    def place_order(self):
        customer_name = input("Enter customer name: ")
        print("Enter the item numbers you want to order (separate by commas):")
        item_numbers = input().split(",")
        items = []

        for number in item_numbers:
            item = self.menu.get_item_by_number(int(number.strip()))
            if item:
                items.append(item)

        if items:
            order = Order(self.next_order_id, customer_name, items)
            self.order_queue.place_order(order)
            self.next_order_id += 1
            return f"Order {order.order_id} placed for {customer_name}."
        else:
            return "No valid items selected for the order."

    def modify_order(self, order_id):
        print("Enter the new item numbers for the order (separate by commas):")
        new_item_numbers = input().split(",")
        items = []

        for number in new_item_numbers:
            item = self.menu.get_item_by_number(int(number.strip()))
            if item:
                items.append(item)

        return self.order_queue.modify_order(order_id, items)

    def cancel_order(self, order_id):
        return self.order_queue.cancel_order(order_id)

    def show_orders(self):
        return self.order_queue.display_orders()

    def track_order(self, order_id):
        return self.order_queue.track_order(order_id)

    def generate_bill(self, order_id):
        for order in self.order_queue.queue:
            if order.order_id == order_id:
                return f"Bill for Order {order.order_id} (Customer: {order.customer_name}):\n" + \
                       "\n".join([f"{item.item_name}: ${item.price:.2f}" for item in order.items]) + \
                       f"\nTotal: ${order.total_price:.2f}"
        return "Order not found."

# Main program to run the restaurant management system
if __name__ == "__main__":
    print("Welcome to CBIT hotel")
    system = RestaurantManagementSystem()
    # Add menu items
    system.add_menu_item("Veg Biryani                ",100)
    system.add_menu_item("Aloo Biryani               ",90)
    system.add_menu_item("Mushroom Biryani           ",200)
    system.add_menu_item("Panner Biryani             ",150)
    system.add_menu_item("Babycorn Biryani           ",170)
    system.add_menu_item("Ulavacharu Egg Biryan      ",250)
    system.add_menu_item("Chicken Lollipop Biryani   ",190)
    system.add_menu_item("Mutton Biryani             ",200)
    system.add_menu_item("Fish Biryani               ",210)
    system.add_menu_item("Pig Biryani                ",150)

    while True:
        print("\nRestaurant Management System")
        print("1. Show Menu")
        print("2. Place Order")
        print("3. Modify Order")
        print("4. Cancel Order")
        print("5. Show Orders")
        print("6. Track Order")
        print("7. Generate Bill")
        print("8. Exit")
        choice = input("Select an option (1-8): ")

        if choice == "1":
            print("\nMenu:")
            print("\n".join(system.show_menu()))
        elif choice == "2":
            print(system.place_order())
        elif choice == "3":
            order_id = int(input("Enter the Order ID to modify: "))
            print(system.modify_order(order_id))
        elif choice == "4":
            order_id = int(input("Enter the Order ID to cancel: "))
            print(system.cancel_order(order_id))
        elif choice == "5":
            print("\nOrders:")
            for order in system.show_orders():
                print(f"Order ID: {order[0]}, Customer: {order[1]}, Items: {order[2]}, Status: {order[3]}, Total Price: ${order[4]:.2f}")
        elif choice == "6":
            order_id = int(input("Enter the Order ID to track: "))
            print(system.track_order(order_id))
        elif choice == "7":
            order_id = int(input("Enter the Order ID to generate the bill: "))
            print(system.generate_bill(order_id))
        elif choice == "8":
            print("Exiting the system. Thank you!")
            break
        else:
            print("Invalid option. Please try again.")
