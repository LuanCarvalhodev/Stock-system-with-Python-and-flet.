# Stock-system-with-Python-and-flet.
This simple inventory system was created using Python together with the flet library, due to its simplicity of manipulation, with the aim of exercising fundamental programming skills.


SYSTEM CODES AND ALGORITHMS.
The system aims to manage the flow of products within a stock, allowing the inclusion, search, update and movement of items in an efficient and simplified manner. The system was developed using Python, with the Tkinter library for creating the graphical interface, allowing users to interact intuitively and practically with the system.
The system offers essential functionalities for stock management, such as product registration, carrying out movements (inputs and outputs), searching for products by different criteria (name, ID, category) and exporting data to an Excel file, which will be used for reports and analyses. The development was carried out with the objective of creating a simple, effective and intuitive tool.
The main functionalities implemented in the system are detailed below:

Product Registration
The system allows the registration of products, where the user must enter the name of the product, the product category, the price and the initial quantity in stock. The system automatically assigns a unique ID to each product at the time of registration, avoiding duplication. If the product already exists in stock, the system offers the option to update the quantity or move the product to another category, if the user wishes.
Registration Flow:
• The user fills in the name, price, category and quantity.
• The system checks whether the product already exists in stock.
• If the product exists, the system updates the quantity.
• Otherwise, the product is added to stock with an automatically generated ID.
Stock Movements (Input and Output)
The system allows the user to record product input and output movements, changing the quantity available in stock. The type of movement (input or output) must be specified, along with the quantity moved.
Movement Functionalities:
• Stock Input: Increases the quantity of the product in stock.
• Stock Output: Decreases the quantity of the product, ensuring that the quantity is not negative. If the quantity desired for output is greater than the quantity available, the system issues an error.
The movement is recorded through a Movement History, which stores the type (input or output), the date of the movement, the name of the product and the quantity moved.

Movement Flow:
• The user selects the product and the quantity.
• The system validates the operation.
• The quantity of the product in the stock is adjusted.
• The movement is recorded in the history.
• Product Search
Product searches can be performed in several ways:
• By Name: The user can type the name of the product and the system will return all products that contain that name.
• By ID: The user can type the product ID and the system will return the specific product.
• By Category: The system also allows you to filter products by category, making it easier to search for items within the same class.
• The search returns a results table, which displays information such as the ID, name, category, price, quantity and status of the product.
Displaying Products in Stock
The interface displays the products registered in the system in a table, with the following columns:
• Product ID
• Name
• Category
• Price
• Quantity
• Status (indicates whether the product is "In Stock" or "Out of Stock").
This table is dynamically updated every time a product is added, changed or moved. The system allows the user to view the quantity and status of each product in real time.
Exporting Data to Excel
The export functionality allows the user to generate an Excel report with all products registered in the system. This report includes information such as:
• Product ID
• Name
• Category
• Price
• Quantity in Stock
• Status
This makes it easier to create backups or analyze the stock in other tools, such as Excel spreadsheets, and can be useful for accounting or auditing purposes.
Below you will find a demonstration of the system and its functionalities in action.
