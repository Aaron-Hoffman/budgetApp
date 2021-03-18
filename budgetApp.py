categories = []
CHARS_IN_LINE = 30
CHARS_IN_DESCRIPTION = 23


def make_decimal(num):
    nums = str(num).split('.')
    if len(nums) < 2:
        num = f"{num}.00"
        return num
    elif len(nums[1]) >= 2:
        return str(num)
    elif len(nums[1]) == 1:
        return f'{num}0'
    else:
        return f'{num}.00'


class Category:
    # create inital variables and category
    def __init__(self, category):
        self.category = category
        self.ledger = []
        self.balance = 0.00
        self.spent = 0.00
        categories.append(self)

    # define what should be printed when printing a category object
    def __repr__(self):
        lines = []
        # create title line with ***
        stars_number = (CHARS_IN_LINE - len(self.category))
        stars = '*' * int(stars_number / 2)
        if (stars_number % 2) == 0:
            top_line = f"{stars}{self.category}{stars}\n"
        else:
            # if error and * should be a beginning move it over here
            top_line = f"{stars}{self.category}{stars}*\n"
        # add to lines list
        lines.append(top_line)
        for entry in self.ledger:
            # figure out space between description and amount
            space = ' ' * \
                (30 - (len(entry['description'][:CHARS_IN_DESCRIPTION]) +
                       len(make_decimal(entry['amount']))))
            # add to lines list
            lines.append(entry['description'][:CHARS_IN_DESCRIPTION] + space +
                         make_decimal(entry['amount']) + '\n')
        # add total line to list
        lines.append(f'Total: {make_decimal(self.balance)}')
        return ''.join(lines)

    def deposit(self, amount, description=''):
        # add ledger entry
        self.ledger.append({
            'amount': float(amount),
            'description': description,
        })
        # update balance
        self.balance += float(amount)

    def withdraw(self, amount, description=''):
        # check available funds
        if not self.check_funds(amount):
            return False
        else:
           # update ledger
            self.ledger.append({
                'amount': float('-' + str(amount)),
                'description': description
            })
            # update balance and spent
            self.spent += float(amount)
            self.balance -= float(amount)
            return True

    def get_balance(self):
        return float(make_decimal(self.balance))

    def transfer(self, amount, category):
        # check available funds
        if not self.check_funds(amount):
            return False
        else:
            self.withdraw(amount, (f"Transfer to {category.category}"))
            category.deposit(amount, f"Transfer from {self.category}")
            return True

    def check_funds(self, amount):
        if self.balance < float(amount):
            return False
        else:
            return True


def create_spend_chart(categories):
    percentages = calculate_precentages(categories)
    graph_lines = create_graph(categories, percentages)
    arranged_names = arrange_names(categories)
    spend_chart = graph_lines + arranged_names
    return '\n'.join(spend_chart)


def calculate_precentages(categories):
    percentages = []
    total_spent = 0
    # calculate total spent for all categories
    for category in categories:
        total_spent += category.spent
    # calculate percentage
    for category in categories:
        percentage = (category.spent / total_spent) * 100
        # round down to 10
        percentage = int(str(percentage).split('.')[0])
        while percentage % 10 != 0:
            percentage -= 1
        percentages.append(percentage)
    return percentages


def create_graph(categories, percentages):
    graph_lines = []
    # title line
    graph_lines.append('Percentage spent by category')
    # add body of the graph with number down the side and 'o' for columns that qualify
    for i in range(100, -10, -10):
        space = " " * (3-len(str(i)))
        line = f"{space}{i}| "
        for percentage in percentages:
            if percentage >= i:
                line = line + 'o  '
            else:
                line = line + '   '
        graph_lines.append(line)
    # add x axis line
    graph_lines.append(f"    {'---' * len(categories)}-")
    return graph_lines


def name_length(categories):
    # create list of category names
    names = []
    for category in categories:
        names.append(category.category)
    # find longest category name
    longest = 0
    for category in names:
        if len(category) > longest:
            longest = len(category)
        else:
            longest = longest
    names_list = []
    # lengthen shorter categories with extra whitespace to avoid error later
    for category in names:
        if len(category) < longest:
            category = category + (' ' * (longest - len(category)))
            names_list.append(category)
        else:
            names_list.append(category)
    return names_list

# arrange names vertically


def arrange_names(categories):
    names_list = name_length(categories)
    arranged_names = []
    for i in range(len(names_list[0])):
        line = '     '
        for x in names_list:
            line = f'{line}{x[i]}  '
        arranged_names.append(line)
    return arranged_names


food = Category("Food")
food.deposit(1000, "initial deposit")
food.withdraw(10.15, "groceries")
food.withdraw(15.89, "restaurant and more food for dessert")
print(food.get_balance())
clothing = Category("Clothing")
food.transfer(50, clothing)
clothing.withdraw(25.55)
clothing.withdraw(100)
auto = Category("Auto")
auto.deposit(1000, "initial deposit")
auto.withdraw(15)

print(food)
print(clothing)

print(create_spend_chart([food, clothing, auto]))
