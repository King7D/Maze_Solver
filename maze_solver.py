from flask import Flask, request, render_template_string

app = Flask(__name__)

# Function to generate an empty matrix with editable headers
def generate_empty_matrix(x_size, y_size):
    grid_str = """
    <table border='1' style='border-collapse: collapse;' class='matrix'>
    <tr>
        <td class='header-cell'></td>
    """
    # Add input fields for column headers
    for x in range(x_size):
        grid_str += f"<td class='header-cell'>"
        grid_str += f"<input type='number' name='cols_target{x}' value='' class='header-input'></td>"
    grid_str += "</tr>"

    # Add rows with input fields for row headers and empty cells
    for y in range(y_size):
        grid_str += f"<tr><td class='header-cell'>"
        grid_str += f"<input type='number' name='rows_target{y}' value='' class='header-input'></td>"
        for x in range(x_size):
            grid_str += "<td class='cell'> </td>"
        grid_str += "</tr>"
    grid_str += "</table>"
    return grid_str

# Function to display the solution matrix with steps
def print_solution_matrix(path, x_size, y_size, cols_target, rows_target):
    # Create a matrix with '.' as default values
    grid = [['.' for _ in range(x_size)] for _ in range(y_size)]
    
    # Place step numbers in the matrix
    for step, (x, y) in enumerate(path, start=1):
        grid[y][x] = str(step)
    
    # Create an HTML table with the solution steps
    grid_str = """
    <table border='1' style='border-collapse: collapse;' class='matrix'>
    <tr>
        <td class='header-cell'></td>
    """
    # Column targets as headers
    for col in cols_target:
        grid_str += f"<td class='header-cell'>{col}</td>"
    grid_str += "</tr>"

    # Row targets as headers with the solution steps in the cells
    for y, row in enumerate(grid):
        grid_str += f"<tr><td class='header-cell'>{rows_target[y]}</td>"
        for cell in row:
            grid_str += f"<td class='cell'>{cell}</td>"
        grid_str += "</tr>"
    grid_str += "</table>"
    return grid_str

# Function to solve the maze and return the result
def main(x_size, y_size, cols_target, rows_target):
    cols_counts = [0] * x_size
    rows_counts = [0] * y_size
    path = []
    visited = set()
    solutions = []

    solve(0, 0, x_size, y_size, path, visited, cols_counts, rows_counts, cols_target, rows_target, solutions)

    # Check if any solutions were found and return the first one
    if solutions:
        result = print_solution_matrix(solutions[0], x_size, y_size, cols_target, rows_target)
    else:
        result = "<h3>No solution found.</h3>"
    
    return result

# Function to solve the maze using backtracking
def solve(x, y, x_size, y_size, path, visited, cols_counts, rows_counts, cols_target, rows_target, solutions):
    visited.add((x, y))
    path.append((x, y))
    cols_counts[x] += 1
    rows_counts[y] += 1

    # Check if we reached the bottom-right cell and targets are met
    if (x, y) == (x_size - 1, y_size - 1):
        if cols_counts == cols_target and rows_counts == rows_target:
            solutions.append(path.copy())
        # Backtrack
        visited.remove((x, y))
        path.pop()
        cols_counts[x] -= 1
        rows_counts[y] -= 1
        return

    # Try moving to adjacent cells
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nx, ny = x + dx, y + dy
        if 0 <= nx < x_size and 0 <= ny < y_size and (nx, ny) not in visited:
            # Check if counts exceed target counts
            if cols_counts[nx] + 1 > cols_target[nx]:
                continue
            if rows_counts[ny] + 1 > rows_target[ny]:
                continue
            # Recurse into next cell
            solve(nx, ny, x_size, y_size, path, visited, cols_counts, rows_counts, cols_target, rows_target, solutions)
    
    # Backtrack
    visited.remove((x, y))
    path.pop()
    cols_counts[x] -= 1
    rows_counts[y] -= 1

