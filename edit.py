import customtkinter as ctk
import CTkListbox
import os
import json
import datetime
from json import dump
from tkinter import messagebox
from tkcalendar import DateEntry

light_color_primary = "blue"  # Text color, light mode
dark_color_primary = "#ECD08E" # Text color, dark mode

light_color_secondary = "gray"
dark_color_secondary = "black"

def edit_project_window(app_instance, filename, update_options_menu=None):
    # Create a new window for editing a project
    edit_window = ctk.CTk()
    # Add this window to the main app's child_windows list
    app_instance.child_windows.append(edit_window)
    edit_window.title("Edit Project")

    # Determine the path to the projects folder
    current_path = os.path.join(os.path.dirname(__file__), 'projects')

    # Create the projects folder if it doesn't exist
    os.makedirs(current_path, exist_ok=True)

    filename = os.path.join(current_path, filename)

    # Function to load the selected project
    def load_project(filename):
        with open(filename, 'r') as file:
            return json.load(file)

    # Load the selected project
    project_data = load_project(filename)
    required_tools = project_data['required_tools']  # Use existing tools
    required_supplies = project_data['required_supplies']  # Use existing supplies

    def add_tool():
        tool = required_tools_entry.get()
        required_tools.append(tool)  # Append to list
        required_tools_listbox.insert("END", tool)  # Insert into listbox
        required_tools_entry.delete(0, 'end')  # Clear entry box

    def add_supply():
        supply = required_supplies_entry.get()
        required_supplies.append(supply)  # Append to list
        required_supplies_listbox.insert("END", supply)  # Insert into listbox
        required_supplies_entry.delete(0, 'end')  # Clear entry box

    def delete_tool():
        selected_index = required_tools_listbox.curselection()
        if isinstance(selected_index, tuple) and selected_index:
            index = selected_index[0]
        else:
            index = selected_index
        if index is not None:
            required_tools.pop(index)
            required_tools_listbox.delete(index)

    def delete_supply():
        selected_index = required_supplies_listbox.curselection()
        if isinstance(selected_index, tuple) and selected_index:
            index = selected_index[0]
        else:
            index = selected_index
        if index is not None:
            required_supplies.pop(index)
            required_supplies_listbox.delete(index)

    def save_project():
        try:
            project_data = {
                "name": project_name_entry.get(),
                "description": description_textbox.get("1.0", "end-1c"),
                "cut_list": cut_list_textbox.get("1.0", "end-1c"),
                "special_instructions": special_instructions_textbox.get("1.0", "end-1c"),
                "required_tools": required_tools,
                "required_supplies": required_supplies,
                "budget": {
                    "project_budget": project_budget_entry.get(),
                    "cost_of_materials": cost_of_materials_entry.get(),
                    "cost_of_labor": cost_of_labor_entry.get(),
                    "total_cost": total_cost_entry.get()
                }
            }
            if not project_data["name"].strip():
                raise ValueError("Project name cannot be empty!")
            
            # Save to the same filename
            with open(filename, 'w') as file:
                dump(project_data, file)
            
            edit_window.destroy()
            if update_options_menu:
                update_options_menu()

        except ValueError as e:
            messagebox.showerror(title="Error", message=str(e))
    edit_window = ctk.CTk()
    edit_window.title("Edit Project")
    edit_window.geometry("800x700")
    
    def tab_order():  # Set tab order
        project_name_entry.focus()  # Focus starts on the project name box
        widgets =[project_name_entry, description_textbox, cut_list_textbox, special_instructions_textbox, project_budget_entry, cost_of_materials_entry, cost_of_labor_entry, total_cost_entry,  required_tools_entry, required_tools_button, delete_tool_button, required_supplies_entry, required_supplies_button, delete_supply_button, cancel_button, save_button]
        for w in widgets:
            w.lift()

    def focus_next_window(event):
        event.widget.tk_focusNext().focus()
        return("break")

    def set_date_from_string(date_string):
        # Parse the date string using the specified format
        date_object = datetime.datetime.strptime(date_string, '%m/%d/%Y').date()
        # Set the date in the DateEntry widget
        # start_date.set_date(date_object)
    
    #############################  LEFT SIDE  #############################

    # Project Name
    ctk.CTkLabel(edit_window, text="Project Name / File Name:", corner_radius=10, text_color=(light_color_primary, dark_color_primary)).place(x=15, y=10)
    project_name_entry = ctk.CTkEntry(edit_window, corner_radius=10, width=400)
    project_name_entry.place(x=15, y=40)
    project_name_entry.insert(0, project_data['name']) # Populate with existing data

    # Description
    ctk.CTkLabel(edit_window, text="Description:", corner_radius=10, text_color=(light_color_primary, dark_color_primary)).place(x=15, y=80)
    description_textbox = ctk.CTkTextbox(edit_window, width=400, height=80, corner_radius=10, wrap="word")
    description_textbox.place(x=15, y=110)
    description_textbox.insert("1.0", project_data['description']) # Populate with existing data
    description_textbox.bind("<Tab>", focus_next_window)

    # Cut List
    ctk.CTkLabel(edit_window, text="Cut List:", corner_radius=10, text_color=(light_color_primary, dark_color_primary)).place(x=15, y=200)
    cut_list_textbox = ctk.CTkTextbox(edit_window, width=400, height=80, corner_radius=10, wrap="word")
    cut_list_textbox.place(x=15, y=230)
    cut_list_textbox.insert("1.0", project_data['cut_list']) # Populate with existing data
    cut_list_textbox.bind("<Tab>", focus_next_window)

    # Special Instructions
    ctk.CTkLabel(edit_window, text="Special Instructions:", corner_radius=10, text_color=(light_color_primary, dark_color_primary)).place(x=15, y=320)
    special_instructions_textbox = ctk.CTkTextbox(edit_window, width=400, height=80, corner_radius=10, wrap="word")
    special_instructions_textbox.place(x=15, y=350)
    special_instructions_textbox.insert("1.0", project_data['special_instructions']) # Populate with existing data
    special_instructions_textbox.bind("<Tab>", focus_next_window)
    
    # Notes
    ctk.CTkLabel(edit_window, text="Notes:", corner_radius=10, text_color=(light_color_primary, dark_color_primary)).place(x=15, y=440)
    notes_textbox = ctk.CTkTextbox(edit_window, width=400, height=50, corner_radius=10, wrap="word")
    notes_textbox.place(x=15, y=470)
    notes_textbox.insert("1.0", project_data['notes']) # Populate with existing data
    notes_textbox.bind("<Tab>", focus_next_window)
    
    # Customer Information
    ctk.CTkLabel(edit_window, text="Customer:", corner_radius=10, text_color=(light_color_primary, dark_color_primary)).place(x=15, y=550)
    customer_entry = ctk.CTkEntry(edit_window, corner_radius=10, width=150)
    customer_entry.insert(0, project_data['customer_entry']) # Populate with existing data
    customer_entry.place(x=15, y=580)
    
    ctk.CTkLabel(edit_window, text="Phone:", corner_radius=10, text_color=(light_color_primary, dark_color_primary)).place(x=225, y=550)
    phone_entry = ctk.CTkEntry(edit_window, corner_radius=10, width=150)
    phone_entry.insert(0, project_data['phone_entry'])
    phone_entry.place(x=225, y=580)
    
    ctk.CTkLabel(edit_window, text="Email:", corner_radius=10, text_color=(light_color_primary, dark_color_primary)).place(x=15, y=620)
    email_entry = ctk.CTkEntry(edit_window, corner_radius=10, width=150)
    email_entry.insert(0, project_data['email_entry'])
    email_entry.place(x=15, y=650)
    
    ctk.CTkLabel(edit_window, text="Other:", corner_radius=10, text_color=(light_color_primary, dark_color_primary)).place(x=225, y=620)
    other_entry = ctk.CTkEntry(edit_window, corner_radius=10, width=150)
    other_entry.insert(0, project_data['other_entry'])
    other_entry.place(x=225, y=650)    
    
    
    #############################  RIGHT SIDE  #############################

    # Required Tools
    ctk.CTkLabel(edit_window, text="Required Tools:", corner_radius=10, text_color=(light_color_primary, dark_color_primary)).place(x=450, y=10)
    required_tools_listbox = CTkListbox.CTkListbox(edit_window, width=120, height=100, corner_radius=10)
    required_tools_listbox.place(x=450, y=40)
    required_tools_entry = ctk.CTkEntry(edit_window, corner_radius=10, width=150)
    required_tools_entry.place(x=450, y=275)
    required_tools_button = ctk.CTkButton(edit_window, text="Add Tool", corner_radius=10, command=add_tool, text_color=(light_color_primary, dark_color_primary), width=150)
    required_tools_button.place(x=450, y=315)
    delete_tool_button = ctk.CTkButton(edit_window, text="Delete Tool", command=delete_tool, text_color=(light_color_primary, dark_color_primary), width=150, fg_color="#FF6666", hover_color="#FF3333", corner_radius=10)
    delete_tool_button.place(x=450, y=345)
    
    for tool in required_tools:
        required_tools_listbox.insert("END", tool)

    # Required Supplies
    ctk.CTkLabel(edit_window, text="Required Supplies:", corner_radius=10, text_color=(light_color_primary, dark_color_primary)).place(x=620, y=10)
    required_supplies_listbox = CTkListbox.CTkListbox(edit_window, width=120, height=100, corner_radius=10)
    required_supplies_listbox.place(x=620, y=40)
    required_supplies_entry = ctk.CTkEntry(edit_window, corner_radius=10, width=150)
    required_supplies_entry.place(x=620, y=275)
    required_supplies_button = ctk.CTkButton(edit_window, text="Add Supply", corner_radius=10, command=add_supply, text_color=(light_color_primary, dark_color_primary), width=150)
    required_supplies_button.place(x=620, y=315)
    delete_supply_button = ctk.CTkButton(edit_window, text="Delete Supply", command=delete_supply, text_color=(light_color_primary, dark_color_primary), width=150, fg_color="#FF6666", hover_color="#FF3333", corner_radius=10)
    delete_supply_button.place(x=620, y=345)
    
    for supply in required_supplies:
        required_supplies_listbox.insert("END", supply)

    # Budgeting
    ctk.CTkLabel(edit_window, text="Project Budget:", corner_radius=10, text_color=(light_color_primary, dark_color_primary)).place(x=450, y=400)
    project_budget_entry = ctk.CTkEntry(edit_window, corner_radius=10, width=150)
    project_budget_entry.insert(0, project_data['project_budget'])
    project_budget_entry.place(x=450, y=430)
    
    ctk.CTkLabel(edit_window, text="Materials Cost:", corner_radius=10, text_color=(light_color_primary, dark_color_primary)).place(x=450, y=470)
    cost_of_materials_entry = ctk.CTkEntry(edit_window, corner_radius=10, width=150)
    cost_of_materials_entry.insert(0, project_data['cost_of_materials'])
    cost_of_materials_entry.place(x=450, y=500)
    
    ctk.CTkLabel(edit_window, text="Labor Cost:", corner_radius=10, text_color=(light_color_primary, dark_color_primary)).place(x=620, y=400)
    cost_of_labor_entry = ctk.CTkEntry(edit_window, corner_radius=10, width=150)
    cost_of_labor_entry.insert(0, project_data['cost_of_labor'])
    cost_of_labor_entry.place(x=620, y=430)
    
    ctk.CTkLabel(edit_window, text="Total Cost:", corner_radius=10, text_color=(light_color_primary, dark_color_primary)).place(x=620, y=470)
    total_cost_entry = ctk.CTkEntry(edit_window, corner_radius=10, width=150)
    total_cost_entry.insert(0, project_data['total_cost'])
    total_cost_entry.place(x=620, y=500)
    
    # DateEntry for Start and Completion
    ctk.CTkLabel(edit_window, text="Start:", corner_radius=10, text_color=(light_color_primary, dark_color_primary)).place(x=450, y=550)
    ctk.CTkLabel(edit_window, text="Complete:", corner_radius=10, text_color=(light_color_primary, dark_color_primary)).place(x=620, y=550)
    
    start_date = DateEntry(edit_window, width=12, background="black", foreground="yellow", borderwidth=2)
    completion_date = DateEntry(edit_window, width=12, background="black", foreground="yellow", borderwidth=2)
    start_date.place(x=450, y=580)
    start_date.set_date(project_data['start_date'])
    completion_date.place(x=620, y=580)
    completion_date.set_date(project_data['completion_date'])

    # Save button
    save_button = ctk.CTkButton(edit_window, corner_radius=10, text="Save Project", text_color=("white", "black"), width=150,  fg_color="#99FFCC", hover_color="#00F800", command=save_project)
    save_button.place(x=620, y=650)

    # Cancel Button
    cancel_button = ctk.CTkButton(edit_window, text="Cancel", command=edit_window.destroy, corner_radius=10, width=150, text_color=(light_color_primary, dark_color_primary), fg_color="#FF6666", hover_color="#FF3333")
    cancel_button.place(x=450, y=650)


    tab_order()  # Set the tab order for our widgets
    
    edit_window.focus_set()
    edit_window.mainloop()