# Define the HTML template with Jinja
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Solve Maze</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;
            margin: 0;
            padding: 20px;
        }
        h1 {
            color: #003366;
        }
        form {
            background-color: #ffffff;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            max-width: 600px;
            margin-bottom: 20px;
        }
        label {
            font-weight: bold;
            display: block;
            margin-top: 10px;
        }
        input[type="number"], input[type="text"] {
            width: 100%;
            padding: 10px;
            margin-top: 5px;
            margin-bottom: 10px;
            border: 1px solid #cccccc;
            border-radius: 4px;
        }
        button {
            background-color: #003366;
            color: #ffffff;
            padding: 10px 20px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 16px;
        }
        button:hover {
            background-color: #002244;
        }
        table {
            margin: 20px 0;
        }
        td {
            border: 1px solid #ccc;
        }
        .matrix {
            table-layout: fixed;
            width: 100%;
            max-width: 600px;
        }
        .header-cell {
            background-color: #003366;
            color: white;
            padding: 10px;
            text-align: center;
            font-weight: bold;
            width: 50px;
            height: 50px;
        }
        .header-input {
            width: 100%;
            height: 100%;
            box-sizing: border-box;
            text-align: center;
        }
        .cell {
            background-color: #ADD8E6;
            padding: 10px;
            text-align: center;
            width: 50px;
            height: 50px;
        }
    </style>
</head>
<body>
    <h1>Solve Maze Problem</h1>
    
    <!-- Maze Size Form -->
    <form method="post" action="/set_size">
        <label for="x_size">X Size:</label>
        <input type="number" id="x_size" name="x_size" placeholder="Enter X size" value="{{ x_size }}" required><br><br>
        
        <label for="y_size">Y Size:</label>
        <input type="number" id="y_size" name="y_size" placeholder="Enter Y size" value="{{ y_size }}" required><br><br>
        
        <button type="submit">Set</button>
    </form>
    
    <!-- Targets Form, displayed only if maze size is set -->
    {% if show_targets_form %}
    <form method="post" action="/solve">
        <!-- Matrix with Editable Headers -->
        <div style="overflow-x: auto;"> 
            {{ matrix|safe }}
        </div>
        <input type="hidden" name="x_size" value="{{ x_size }}">
        <input type="hidden" name="y_size" value="{{ y_size }}">
        
        <button type="submit">Solve</button>
    </form>
    {% endif %}

    <h2>Solution:</h2>
    <div id="output">{{ output|safe }}</div>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(html_template, x_size='', y_size='', 
                                  cols_target='', rows_target='', 
                                  matrix='', output='', show_targets_form=False)

@app.route('/set_size', methods=['POST'])
def set_size():
    # Set maze size based on user input
    x_size = int(request.form['x_size'])
    y_size = int(request.form['y_size'])
    
    # Generate and display an empty matrix with editable headers
    empty_matrix = generate_empty_matrix(x_size, y_size)
    
    # Render the form for target values and show the empty matrix
    return render_template_string(html_template, x_size=x_size, y_size=y_size, 
                                  cols_target='', rows_target='', 
                                  matrix=empty_matrix, output='', show_targets_form=True)

@app.route('/solve', methods=['POST'])
def solve_maze():
    # Get input from form
    x_size = int(request.form['x_size'])
    y_size = int(request.form['y_size'])
    
    # Collect column and row targets from form and convert to list of integers
    try:
        cols_target = [int(request.form.get(f'cols_target{x}', '0')) for x in range(x_size)]
        rows_target = [int(request.form.get(f'rows_target{y}', '0')) for y in range(y_size)]
    except ValueError:
        # If any value is not an integer, return an error
        result = "<h3>Error: All targets must be integers.</h3>"
        return render_template_string(html_template, x_size=x_size, y_size=y_size, 
                                      cols_target='', rows_target='', 
                                      matrix='', output=result, show_targets_form=True)
    
    # Solve the maze and return the solution matrix
    result = main(x_size, y_size, cols_target, rows_target)
    
    # Render the result and retain form inputs in the HTML
    return render_template_string(html_template, x_size=x_size, y_size=y_size, 
                                  cols_target=cols_target, rows_target=rows_target, 
                                  matrix='', output=result, show_targets_form=True)

if __name__ == "__main__":
    app.run(debug=True)
